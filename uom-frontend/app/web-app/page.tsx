'use client';

import { useState } from "react";
import { useChat } from "@/hooks/useChat";
import "./chat.css";

export default function ChatPage() {
  const [input, setInput] = useState('');
  const { user, messages, sendMessage, logout, isConnected, error, isLoadingHistory, messagesEndRef } = useChat();

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput('');
  };

  if (!user) return <p>Завантаження...</p>;

  return (
    <div className="chat-container">
      {/* header */}
      <header>
        <h1>Чат</h1>
        <p>Ви увійшли як: {user.username}</p>
        <button onClick={logout}>Вийти</button>
        <p>{isConnected ? 'Онлайн' : 'Оффлайн'}</p>
      </header>

      {error && <div className="error-alert">{error}</div>}

      <main>
        {isLoadingHistory ? <p>Завантаження історії...</p> :
          messages.map(msg => (
            <div key={msg.id}>
              <b>{msg.username}: </b>{msg.text} <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
            </div>
          ))
        }
        <div ref={messagesEndRef} />
      </main>

      <form onSubmit={handleSend}>
        <input value={input} onChange={(e) => setInput(e.target.value)} disabled={!isConnected} />
        <button type="submit" disabled={!input.trim() || !isConnected}>Відправити</button>
      </form>
    </div>
  );
}
