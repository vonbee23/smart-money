import { Link } from "react-router-dom";
import DirectionBadge from "./DirectionBadge";
import SignalIcons from "./SignalIcons";
import WatchButton from "./WatchButton";

export default function TickerCard({ entry }) {
  return (
    <Link
      to={`/ticker/${entry.ticker}`}
      className="flex items-center gap-3 rounded-2xl border border-border bg-surface p-4 shadow-lg shadow-black/20 transition active:scale-[0.98]"
    >
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <span className="font-mono text-base font-semibold text-ink">{entry.ticker}</span>
          {entry.high_conviction && (
            <span className="text-sm" title="High conviction: all 3 sources agree">
              ⚡
            </span>
          )}
        </div>
        <p className="truncate text-sm text-ink-muted">{entry.company}</p>
        <div className="mt-2">
          <SignalIcons sourcesPresent={entry.sources_present} />
        </div>
      </div>

      <div className="flex flex-col items-end gap-1">
        <div className="flex items-center gap-1">
          <DirectionBadge direction={entry.direction} />
          <span className="font-mono text-2xl font-bold tabular-nums text-ink">{entry.score.toFixed(0)}</span>
        </div>
        <WatchButton ticker={entry.ticker} size="sm" />
      </div>
    </Link>
  );
}
