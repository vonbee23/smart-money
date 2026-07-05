import { formatRelativeTime } from "../lib/format";

export default function LastUpdated({ sources, meta }) {
  const entries = sources.map((s) => meta?.[s]).filter(Boolean);
  if (entries.length === 0) return null;

  const oldest = entries.reduce((a, b) => (new Date(a.last_updated) < new Date(b.last_updated) ? a : b));
  const anySample = entries.some((e) => e.is_sample);
  const relative = formatRelativeTime(oldest.last_updated);

  return (
    <div className="flex items-center justify-between px-4 pb-2 pt-3 text-[11px] text-ink-faint">
      <span className="font-mono">{relative ? `Updated ${relative}` : ""}</span>
      {anySample && (
        <span className="rounded-full bg-surface2 px-2 py-0.5 font-medium text-ink-muted">sample data</span>
      )}
    </div>
  );
}
