import { useParams } from "react-router-dom";
import { ChatArea } from "../components/Chat/ChatArea";

export function ChatsPage() {
  const { chatId } = useParams<{ chatId: string }>();
  return <ChatArea chatId={chatId ?? null} />;
}
