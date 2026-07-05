import { IconInbox } from "./icons";

export default function EmptyState({ title = "Nothing here yet", subtitle }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 px-8 py-20 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-full bg-surface text-2xl text-ink-faint">
        <IconInbox />
      </div>
      <p className="font-medium text-ink">{title}</p>
      {subtitle && <p className="max-w-xs text-sm text-ink-muted">{subtitle}</p>}
    </div>
  );
}
