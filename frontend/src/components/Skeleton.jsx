export function SkeletonCard() {
  return (
    <div className="rounded-2xl border border-border bg-surface p-4 shadow-lg shadow-black/20">
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <div className="skeleton h-4 w-20 rounded-md" />
          <div className="skeleton h-3 w-32 rounded-md" />
        </div>
        <div className="skeleton h-9 w-14 rounded-md" />
      </div>
    </div>
  );
}

export function SkeletonList({ count = 6 }) {
  return (
    <div className="space-y-3 p-4">
      {Array.from({ length: count }).map((_, i) => (
        <SkeletonCard key={i} />
      ))}
    </div>
  );
}
