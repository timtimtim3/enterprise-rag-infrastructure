import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import type { MessageInfo } from "../../types/api";
import { SourcesButton } from "../Sources/SourcesButton";
import { User, Sparkles } from "lucide-react";

interface MessageItemProps {
  message: MessageInfo;
  chatId?: string;
}

const PENDING_ID_PREFIX = "pending-";

export function MessageItem({ message, chatId }: MessageItemProps) {
  const isUser = message.role === "user";
  const isPending = message.message_id.startsWith(PENDING_ID_PREFIX);

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-in">
        <div className="flex items-start gap-2.5 max-w-[75%]">
          <div className="bg-bg-elevated border border-border rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm text-text-primary leading-relaxed">
            {message.content}
          </div>
          <div className="flex-shrink-0 w-7 h-7 rounded-full bg-bg-elevated border border-border flex items-center justify-center mt-0.5">
            <User size={13} className="text-text-secondary" />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start animate-fade-in">
      <div className="flex items-start gap-2.5 max-w-[85%]">
        <div className="flex-shrink-0 w-7 h-7 rounded-full bg-accent-dim border border-accent/30 flex items-center justify-center mt-0.5">
          <Sparkles size={12} className="text-accent" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="prose-chat text-sm">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || "");
                  const isInline = !match;
                  return isInline ? (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  ) : (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      customStyle={{
                        margin: 0,
                        borderRadius: "0.5rem",
                        fontSize: "0.8rem",
                        background: "#13131a",
                      }}
                    >
                      {String(children).replace(/\n$/, "")}
                    </SyntaxHighlighter>
                  );
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>

          {!isPending && chatId && message.route === "rag" && (
            <SourcesButton chatId={chatId} messageId={message.message_id} />
          )}
        </div>
      </div>
    </div>
  );
}
