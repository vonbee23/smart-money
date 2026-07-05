import { useParams } from "react-router-dom";
import BackRow from "../components/BackRow";
import CongressCard from "../components/CongressCard";
import DirectionBadge from "../components/DirectionBadge";
import EmptyState from "../components/EmptyState";
import MarketCard from "../components/MarketCard";
import InsiderCard from "../components/InsiderCard";
import SourceBreakdown from "../components/SourceBreakdown";
import { SkeletonList } from "../components/Skeleton";
import WatchButton from "../components/WatchButton";
import { api } from "../lib/api";
import { useAsync } from "../hooks/useAsync";

function Section({ title, children, empty }) {
  return (
    <div className="mt-6">
      <h2 className="px-4 text-sm font-semibold text-ink-muted">{title}</h2>
      <div className="mt-2 space-y-3 px-4">{children.length ? children : empty}</div>
    </div>
  );
}

export default function TickerDetailPage() {
  const { ticker } = useParams();
  const { data, loading, error } = useAsync(() => api.convictionDetail(ticker), [ticker]);

  if (loading) return <SkeletonList count={4} />;
  if (error || !data) {
    return <EmptyState title="Couldn't load this ticker" subtitle="Try refreshing from the home screen." />;
  }

  return (
    <div className="pb-4">
      <BackRow label="Conviction" />

      <div className="flex items-start justify-between px-4 pt-2">
        <div>
          <div className="flex items-center gap-2">
            <span className="font-mono text-2xl font-bold text-ink">{data.ticker}</span>
            {data.high_conviction && <span title="High conviction">⚡</span>}
          </div>
          <p className="text-sm text-ink-muted">{data.company}</p>
        </div>
        <WatchButton ticker={data.ticker} />
      </div>

      <div className="mt-4 flex items-center gap-2 px-4">
        <DirectionBadge direction={data.direction} className="text-2xl" />
        <span className="font-mono text-5xl font-bold tabular-nums text-ink">{data.score.toFixed(0)}</span>
        <span className="pt-4 text-sm capitalize text-ink-muted">{data.direction}</span>
      </div>

      <div className="mt-6 px-4">
        <SourceBreakdown breakdown={{ congress: data.congress, insiders: data.insiders, polymarket: data.polymarket }} />
      </div>

      <Section title="CONGRESS TRADES" empty={<p className="text-sm text-ink-faint">No recent trades found.</p>}>
        {data.congress_trades.map((t) => (
          <CongressCard key={t.id} trade={t} />
        ))}
      </Section>

      <Section title="INSIDER FILINGS" empty={<p className="text-sm text-ink-faint">No recent filings found.</p>}>
        {data.insider_filings.map((f) => (
          <InsiderCard key={f.id} filing={f} />
        ))}
      </Section>

      <Section title="POLYMARKET MARKETS" empty={<p className="text-sm text-ink-faint">No related markets found.</p>}>
        {data.polymarket_markets.map((m) => (
          <MarketCard key={m.id} market={m} />
        ))}
      </Section>
    </div>
  );
}
