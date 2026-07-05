"""Hand-authored, clearly-labeled fallback data used when a live source is
unreachable, so the app always renders a full, coherent experience end to end.
Every record here sets is_sample=True and the API/UI must surface that flag.
"""

from datetime import datetime, timedelta, timezone

NOW = datetime.now(timezone.utc)


def _days_ago(n: int) -> str:
    return (NOW - timedelta(days=n)).strftime("%Y-%m-%d")


SAMPLE_CONGRESS_TRADES = [
    dict(id="s-cg-1", representative="Nancy Pelosi", chamber="house", party="D",
         ticker="NVDA", company="NVIDIA Corporation", transaction_type="buy",
         amount_range="$1,000,001 - $5,000,000", amount_min=1000001, amount_max=5000000,
         transaction_date=_days_ago(12), disclosure_date=_days_ago(2)),
    dict(id="s-cg-2", representative="Dan Crenshaw", chamber="house", party="R",
         ticker="NVDA", company="NVIDIA Corporation", transaction_type="buy",
         amount_range="$15,001 - $50,000", amount_min=15001, amount_max=50000,
         transaction_date=_days_ago(20), disclosure_date=_days_ago(6)),
    dict(id="s-cg-3", representative="Ro Khanna", chamber="house", party="D",
         ticker="TSLA", company="Tesla, Inc.", transaction_type="sell",
         amount_range="$50,001 - $100,000", amount_min=50001, amount_max=100000,
         transaction_date=_days_ago(9), disclosure_date=_days_ago(1)),
    dict(id="s-cg-4", representative="Tommy Tuberville", chamber="senate", party="R",
         ticker="TSLA", company="Tesla, Inc.", transaction_type="sell",
         amount_range="$100,001 - $250,000", amount_min=100001, amount_max=250000,
         transaction_date=_days_ago(30), disclosure_date=_days_ago(15)),
    dict(id="s-cg-5", representative="Josh Gottheimer", chamber="house", party="D",
         ticker="AAPL", company="Apple Inc.", transaction_type="buy",
         amount_range="$1,001 - $15,000", amount_min=1001, amount_max=15000,
         transaction_date=_days_ago(40), disclosure_date=_days_ago(25)),
    dict(id="s-cg-6", representative="Marjorie Taylor Greene", chamber="house", party="R",
         ticker="PLTR", company="Palantir Technologies Inc.", transaction_type="buy",
         amount_range="$15,001 - $50,000", amount_min=15001, amount_max=50000,
         transaction_date=_days_ago(5), disclosure_date=_days_ago(1)),
    dict(id="s-cg-7", representative="Michael McCaul", chamber="house", party="R",
         ticker="PLTR", company="Palantir Technologies Inc.", transaction_type="buy",
         amount_range="$50,001 - $100,000", amount_min=50001, amount_max=100000,
         transaction_date=_days_ago(18), disclosure_date=_days_ago(4)),
    dict(id="s-cg-8", representative="Sheldon Whitehouse", chamber="senate", party="D",
         ticker="XOM", company="Exxon Mobil Corporation", transaction_type="sell",
         amount_range="$15,001 - $50,000", amount_min=15001, amount_max=50000,
         transaction_date=_days_ago(22), disclosure_date=_days_ago(8)),
    dict(id="s-cg-9", representative="Markwayne Mullin", chamber="senate", party="R",
         ticker="XOM", company="Exxon Mobil Corporation", transaction_type="buy",
         amount_range="$1,001 - $15,000", amount_min=1001, amount_max=15000,
         transaction_date=_days_ago(60), disclosure_date=_days_ago(44)),
    dict(id="s-cg-10", representative="Ro Khanna", chamber="house", party="D",
         ticker="AMD", company="Advanced Micro Devices, Inc.", transaction_type="buy",
         amount_range="$15,001 - $50,000", amount_min=15001, amount_max=50000,
         transaction_date=_days_ago(7), disclosure_date=_days_ago(3)),
    dict(id="s-cg-11", representative="Debbie Wasserman Schultz", chamber="house", party="D",
         ticker="MSFT", company="Microsoft Corporation", transaction_type="buy",
         amount_range="$1,001 - $15,000", amount_min=1001, amount_max=15000,
         transaction_date=_days_ago(35), disclosure_date=_days_ago(20)),
    dict(id="s-cg-12", representative="Pat Fallon", chamber="house", party="R",
         ticker="COIN", company="Coinbase Global, Inc.", transaction_type="sell",
         amount_range="$1,001 - $15,000", amount_min=1001, amount_max=15000,
         transaction_date=_days_ago(50), disclosure_date=_days_ago(35)),
]

SAMPLE_INSIDER_FILINGS = [
    dict(id="s-in-1", ticker="NVDA", company="NVIDIA Corporation", insider_name="Jensen Huang",
         role="CEO", transaction_type="buy", shares=15000, price_per_share=118.50,
         value=1777500, filing_date=_days_ago(3), transaction_date=_days_ago(4)),
    dict(id="s-in-2", ticker="NVDA", company="NVIDIA Corporation", insider_name="Mark Stevens",
         role="Director", transaction_type="buy", shares=5000, price_per_share=117.20,
         value=586000, filing_date=_days_ago(10), transaction_date=_days_ago(11)),
    dict(id="s-in-3", ticker="TSLA", company="Tesla, Inc.", insider_name="Robyn Denholm",
         role="Chair", transaction_type="sell", shares=20000, price_per_share=248.10,
         value=4962000, filing_date=_days_ago(6), transaction_date=_days_ago(7)),
    dict(id="s-in-4", ticker="TSLA", company="Tesla, Inc.", insider_name="Vaibhav Taneja",
         role="CFO", transaction_type="sell", shares=8000, price_per_share=251.40,
         value=2011200, filing_date=_days_ago(14), transaction_date=_days_ago(15)),
    dict(id="s-in-5", ticker="AAPL", company="Apple Inc.", insider_name="Deirdre O'Brien",
         role="SVP Retail", transaction_type="sell", shares=12000, price_per_share=195.30,
         value=2343600, filing_date=_days_ago(9), transaction_date=_days_ago(10)),
    dict(id="s-in-6", ticker="PLTR", company="Palantir Technologies Inc.", insider_name="Shyam Sankar",
         role="CTO", transaction_type="buy", shares=25000, price_per_share=24.80,
         value=620000, filing_date=_days_ago(2), transaction_date=_days_ago(3)),
    dict(id="s-in-7", ticker="AMD", company="Advanced Micro Devices, Inc.", insider_name="Lisa Su",
         role="CEO", transaction_type="buy", shares=6000, price_per_share=162.75,
         value=976500, filing_date=_days_ago(8), transaction_date=_days_ago(9)),
    dict(id="s-in-8", ticker="XOM", company="Exxon Mobil Corporation", insider_name="Kathryn Mikells",
         role="CFO", transaction_type="sell", shares=9000, price_per_share=114.60,
         value=1031400, filing_date=_days_ago(17), transaction_date=_days_ago(18)),
    dict(id="s-in-9", ticker="MSFT", company="Microsoft Corporation", insider_name="Satya Nadella",
         role="CEO", transaction_type="sell", shares=10000, price_per_share=420.10,
         value=4201000, filing_date=_days_ago(28), transaction_date=_days_ago(29)),
    dict(id="s-in-10", ticker="COIN", company="Coinbase Global, Inc.", insider_name="Brian Armstrong",
         role="CEO", transaction_type="sell", shares=15000, price_per_share=225.40,
         value=3381000, filing_date=_days_ago(5), transaction_date=_days_ago(6)),
    dict(id="s-in-11", ticker="META", company="Meta Platforms, Inc.", insider_name="Susan Li",
         role="CFO", transaction_type="buy", shares=1500, price_per_share=505.20,
         value=757800, filing_date=_days_ago(4), transaction_date=_days_ago(5)),
]

SAMPLE_POLYMARKET_MARKETS = [
    # NOTE ON POLARITY: the conviction engine reads a market's lean as
    # (yes_price - 0.5); every question below is phrased so that YES is the
    # stock-bullish outcome, keeping this sample set consistent with that
    # simple heuristic (see app/conviction.py docstring).
    dict(id="s-pm-1", question="Will NVIDIA be the world's most valuable company by end of 2026?",
         category="Business", yes_price=0.71, no_price=0.29, change_24h=3.2,
         volume=8_200_000, liquidity=1_400_000, end_date="2026-12-31",
         tickers=["NVDA"], url="https://polymarket.com"),
    dict(id="s-pm-2", question="Will Tesla stock trade above $300 by the end of Q3 2026?",
         category="Business", yes_price=0.28, no_price=0.72, change_24h=-4.5,
         volume=3_100_000, liquidity=610_000, end_date="2026-09-30",
         tickers=["TSLA"], url="https://polymarket.com"),
    dict(id="s-pm-3", question="Will Palantir win a new $500M+ government contract in 2026?",
         category="Business", yes_price=0.68, no_price=0.32, change_24h=2.4,
         volume=1_450_000, liquidity=310_000, end_date="2026-12-31",
         tickers=[], url="https://polymarket.com"),
    dict(id="s-pm-4", question="Will the Fed cut rates at the next FOMC meeting?",
         category="Economy", yes_price=0.55, no_price=0.45, change_24h=-1.8,
         volume=12_500_000, liquidity=2_800_000, end_date="2026-09-17",
         tickers=[], url="https://polymarket.com"),
    dict(id="s-pm-5", question="Will Coinbase stock close above $250 this quarter?",
         category="Business", yes_price=0.30, no_price=0.70, change_24h=-3.6,
         volume=980_000, liquidity=220_000, end_date="2026-09-30",
         tickers=[], url="https://polymarket.com"),
    dict(id="s-pm-6", question="Will Apple stock outperform the S&P 500 in 2026?",
         category="Business", yes_price=0.62, no_price=0.38, change_24h=1.4,
         volume=2_050_000, liquidity=440_000, end_date="2026-12-31",
         tickers=["AAPL"], url="https://polymarket.com"),
]
