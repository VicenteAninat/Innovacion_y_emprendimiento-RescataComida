import { useState } from "react";
import { Search } from "lucide-react";

export default function SearchBar({
  placeholder = "Buscar restaurantes...",
}: {
  placeholder?: string;
}) {
  const [value, setValue] = useState("");
  return (
    <div className="flex items-center gap-3 bg-card rounded-2xl px-4 h-12 border border-border">
      <Search size={18} className="text-muted-foreground shrink-0" />
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={placeholder}
        className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none"
      />
    </div>
  );
}
