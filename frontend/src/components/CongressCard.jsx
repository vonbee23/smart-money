import { formatDate } from "../lib/format";

const TYPE_STYLE = {
  buy: "bg-bull-dim text-bull",
  sell: "bg-bear-dim text-bear",
  exchange: "bg-surface2 text-ink-muted",
};

export default function CongressCard({ trade }) {
  return (
    <div className="rounded-2xl border border-border bg-surface p-4 shadow-lg shadow-black/20">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-sm font-medium text-ink">{trade.representative}</p>
          <p className="text-xs text-ink-muted capitalize">
            {trade.chamber}
            {trade.party ? ` · ${trade.party}` : ""}
          </p>
        </div>
        <span className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold ${TYPE_STYLE[trade.transaction_type]}`}>
          {trade.transaction_type.toUpperCase()}
        </span>
      </div>

      <div className="mt-3 flex items-center gap-2">
        <span className="font-mono text-sm font-semibold text-ink">{trade.ticker}</span>
        <span className="font-mono text-sm text-ink-muted">{trade.amount_range}</span>
      </div>

      <div className="mt-2 flex items-center justify-between font-mono text-xs text-ink-faint">
        <span>Traded {formatDate(trade.transaction_date)}</span>
        <span>Disclosed {formatDate(trade.disclosure_date)}</span>
      </div>
    </div>
  );
}
