import { useNavigate, useParams } from "react-router-dom";
import { SquarePen, Star, LogOut } from "lucide-react";
import { useChatList, useDeleteChat } from "../../hooks/useChats";
import { ChatListItem } from "./ChatListItem";
import { useAuth } from "../../contexts/useAuth";

export function Sidebar() {
  const navigate = useNavigate();
  const { chatId } = useParams<{ chatId: string }>();
  const { data, isLoading } = useChatList();
  const deleteChat = useDeleteChat();
  const { user, logout } = useAuth();

  const chats = data?.chats ?? [];

  function handleDelete(id: string) {
    deleteChat.mutate(id, {
      onSuccess: () => {
        if (chatId === id) navigate("/chats");
      },
    });
  }

  return (
    <aside className="w-[260px] flex-shrink-0 flex flex-col h-full bg-bg-sidebar border-r border-border-subtle">
      <div className="flex items-center gap-2.5 px-4 py-4 border-b border-border-subtle">
        <div className="w-7 h-7 rounded-lg bg-accent-dim border border-accent/30 flex items-center justify-center">
          <Star size={13} className="text-accent fill-accent" />
        </div>
        <span className="text-sm font-semibold text-text-primary tracking-tight">
          Northstar
        </span>
      </div>

      <div className="px-3 py-3">
        <button
          onClick={() => navigate("/chats")}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-xs text-text-secondary hover:text-text-primary hover:bg-bg-hover transition-colors border border-border-subtle hover:border-border"
        >
          <SquarePen size={13} />
          <span>New chat</span>
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-3 pb-3">
        {isLoading ? (
          <div className="flex flex-col gap-1.5 mt-1">
            {[...Array(4)].map((_, i) => (
              <div
                key={i}
                className="h-8 rounded-lg bg-bg-elevated animate-pulse"
                style={{ opacity: 1 - i * 0.2 }}
              />
            ))}
          </div>
        ) : chats.length === 0 ? (
          <p className="text-xs text-text-muted px-3 py-2">No conversations yet</p>
        ) : (
          <div className="flex flex-col gap-0.5">
            {chats.map((chat) => (
              <ChatListItem
                key={chat.chat_id}
                chat={chat}
                isActive={chatId === chat.chat_id}
                onClick={() => navigate(`/chats/${chat.chat_id}`)}
                onDelete={() => handleDelete(chat.chat_id)}
              />
            ))}
          </div>
        )}
      </div>

      <div className="border-t border-border-subtle px-3 py-3">
        <div className="flex items-center gap-2.5 px-2 py-1.5">
          <div className="w-6 h-6 rounded-full bg-bg-elevated border border-border flex items-center justify-center text-2xs font-semibold text-text-secondary">
            {user?.username?.[0]?.toUpperCase() ?? "?"}
          </div>
          <span className="flex-1 text-xs text-text-secondary truncate">
            {user?.username}
          </span>
          <button
            onClick={async () => {
              await logout();
              navigate("/login");
            }}
            className="w-6 h-6 rounded flex items-center justify-center hover:bg-bg-hover transition-colors"
            aria-label="Sign out"
            title="Sign out"
          >
            <LogOut size={13} className="text-text-muted hover:text-text-secondary" />
          </button>
        </div>
      </div>
    </aside>
  );
}
