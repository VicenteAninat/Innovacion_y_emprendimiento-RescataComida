export default function SectionHeader({
  title,
  action,
  onAction,
}: {
  title: string;
  action?: string;
  onAction?: () => void;
}) {
  return (
    <div className="flex items-center justify-between px-5 mb-3">
      <h2
        className="font-bold text-base text-foreground"
        style={{ fontFamily: "'Righteous', sans-serif" }}
      >
        {title}
      </h2>
      {action && (
        <button
          onClick={onAction}
          className="text-xs text-primary font-semibold"
        >
          {action}
        </button>
      )}
    </div>
  );
}
