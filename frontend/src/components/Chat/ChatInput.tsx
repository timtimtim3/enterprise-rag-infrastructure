import { useState, useRef, useCallback, type KeyboardEvent } from "react";
import { ArrowUp } from "lucide-react";

interface ChatInputProps {
  onSend: (query: string) => void;
  isLoading: boolean;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({
  onSend,
  isLoading,
  disabled,
  placeholder = "Ask anything...",
}: ChatInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const adjustHeight = useCallback(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";
  }, []);

  const handleSend = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || isLoading || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  }, [value, isLoading, disabled, onSend]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    },
    [handleSend]
  );

  const canSend = value.trim().length > 0 && !isLoading && !disabled;

  return (
    <div className="px-4 py-3 border-t border-border-subtle bg-bg-base">
      <div className="max-w-3xl mx-auto">
        <div className="relative flex items-end gap-2 bg-bg-surface border border-border rounded-xl p-2 focus-within:border-border-strong transition-colors">
          <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => {
              setValue(e.target.value);
              adjustHeight();
            }}
            onKeyDown={handleKeyDown}
            disabled={disabled || isLoading}
            placeholder={placeholder}
            rows={1}
            className="flex-1 resize-none bg-transparent text-sm text-text-primary placeholder:text-text-muted outline-none px-2 py-1.5 min-h-[36px] max-h-[200px] leading-relaxed disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={!canSend}
            aria-label="Send message"
            className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center transition-all disabled:opacity-30 disabled:cursor-not-allowed bg-accent hover:bg-accent-hover disabled:bg-bg-elevated"
          >
            {isLoading ? (
              <span className="w-3.5 h-3.5 rounded-sm bg-text-inverse opacity-70" />
            ) : (
              <ArrowUp size={15} className="text-text-inverse" />
            )}
          </button>
        </div>
        <p className="text-center text-2xs text-text-muted mt-2">
          Enter to send · Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
