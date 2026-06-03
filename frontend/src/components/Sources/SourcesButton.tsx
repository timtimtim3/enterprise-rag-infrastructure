import { useState } from "react";
import { Quote, ChevronDown, ChevronUp, Loader2 } from "lucide-react";
import { useMessageSources } from "../../hooks/useChats";
import { SourceCard } from "./SourceCard";

interface SourcesButtonProps {
  chatId: string;
  messageId: string;
}

export function SourcesButton({ chatId, messageId }: SourcesButtonProps) {
  const [open, setOpen] = useState(false);
  const [fetchEnabled, setFetchEnabled] = useState(false);

  const { data, isLoading, isError } = useMessageSources(
    chatId,
    messageId,
    fetchEnabled
  );

  const sources = data?.message_sources ?? [];

  function handleClick() {
    if (!fetchEnabled) setFetchEnabled(true);
    setOpen((v) => !v);
  }

  const hasSources = sources.length > 0;
  const showEmpty = fetchEnabled && !isLoading && !isError && !hasSources;

  return (
    <div className="mt-2.5">
      <button
        onClick={handleClick}
        className={`flex items-center gap-1.5 text-2xs rounded-md px-2 py-1 border transition-colors ${
          open
            ? "text-accent border-accent/30 bg-accent-dim"
            : "text-text-muted border-border-subtle hover:text-accent hover:border-accent/30 hover:bg-accent-dim"
        }`}
      >
        {isLoading ? (
          <Loader2 size={11} className="animate-spin" />
        ) : (
          <Quote size={11} />
        )}
        <span>Sources</span>
        {hasSources && (
          <span className="font-mono tabular-nums">{sources.length}</span>
        )}
        {open ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
      </button>

      {open && (
        <div className="mt-2 flex flex-col gap-1.5 animate-fade-in">
          {isLoading && (
            <p className="text-2xs text-text-muted px-1">Loading sources…</p>
          )}
          {isError && (
            <p className="text-2xs text-red-400 px-1">Failed to load sources.</p>
          )}
          {showEmpty && (
            <p className="text-2xs text-text-muted px-1">No sources found.</p>
          )}
          {sources.map((source, i) => (
            <SourceCard key={source.doc_id + i} source={source} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}
