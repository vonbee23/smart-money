import { Link } from "react-router-dom";
import { formatMoney, formatPercent } from "../lib/format";

export default function MarketCard({ market }) {
  const yesPct = Math.round(market.yes_price * 100);
  const up = (market.change_24h ?? 0) >= 0;

  return (
    <Link
      to={`/polymarket/${encodeURIComponent(market.id)}`}
      className="block rounded-2xl border border-border bg-surface p-4 shadow-lg shadow-black/20 transition active:scale-[0.98]"
    >
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm font-medium leading-snug text-ink">{market.question}</p>
        {market.tickers?.length > 0 && (
          <span className="shrink-0 rounded-full bg-surface2 px-2 py-0.5 font-mono text-[11px] text-teal">
            {market.tickers[0]}
          </span>
        )}
      </div>

      <div className="mt-3 flex items-center gap-3">
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface2">
          <div className="h-full rounded-full bg-teal" style={{ width: `${yesPct}%` }} />
        </div>
        <span className="font-mono text-sm font-semibold text-ink">{yesPct}% YES</span>
      </div>

      <div className="mt-2 flex items-center justify-between font-mono text-xs text-ink-faint">
        <span>Vol {formatMoney(market.volume)}</span>
        {market.change_24h !== null && market.change_24h !== undefined && (
          <span className={up ? "text-bull" : "text-bear"}>{formatPercent(market.change_24h, { showSign: true })} 24h</span>
        )}
      </div>
    </Link>
  );
}
