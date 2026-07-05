import { IconBriefcase, IconChart, IconLandmark } from "./icons";

const SOURCES = [
  { key: "congress", label: "Congress", Icon: IconLandmark },
  { key: "insiders", label: "Insiders", Icon: IconBriefcase },
  { key: "polymarket", label: "Polymarket", Icon: IconChart },
];

function leanLabel(lean) {
  if (lean === null || lean === undefined) return "No data";
  if (lean > 0.05) return "Bullish";
  if (lean < -0.05) return "Bearish";
  return "Neutral";
}

function leanColor(lean) {
  if (lean === null || lean === undefined) return "text-ink-faint";
  if (lean > 0.05) return "text-bull";
  if (lean < -0.05) return "text-bear";
  return "text-ink-muted";
}

export default function SourceBreakdown({ breakdown }) {
  return (
    <div className="space-y-3 rounded-2xl border border-border bg-surface p-4">
      {SOURCES.map(({ key, label, Icon }) => {
        const b = breakdown[key] || {};
        const hasData = b.lean !== null && b.lean !== undefined && b.count > 0;
        const markerPct = hasData ? ((b.lean + 1) / 2) * 100 : 50;
        return (
          <div key={key}>
            <div className="flex items-center justify-between text-sm">
              <span className="flex items-center gap-2 text-ink">
                <Icon /> {label}
              </span>
              <span className={`font-mono text-xs font-semibold ${leanColor(hasData ? b.lean : null)}`}>
                {hasData ? `${leanLabel(b.lean)} · ${b.count} record${b.count === 1 ? "" : "s"}` : "No data"}
              </span>
            </div>
            <div className="relative mt-1.5 h-1.5 rounded-full bg-surface2">
              <div className="absolute inset-y-0 left-1/2 w-px bg-ink-faint/30" />
              {hasData && (
                <div
                  className={`absolute top-1/2 h-2.5 w-2.5 -translate-x-1/2 -translate-y-1/2 rounded-full ${
                    b.lean > 0.05 ? "bg-bull" : b.lean < -0.05 ? "bg-bear" : "bg-ink-faint"
                  }`}
                  style={{ left: `${markerPct}%` }}
                />
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
