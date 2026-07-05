import { useWatchlist } from "../hooks/useWatchlist";
import { IconStar } from "./icons";

export default function WatchButton({ ticker, size = "md" }) {
  const { isWatched, toggle } = useWatchlist();
  const watched = isWatched(ticker);
  const dim = size === "sm" ? "h-8 w-8 text-base" : "h-10 w-10 text-lg";

  return (
    <button
      type="button"
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        toggle(ticker);
      }}
      aria-label={watched ? `Remove ${ticker} from watchlist` : `Add ${ticker} to watchlist`}
      aria-pressed={watched}
      className={`flex ${dim} shrink-0 items-center justify-center rounded-full transition active:scale-90 ${
        watched ? "text-teal" : "text-ink-faint"
      }`}
    >
      <IconStar filled={watched} />
    </button>
  );
}
