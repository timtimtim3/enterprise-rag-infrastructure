import { useState, useRef, useEffect } from "react";
import { MessageSquare, Trash2 } from "lucide-react";
import type { ChatInfo } from "../../types/api";

interface ChatListItemProps {
  chat: ChatInfo;
  isActive: boolean;
  onClick: () => void;
  onDelete: () => void;
}

export function ChatListItem({
  chat,
  isActive,
  onClick,
  onDelete,
}: ChatListItemProps) {
  const [showDelete, setShowDelete] = useState(false);
  const itemRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isActive) setShowDelete(false);
  }, [isActive]);

  return (
    <div
      ref={itemRef}
      onMouseEnter={() => setShowDelete(true)}
      onMouseLeave={() => setShowDelete(false)}
      className={`group relative flex items-center gap-2.5 px-3 py-2 rounded-lg cursor-pointer transition-colors text-sm ${
        isActive
          ? "bg-bg-elevated text-text-primary"
          : "text-text-secondary hover:bg-bg-hover hover:text-text-primary"
      }`}
      onClick={onClick}
    >
      <MessageSquare
        size={13}
        className={`flex-shrink-0 ${isActive ? "text-accent" : "text-text-muted group-hover:text-text-secondary"}`}
      />
      <span className="flex-1 truncate text-xs leading-5">
        {chat.title ?? "New conversation"}
      </span>

      {showDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
          className="flex-shrink-0 w-5 h-5 rounded flex items-center justify-center hover:bg-bg-surface transition-colors"
          aria-label="Delete chat"
        >
          <Trash2 size={11} className="text-text-muted hover:text-red-400" />
        </button>
      )}
    </div>
  );
}
