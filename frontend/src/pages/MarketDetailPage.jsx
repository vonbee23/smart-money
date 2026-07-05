import { Link, useParams } from "react-router-dom";
import BackRow from "../components/BackRow";
import EmptyState from "../components/EmptyState";
import { SkeletonList } from "../components/Skeleton";
import { api } from "../lib/api";
import { useAsync } from "../hooks/useAsync";
import { formatDate, formatMoney, formatPercent } from "../lib/format";

export default function MarketDetailPage() {
  const { id } = useParams();
  const { data: market, loading, error } = useAsync(() => api.polymarketDetail(id), [id]);

  if (loading) return <SkeletonList count={3} />;
  if (error || !market) {
    return <EmptyState title="Couldn't load this market" subtitle="Try refreshing from the Polymarket tab." />;
  }

  const yesPct = Math.round(market.yes_price * 100);
  const up = (market.change_24h ?? 0) >= 0;

  return (
    <div className="px-4 pb-6">
      <BackRow label="Polymarket" />
      <h1 className="mt-2 text-lg font-semibold leading-snug text-ink">{market.question}</h1>
      {market.category && <p className="mt-1 text-sm text-ink-muted">{market.category}</p>}

      <div className="mt-5 rounded-2xl border border-border bg-surface p-4">
        <div className="flex items-center justify-between">
          <span className="font-mono text-3xl font-bold text-teal">{yesPct}%</span>
          <span className="text-sm text-ink-muted">YES</span>
        </div>
        <div className="mt-2 h-2 overflow-hidden rounded-full bg-surface2">
          <div className="h-full rounded-full bg-teal" style={{ width: `${yesPct}%` }} />
        </div>
        {market.change_24h !== null && market.change_24h !== undefined && (
          <p className={`mt-2 font-mono text-sm ${up ? "text-bull" : "text-bear"}`}>
            {formatPercent(market.change_24h, { showSign: true })} in 24h
          </p>
        )}
      </div>

      <dl className="mt-4 grid grid-cols-2 gap-3">
        <div className="rounded-2xl border border-border bg-surface p-4">
          <dt className="text-xs text-ink-muted">Volume</dt>
          <dd className="mt-1 font-mono text-lg font-semibold text-ink">{formatMoney(market.volume)}</dd>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-4">
          <dt className="text-xs text-ink-muted">Liquidity</dt>
          <dd className="mt-1 font-mono text-lg font-semibold text-ink">{formatMoney(market.liquidity)}</dd>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-4">
          <dt className="text-xs text-ink-muted">Ends</dt>
          <dd className="mt-1 font-mono text-sm font-semibold text-ink">{formatDate(market.end_date)}</dd>
        </div>
        <div className="rounded-2xl border border-border bg-surface p-4">
          <dt className="text-xs text-ink-muted">Linked ticker</dt>
          <dd className="mt-1 font-mono text-sm font-semibold text-ink">
            {market.tickers?.length ? (
              <Link to={`/ticker/${market.tickers[0]}`} className="text-teal">
                {market.tickers.join(", ")}
              </Link>
            ) : (
              "—"
            )}
          </dd>
        </div>
      </dl>

      {market.url && (
        <a
          href={market.url}
          target="_blank"
          rel="noreferrer"
          className="mt-5 block rounded-2xl border border-border bg-surface py-3 text-center text-sm font-medium text-teal"
        >
          View on Polymarket ↗
        </a>
      )}
    </div>
  );
}
