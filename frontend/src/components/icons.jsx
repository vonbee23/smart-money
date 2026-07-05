const base = {
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round",
  strokeLinejoin: "round",
};

export function IconBolt(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M13 2 3 14h7l-1 8 10-12h-7l1-8Z" />
    </svg>
  );
}

export function IconChart(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M3 3v18h18" />
      <path d="M7 15l4-5 3 3 5-7" />
    </svg>
  );
}

export function IconBriefcase(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <rect x="2.5" y="7" width="19" height="13" rx="2" />
      <path d="M8 7V5.5A1.5 1.5 0 0 1 9.5 4h5A1.5 1.5 0 0 1 16 5.5V7" />
      <path d="M2.5 12h19" />
    </svg>
  );
}

export function IconLandmark(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M3 21h18" />
      <path d="M4 21V10M9 21V10M15 21V10M20 21V10" />
      <path d="M2 10l10-6 10 6" />
    </svg>
  );
}

export function IconStar({ filled, ...props }) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} fill={filled ? "currentColor" : "none"} {...props}>
      <path d="m12 2.5 2.9 6.4 6.9.7-5.2 4.7 1.5 6.9L12 17.6l-6.1 3.6 1.5-6.9-5.2-4.7 6.9-.7L12 2.5Z" strokeLinejoin="round" />
    </svg>
  );
}

export function IconRefresh(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M3 12a9 9 0 0 1 15.4-6.4L21 8" />
      <path d="M21 3v5h-5" />
      <path d="M21 12a9 9 0 0 1-15.4 6.4L3 16" />
      <path d="M3 21v-5h5" />
    </svg>
  );
}

export function IconArrowUp(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M12 19V5" />
      <path d="m5 12 7-7 7 7" />
    </svg>
  );
}

export function IconArrowDown(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M12 5v14" />
      <path d="m19 12-7 7-7-7" />
    </svg>
  );
}

export function IconMinus(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M5 12h14" />
    </svg>
  );
}

export function IconChevronRight(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="m9 6 6 6-6 6" />
    </svg>
  );
}

export function IconInbox(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" {...base} {...props}>
      <path d="M3 12h4l2 3h6l2-3h4" />
      <path d="M5 5h14l2 7v7a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-7l2-7Z" />
    </svg>
  );
}
