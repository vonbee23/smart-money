import { IconBriefcase, IconChart, IconLandmark } from "./icons";

const SIGNALS = [
  { key: "congress", Icon: IconLandmark, label: "Congress" },
  { key: "insiders", Icon: IconBriefcase, label: "Insiders" },
  { key: "polymarket", Icon: IconChart, label: "Polymarket" },
];

export default function SignalIcons({ sourcesPresent = [] }) {
  return (
    <div className="flex items-center gap-1.5">
      {SIGNALS.map(({ key, Icon, label }) => {
        const active = sourcesPresent.includes(key);
        return (
          <span
            key={key}
            title={`${label}${active ? " signal" : " — no data"}`}
            className={`flex h-5 w-5 items-center justify-center rounded-full text-[11px] ${
              active ? "bg-teal-dim text-teal" : "bg-surface2 text-ink-faint/50"
            }`}
          >
            <Icon />
          </span>
        );
      })}
    </div>
  );
}
