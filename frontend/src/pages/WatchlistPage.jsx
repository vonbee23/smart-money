import EmptyState from "../components/EmptyState";
import { SkeletonList } from "../components/Skeleton";
import TickerCard from "../components/TickerCard";
import { useWatchlist } from "../hooks/useWatchlist";
import { useData } from "../lib/DataContext";

export default function WatchlistPage() {
  const { conviction, loading } = useData();
  const { tickers } = useWatchlist();

  if (loading && !conviction) return <SkeletonList />;

  if (tickers.length === 0) {
    return (
      <EmptyState
        title="Your watchlist is empty"
        subtitle="Tap the star on any ticker to track it here."
      />
    );
  }

  const entries = (conviction || []).filter((e) => tickers.includes(e.ticker));
  const missing = tickers.filter((t) => !entries.some((e) => e.ticker === t));

  return (
    <div className="space-y-3 px-4 py-4">
      {entries.map((entry) => (
        <TickerCard key={entry.ticker} entry={entry} />
      ))}
      {missing.map((t) => (
        <div key={t} className="rounded-2xl border border-dashed border-border p-4 text-sm text-ink-faint">
          <span className="font-mono text-ink-muted">{t}</span> — no current activity from any source.
        </div>
      ))}
    </div>
  );
}
