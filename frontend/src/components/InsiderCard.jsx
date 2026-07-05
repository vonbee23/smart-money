import { formatDate, formatMoney } from "../lib/format";

export default function InsiderCard({ filing }) {
  const isBuy = filing.transaction_type === "buy";
  return (
    <div className="rounded-2xl border border-border bg-surface p-4 shadow-lg shadow-black/20">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-baseline gap-2">
            <span className="font-mono text-sm font-semibold text-ink">{filing.ticker}</span>
            <span className="truncate text-sm text-ink-muted">{filing.company}</span>
          </div>
          <p className="mt-1 text-sm text-ink">
            {filing.insider_name}
            {filing.role && <span className="text-ink-muted"> · {filing.role}</span>}
          </p>
        </div>
        <span
          className={`shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold ${
            isBuy ? "bg-bull-dim text-bull" : "bg-bear-dim text-bear"
          }`}
        >
          {isBuy ? "BUY" : "SELL"}
        </span>
      </div>

      <div className="mt-3 flex items-center justify-between font-mono text-sm">
        <span className="text-ink-muted">{formatDate(filing.filing_date)}</span>
        <span className={`font-semibold ${isBuy ? "text-bull" : "text-bear"}`}>{formatMoney(filing.value)}</span>
      </div>
    </div>
  );
}
