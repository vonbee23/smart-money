"""
CONVICTION SCORE FORMULA
========================
For every ticker, each of the 3 sources (Congress, Insiders, Polymarket) that
has any matching recent activity produces a (lean, strength) pair:

  lean     in [-1, 1]   direction: -1 fully bearish .. +1 fully bullish
  strength in [0, 1]    how much real, recent, sizeable activity backs it

Congress / Insiders, per trade or filing:
  direction = +1 for a buy, -1 for a sell (Congress "exchange" trades are ignored
              -- they aren't a directional bet)
  weight    = recency_weight(transaction_date) * size_weight(dollar_amount)
              recency_weight = 0.5 ** (age_in_days / half_life)   -- exponential decay
              size_weight    = min(1, log1p(amount) / log1p(scale))  -- log-scaled so
                                a single mega-trade can't single-handedly saturate it
  source lean     = Σ(direction_i * weight_i) / Σ(weight_i)
  source strength = min(1, Σ(weight_i) / saturation_constant)

Polymarket, per matched market (question text mentions the ticker's company):
  lean   = (yes_price - 0.5) * 2
  weight = volume_weight (log-scaled) * (1 + min(1, |24h change %|/10) * 0.3)
  combined the same way (weighted average lean, summed weight -> strength)

Combining the up-to-3 source leans for a ticker:
  weighted_lean   = Σ(lean_s * strength_s) / Σ(strength_s)     over sources present
  agreement_count = # of present sources whose lean sign matches sign(weighted_lean)
  agreement_ratio = agreement_count / 3   <- divided by 3 (not by sources present) so
                                             that having *more of the 3 possible
                                             sources* corroborate the call is what
                                             drives the score up, not just internal
                                             consistency among whichever 1-2 showed up
  avg_strength    = average strength across sources present

  CONVICTION = 100 * |weighted_lean| * agreement_ratio * (0.5 + 0.5 * avg_strength)

  direction       = "bullish"/"bearish" if |weighted_lean| > 0.05, else "neutral"
  high_conviction = all 3 sources present AND all 3 lean the same direction (⚡)

This rewards signals that are: (a) directionally strong, (b) corroborated by as
many of the 3 groups as possible, and (c) backed by recent, sizeable activity --
and it scores near zero when sources conflict or activity is thin/stale.
"""

import math
from datetime import datetime, timezone
from typing import Optional

from app.services.ticker_map import company_name

CONGRESS_HALF_LIFE_DAYS = 60
CONGRESS_SIZE_SCALE = 750_000
CONGRESS_SATURATION = 2.5

INSIDER_HALF_LIFE_DAYS = 45
INSIDER_SIZE_SCALE = 1_500_000
INSIDER_SATURATION = 2.5

POLYMARKET_VOLUME_SCALE = 5_000_000
POLYMARKET_SATURATION = 1.5

NEUTRAL_BAND = 0.05


def _recency_weight(date_str: Optional[str], half_life_days: float) -> float:
    if not date_str:
        return 0.0
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return 0.0
    age_days = max(0, (datetime.now(timezone.utc) - d).days)
    return 0.5 ** (age_days / half_life_days)


def _size_weight(value: Optional[float], scale: float) -> float:
    if not value or value <= 0:
        return 0.15
    return min(1.0, math.log1p(value) / math.log1p(scale))


def _congress_source(trades: list[dict]) -> tuple[Optional[float], float, int]:
    weighted_sum = 0.0
    weight_total = 0.0
    count = 0
    for t in trades:
        if t.get("transaction_type") not in ("buy", "sell"):
            continue
        direction = 1.0 if t["transaction_type"] == "buy" else -1.0
        recency = _recency_weight(t.get("transaction_date"), CONGRESS_HALF_LIFE_DAYS)
        mid = None
        if t.get("amount_min") is not None and t.get("amount_max") is not None:
            mid = (t["amount_min"] + t["amount_max"]) / 2
        w = recency * _size_weight(mid, CONGRESS_SIZE_SCALE)
        if w <= 0:
            continue
        weighted_sum += direction * w
        weight_total += w
        count += 1
    if weight_total == 0:
        return None, 0.0, 0
    return weighted_sum / weight_total, min(1.0, weight_total / CONGRESS_SATURATION), count


def _insider_source(filings: list[dict]) -> tuple[Optional[float], float, int]:
    weighted_sum = 0.0
    weight_total = 0.0
    count = 0
    for f in filings:
        if f.get("transaction_type") not in ("buy", "sell"):
            continue
        direction = 1.0 if f["transaction_type"] == "buy" else -1.0
        recency = _recency_weight(f.get("transaction_date") or f.get("filing_date"), INSIDER_HALF_LIFE_DAYS)
        w = recency * _size_weight(f.get("value"), INSIDER_SIZE_SCALE)
        if w <= 0:
            continue
        weighted_sum += direction * w
        weight_total += w
        count += 1
    if weight_total == 0:
        return None, 0.0, 0
    return weighted_sum / weight_total, min(1.0, weight_total / INSIDER_SATURATION), count


def _polymarket_source(markets: list[dict]) -> tuple[Optional[float], float, int]:
    weighted_sum = 0.0
    weight_total = 0.0
    count = 0
    for m in markets:
        lean = max(-1.0, min(1.0, (m["yes_price"] - 0.5) * 2))
        vol_w = _size_weight(m.get("volume"), POLYMARKET_VOLUME_SCALE)
        move_w = 1 + min(1.0, abs(m.get("change_24h") or 0) / 10) * 0.3
        w = vol_w * move_w
        weighted_sum += lean * w
        weight_total += w
        count += 1
    if weight_total == 0:
        return None, 0.0, 0
    return weighted_sum / weight_total, min(1.0, weight_total / POLYMARKET_SATURATION), count


def _combine(congress: tuple, insiders: tuple, polymarket: tuple) -> dict:
    raw = {"congress": congress, "insiders": insiders, "polymarket": polymarket}
    present = [name for name, (lean, _, count) in raw.items() if lean is not None and count > 0]

    breakdown = {
        name: dict(lean=raw[name][0], strength=raw[name][1] if raw[name][0] is not None else None, count=raw[name][2])
        for name in raw
    }

    if not present:
        return dict(score=0.0, direction="neutral", high_conviction=False, sources_present=[], breakdown=breakdown)

    strengths = {name: raw[name][1] for name in present}
    leans = {name: raw[name][0] for name in present}
    weight_total = sum(strengths.values())
    weighted_lean = (
        sum(leans[n] * strengths[n] for n in present) / weight_total
        if weight_total > 0
        else sum(leans.values()) / len(present)
    )

    if weighted_lean > NEUTRAL_BAND:
        direction, sign = "bullish", 1
    elif weighted_lean < -NEUTRAL_BAND:
        direction, sign = "bearish", -1
    else:
        direction, sign = "neutral", 0

    agreement_count = 0
    if sign != 0:
        for n in present:
            lean_sign = 1 if leans[n] > NEUTRAL_BAND else (-1 if leans[n] < -NEUTRAL_BAND else 0)
            if lean_sign == sign:
                agreement_count += 1

    avg_strength = sum(strengths.values()) / len(present)
    agreement_ratio = agreement_count / 3
    score = round(min(100.0, 100 * abs(weighted_lean) * agreement_ratio * (0.5 + 0.5 * avg_strength)), 1)
    high_conviction = len(present) == 3 and agreement_count == 3

    return dict(score=score, direction=direction, high_conviction=high_conviction,
                sources_present=present, breakdown=breakdown)


def build_conviction_board(congress_trades: list[dict], insider_filings: list[dict],
                            polymarket_markets: list[dict]) -> list[dict]:
    """Groups all cached records by ticker and scores each one."""
    tickers: set[str] = set()
    tickers.update(t["ticker"] for t in congress_trades)
    tickers.update(f["ticker"] for f in insider_filings)
    for m in polymarket_markets:
        tickers.update(m.get("tickers", []))

    board = []
    for ticker in tickers:
        t_congress = [t for t in congress_trades if t["ticker"] == ticker]
        t_insiders = [f for f in insider_filings if f["ticker"] == ticker]
        t_polymarket = [m for m in polymarket_markets if ticker in m.get("tickers", [])]

        result = _combine(_congress_source(t_congress), _insider_source(t_insiders), _polymarket_source(t_polymarket))

        company = None
        if t_congress:
            company = t_congress[0].get("company")
        if not company and t_insiders:
            company = t_insiders[0].get("company")
        company = company_name(ticker, company or "")

        board.append(dict(
            ticker=ticker,
            company=company,
            score=result["score"],
            direction=result["direction"],
            high_conviction=result["high_conviction"],
            sources_present=result["sources_present"],
            congress=result["breakdown"]["congress"],
            insiders=result["breakdown"]["insiders"],
            polymarket=result["breakdown"]["polymarket"],
            _congress_trades=t_congress,
            _insider_filings=t_insiders,
            _polymarket_markets=t_polymarket,
        ))

    board.sort(key=lambda x: x["score"], reverse=True)
    return board
