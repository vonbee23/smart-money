import { IconArrowDown, IconArrowUp, IconMinus } from "./icons";

const CONFIG = {
  bullish: { Icon: IconArrowUp, className: "text-bull" },
  bearish: { Icon: IconArrowDown, className: "text-bear" },
  neutral: { Icon: IconMinus, className: "text-ink-faint" },
};

export default function DirectionBadge({ direction, className = "" }) {
  const { Icon, className: color } = CONFIG[direction] || CONFIG.neutral;
  return <Icon className={`${color} ${className}`} />;
}
