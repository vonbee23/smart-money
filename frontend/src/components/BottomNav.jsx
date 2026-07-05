import { NavLink } from "react-router-dom";
import { IconBolt, IconBriefcase, IconChart, IconLandmark, IconStar } from "./icons";

const TABS = [
  { to: "/", label: "Conviction", icon: IconBolt, end: true },
  { to: "/polymarket", label: "Polymarket", icon: IconChart },
  { to: "/insiders", label: "Insiders", icon: IconBriefcase },
  { to: "/congress", label: "Congress", icon: IconLandmark },
  { to: "/watchlist", label: "Watchlist", icon: IconStar },
];

export default function BottomNav() {
  return (
    <nav className="grid grid-cols-5 border-t border-border bg-surface pb-[env(safe-area-inset-bottom)]">
      {TABS.map(({ to, label, icon: Icon, end }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          className={({ isActive }) =>
            `flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium transition-colors ${
              isActive ? "text-teal" : "text-ink-muted"
            }`
          }
        >
          <Icon className="text-[20px]" />
          {label}
        </NavLink>
      ))}
    </nav>
  );
}
