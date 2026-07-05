import { useMemo, useState } from "react";
import EmptyState from "../components/EmptyState";
import InsiderCard from "../components/InsiderCard";
import LastUpdated from "../components/LastUpdated";
import { SkeletonList } from "../components/Skeleton";
import { useData } from "../lib/DataContext";

export default function InsidersPage() {
  const { insiders, loading, meta } = useData();
  const [buysOnly, setBuysOnly] = useState(false);

  const filtered = useMemo(() => {
    if (!insiders) return null;
    return buysOnly ? insiders.filter((f) => f.transaction_type === "buy") : insiders;
  }, [insiders, buysOnly]);

  if (loading && !insiders) return <SkeletonList />;

  return (
    <div>
      <LastUpdated sources={["insiders"]} meta={meta} />
      <div className="flex items-center gap-2 px-4 pb-2">
        <button
          type="button"
          onClick={() => setBuysOnly(false)}
          className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
            !buysOnly ? "bg-teal text-bg" : "bg-surface text-ink-muted"
          }`}
        >
          All
        </button>
        <button
          type="button"
          onClick={() => setBuysOnly(true)}
          className={`rounded-full px-3 py-1.5 text-xs font-semibold transition ${
            buysOnly ? "bg-teal text-bg" : "bg-surface text-ink-muted"
          }`}
        >
          Buys only
        </button>
      </div>

      {filtered && filtered.length === 0 ? (
        <EmptyState title="No filings match" subtitle="Try switching back to All." />
      ) : (
        <div className="space-y-3 px-4 pb-4">
          {(filtered || []).map((f) => (
            <InsiderCard key={f.id} filing={f} />
          ))}
        </div>
      )}
    </div>
  );
}
