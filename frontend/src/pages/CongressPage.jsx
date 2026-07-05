import EmptyState from "../components/EmptyState";
import CongressCard from "../components/CongressCard";
import LastUpdated from "../components/LastUpdated";
import { SkeletonList } from "../components/Skeleton";
import { useData } from "../lib/DataContext";

export default function CongressPage() {
  const { congress, loading, meta } = useData();

  if (loading && !congress) return <SkeletonList />;
  if (!congress || congress.length === 0) {
    return <EmptyState title="No congressional trades yet" subtitle="Tap refresh to check again." />;
  }

  return (
    <div>
      <LastUpdated sources={["congress"]} meta={meta} />
      <div className="space-y-3 px-4 pb-4">
        {congress.map((t) => (
          <CongressCard key={t.id} trade={t} />
        ))}
      </div>
    </div>
  );
}
