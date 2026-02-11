import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Message, User } from "../types";
import { verifyToken, loadMessageHistory } from "@/main/chat/api";
import { createWebSocket } from "@/main/chat/websocket";

export function useChat() {
  const router = useRouter();
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [error, setError] = useState('');
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const savedToken = localStorage.getItem('chat_token');
    if (savedToken) initChat(savedToken);
    else router.push('/login');
  }, []);

  const initChat = async (savedToken: string) => {
    try {
      const data = await verifyToken(savedToken);
      setToken(savedToken);
      setUser(data.user);
      const history = await loadMessageHistory(savedToken);
      setMessages(history);

      const socket = createWebSocket(
        savedToken,
        data.user,
        (msg) => setMessages((prev) => prev.some(m => m.id === msg.id) ? prev : [...prev, msg]),
        (username) => console.log(`${username} joined`),
        (username) => console.log(`${username} left`),
        () => setIsConnected(true),
        (msg) => setError(msg)
      );
      setWs(socket);
    } catch {
      localStorage.removeItem('chat_token');
      router.push('/login');
    }
  };

  const sendMessage = (text: string) => {
    if (!ws || ws.readyState !== WebSocket.OPEN || !token) return;
    ws.send(JSON.stringify({ type: 'message', text, token }));
  };

  const logout = () => {
    ws?.close();
    setWs(null);
    setToken(null);
    setUser(null);
    setMessages([]);
    setIsConnected(false);
    localStorage.removeItem('chat_token');
    router.push('/login');
  };

  return {
    user,
    messages,
    inputMessage: '',
    setInputMessage: () => {},
    sendMessage,
    logout,
    isConnected,
    error,
    isLoadingHistory,
    messagesEndRef
  };
}
