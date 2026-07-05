import EmptyState from "../components/EmptyState";
import LastUpdated from "../components/LastUpdated";
import MarketCard from "../components/MarketCard";
import { SkeletonList } from "../components/Skeleton";
import { useData } from "../lib/DataContext";

export default function PolymarketPage() {
  const { polymarket, loading, meta } = useData();

  if (loading && !polymarket) return <SkeletonList />;
  if (!polymarket || polymarket.length === 0) {
    return <EmptyState title="No markets available" subtitle="Tap refresh to try Polymarket again." />;
  }

  return (
    <div>
      <LastUpdated sources={["polymarket"]} meta={meta} />
      <div className="space-y-3 px-4 pb-4">
        {polymarket.map((m) => (
          <MarketCard key={m.id} market={m} />
        ))}
      </div>
    </div>
  );
}
