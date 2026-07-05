import { useData } from "../lib/DataContext";
import { IconRefresh } from "./icons";

export default function Header() {
  const { refresh, refreshing } = useData();

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-border bg-bg/95 px-4 py-3 backdrop-blur">
      <h1 className="text-lg font-semibold tracking-tight text-ink">
        Smart <span className="text-teal">Money</span>
      </h1>
      <button
        type="button"
        onClick={refresh}
        disabled={refreshing}
        aria-label="Refresh data"
        className="flex h-10 w-10 items-center justify-center rounded-full border border-border bg-surface text-ink-muted transition active:scale-95 disabled:opacity-60"
      >
        <IconRefresh className={refreshing ? "animate-spin" : ""} />
      </button>
    </header>
  );
}
