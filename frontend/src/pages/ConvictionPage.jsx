import EmptyState from "../components/EmptyState";
import LastUpdated from "../components/LastUpdated";
import { SkeletonList } from "../components/Skeleton";
import TickerCard from "../components/TickerCard";
import { useData } from "../lib/DataContext";

export default function ConvictionPage() {
  const { conviction, loading, meta } = useData();

  if (loading && !conviction) return <SkeletonList />;
  if (!conviction || conviction.length === 0) {
    return <EmptyState title="No conviction signals yet" subtitle="Tap refresh once data sources are available." />;
  }

  return (
    <div>
      <LastUpdated sources={["congress", "insiders", "polymarket"]} meta={meta} />
      <div className="space-y-3 px-4 pb-4">
        {conviction.map((entry) => (
          <TickerCard key={entry.ticker} entry={entry} />
        ))}
      </div>
    </div>
  );
}
