import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import type { MessageInfo, AskResponse } from "../../types/api";
import { useChatMessages, useCreateChat, useAddMessage, chatKeys } from "../../hooks/useChats";
import { MessageItem } from "../Message/MessageItem";
import { TypingIndicator } from "../Message/TypingIndicator";
import { ChatInput } from "./ChatInput";
import { Sparkles } from "lucide-react";

interface ChatAreaProps {
  chatId: string | null;
}

export function ChatArea({ chatId }: ChatAreaProps) {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const scrollRef = useRef<HTMLDivElement>(null);
  const [pendingUserContent, setPendingUserContent] = useState<string | null>(null);
  const [pendingAnswer, setPendingAnswer] = useState<string | null>(null);

  const { data: messagesData, isLoading: messagesLoading } =
    useChatMessages(chatId);

  const createChat = useCreateChat();
  const addMessage = useAddMessage(chatId ?? "");

  const messages = messagesData?.messages ?? [];

  const seedSourcesCache = useCallback(
    (response: AskResponse, resolvedChatId: string) => {
      if (response.sources?.length) {
        queryClient.setQueryData(
          chatKeys.sources(resolvedChatId, response.answer_message_id),
          { message_sources: response.sources }
        );
      }
    },
    [queryClient]
  );

  const handleResponse = useCallback(
    (response: AskResponse, newChatId?: string) => {
      const resolvedChatId = newChatId ?? chatId ?? "";
      seedSourcesCache(response, resolvedChatId);
      setPendingAnswer(null);
      setPendingUserContent(null);
      if (newChatId) {
        navigate(`/chats/${newChatId}`, { replace: true });
      }
    },
    [chatId, navigate, seedSourcesCache]
  );

  const handleSend = useCallback(
    async (query: string) => {
      setPendingUserContent(query);
      setPendingAnswer("");

      try {
        if (!chatId) {
          const response = await createChat.mutateAsync({ query });
          setPendingAnswer(response.answer);
          await new Promise((r) => setTimeout(r, 50));
          handleResponse(response, response.chat_id);
        } else {
          const response = await addMessage.mutateAsync({ query });
          setPendingAnswer(response.answer);
          await new Promise((r) => setTimeout(r, 50));
          handleResponse(response);
        }
      } catch {
        setPendingUserContent(null);
        setPendingAnswer(null);
      }
    },
    [chatId, createChat, addMessage, handleResponse]
  );

  useEffect(() => {
    const el = scrollRef.current;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  }, [messages, pendingUserContent, pendingAnswer]);

  const isLoading = createChat.isPending || addMessage.isPending;
  const isEmpty = !chatId && !pendingUserContent;

  if (isEmpty) {
    return (
      <div className="flex flex-col h-full">
        <div className="flex-1 flex flex-col items-center justify-center px-4">
          <div className="w-12 h-12 rounded-2xl bg-accent-dim border border-accent/30 flex items-center justify-center mb-4">
            <Sparkles size={22} className="text-accent" />
          </div>
          <h1 className="text-xl font-semibold text-text-primary mb-1">
            Northstar Knowledge Assistant
          </h1>
          <p className="text-sm text-text-secondary text-center max-w-sm">
            Ask questions about your company's knowledge base. I'll find relevant information and provide cited answers.
          </p>
        </div>
        <ChatInput onSend={handleSend} isLoading={isLoading} />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto flex flex-col gap-6">
          {messagesLoading && chatId && (
            <div className="flex justify-start">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-full bg-accent-dim border border-accent/30 flex items-center justify-center">
                  <Sparkles size={12} className="text-accent" />
                </div>
                <TypingIndicator />
              </div>
            </div>
          )}

          {messages.map((msg: MessageInfo) => {
            if (msg.role === "system") return null;
            return (
              <MessageItem
                key={msg.message_id}
                message={msg}
                chatId={chatId ?? undefined}
              />
            );
          })}

          {pendingUserContent && (
            <>
              <MessageItem
                message={{
                  message_id: "pending-user",
                  role: "user",
                  content: pendingUserContent,
                }}
              />
              {pendingAnswer !== null ? (
                pendingAnswer === "" ? (
                  <div className="flex justify-start animate-fade-in">
                    <div className="flex items-start gap-2.5">
                      <div className="w-7 h-7 rounded-full bg-accent-dim border border-accent/30 flex items-center justify-center mt-0.5">
                        <Sparkles size={12} className="text-accent" />
                      </div>
                      <TypingIndicator />
                    </div>
                  </div>
                ) : (
                  <MessageItem
                    message={{
                      message_id: "pending-answer",
                      role: "assistant",
                      content: pendingAnswer,
                    }}
                  />
                )
              ) : null}
            </>
          )}
        </div>
      </div>

      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  );
}
