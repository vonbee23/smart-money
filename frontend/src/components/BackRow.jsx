import { useNavigate } from "react-router-dom";

export default function BackRow({ label }) {
  const navigate = useNavigate();
  return (
    <button
      type="button"
      onClick={() => navigate(-1)}
      className="flex items-center gap-1 px-4 pb-1 pt-4 text-sm text-ink-muted"
    >
      <span aria-hidden>←</span> {label}
    </button>
  );
}
