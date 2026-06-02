import { useState } from "react";
import { ChevronDown, ChevronUp, BookOpen } from "lucide-react";
import { SourceCard } from "./SourceCard";
import type { MessageSourceInfo, Source } from "../../types/api";

type SourcesListProps = {
  sources: (MessageSourceInfo | Source)[];
};

export function SourcesList({ sources }: SourcesListProps) {
  const [expanded, setExpanded] = useState(false);

  if (!sources.length) return null;

  const visible = expanded ? sources : sources.slice(0, 3);

  return (
    <div className="mt-3 pt-3 border-t border-border-subtle">
      <button
        onClick={() => setExpanded((v) => !v)}
        className="flex items-center gap-1.5 text-2xs text-text-secondary hover:text-text-primary transition-colors mb-2 group"
      >
        <BookOpen size={11} className="text-text-muted" />
        <span>
          {sources.length} source{sources.length !== 1 ? "s" : ""}
        </span>
        {sources.length > 3 &&
          (expanded ? (
            <ChevronUp size={11} className="text-text-muted" />
          ) : (
            <ChevronDown size={11} className="text-text-muted" />
          ))}
      </button>

      <div className="flex flex-col gap-1.5">
        {visible.map((source, i) => (
          <SourceCard key={source.doc_id + i} source={source} index={i} />
        ))}
      </div>

      {!expanded && sources.length > 3 && (
        <button
          onClick={() => setExpanded(true)}
          className="mt-1.5 text-2xs text-text-muted hover:text-text-secondary transition-colors"
        >
          +{sources.length - 3} more
        </button>
      )}
    </div>
  );
}
