'use client';

import { useState, useEffect, useRef } from 'react';

interface Message {
  id: string;
  userId: string;
  username: string;
  text: string;
  timestamp: number;
  edited?: boolean;
}

interface User {
  id: string;
  username: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080/ws';

export default function ChatPage() {
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Перевірка збереженого токену при завантаженні
  useEffect(() => {
    const savedToken = localStorage.getItem('chat_token');
    if (savedToken) {
      verifyToken(savedToken);
    }
  }, []);

  // Верифікація токену
  const verifyToken = async (token: string) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token })
      });

      if (response.ok) {
        const data = await response.json();
        setToken(token);
        setUser(data.user);
        localStorage.setItem('chat_token', token);
        await loadMessageHistory(token);
        connectWebSocket(token, data.user);
      } else {
        localStorage.removeItem('chat_token');
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      localStorage.removeItem('chat_token');
    }
  };

  // Завантаження історії повідомлень
  const loadMessageHistory = async (authToken: string) => {
    setIsLoadingHistory(true);
    try {
      const response = await fetch(`${API_URL}/api/messages/recent?limit=50`, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
      } else {
        console.error('Failed to load message history');
      }
    } catch (error) {
      console.error('Error loading message history:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  // Підключення до WebSocket
  const connectWebSocket = (authToken: string, userData: User) => {
    try {
      const websocket = new WebSocket(WS_URL);

      websocket.onopen = () => {
        console.log('WebSocket з\'єднання встановлено');
        
        websocket.send(JSON.stringify({
          type: 'auth',
          token: authToken
        }));
      };

      websocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Отримано повідомлення:', data.type);

          if (data.type === 'auth_success') {
            console.log('WebSocket аутентифікація успішна');
            setIsConnected(true);
          }

          if (data.type === 'message' && data.message) {
            setMessages((prev) => {
              if (prev.some(m => m.id === data.message.id)) {
                return prev;
              }
              return [...prev, data.message];
            });
          }

          if (data.type === 'user_joined') {
            console.log(`${data.username} приєднався до чату`);
          }

          if (data.type === 'user_left') {
            console.log(`${data.username} покинув чат`);
          }

          if (data.type === 'error') {
            console.error('Помилка від сервера:', data.message);
            setError(data.message || 'Помилка сервера');
            setTimeout(() => setError(''), 5000);
          }
        } catch (parseError) {
          console.error('Помилка парсингу повідомлення:', parseError);
        }
      };

      websocket.onerror = (error) => {
        console.error('WebSocket помилка:', error);
        setError('Помилка з\'єднання з сервером');
        setIsConnected(false);
      };

      websocket.onclose = () => {
        console.log('WebSocket з\'єднання закрито');
        setIsConnected(false);
        
        const reconnectTimeout = setTimeout(() => {
          if (token && user) {
            console.log('Спроба перепідключення...');
            connectWebSocket(token, user);
          }
        }, 3000);

        return () => clearTimeout(reconnectTimeout);
      };

      setWs(websocket);
    } catch (error) {
      console.error('Помилка при підключенні WebSocket:', error);
      setError('Не вдалося підключитися до сервера');
    }
  };

  // Реєстрація/вхід
  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    if (!username.trim() || !password.trim()) {
      setError('Введіть ім\'я користувача та пароль');
      setIsLoading(false);
      return;
    }

    try {
      const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/register';
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        setToken(data.token);
        setUser(data.user);
        localStorage.setItem('chat_token', data.token);
        await loadMessageHistory(data.token);
        connectWebSocket(data.token, data.user);
        setPassword('');
      } else {
        setError(data.error || 'Помилка аутентифікації');
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('Помилка з\'єднання з сервером');
    } finally {
      setIsLoading(false);
    }
  };

  // Відправка повідомлення
  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim()) {
      setError('Повідомлення не може бути пустим');
      setTimeout(() => setError(''), 3000);
      return;
    }

    if (!ws) {
      setError('WebSocket не з\'єднаний');
      setTimeout(() => setError(''), 3000);
      return;
    }

    if (ws.readyState !== WebSocket.OPEN) {
      setError('З\'єднання не встановлено. Спробуйте ще раз...');
      setTimeout(() => setError(''), 3000);
      return;
    }

    if (!isConnected) {
      setError('WebSocket ще не аутентифікований. Спробуйте через секунду...');
      setTimeout(() => setError(''), 3000);
      return;
    }

    try {
      const messageData = {
        type: 'message',
        text: inputMessage.trim(),
        token: token
      };

      console.log('Відправляю повідомлення');
      ws.send(JSON.stringify(messageData));
      setInputMessage('');
    } catch (error) {
      console.error('Помилка відправки повідомлення:', error);
      setError('Не вдалося відправити повідомлення');
      setTimeout(() => setError(''), 3000);
    }
  };

  // Вихід
  const handleLogout = () => {
    if (ws) {
      ws.close();
      setWs(null);
    }
    setToken(null);
    setUser(null);
    setMessages([]);
    setIsConnected(false);
    localStorage.removeItem('chat_token');
  };

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit' });
  };

  // Форма аутентифікації
  if (!token || !user) {
    return (
      <div className="auth-container">
        <div className="auth-form-wrapper">
          <div className="auth-title">
            <h1>
              {authMode === 'login' ? 'Вхід в чат' : 'Реєстрація'}
            </h1>
            <p>
              {authMode === 'login' ? 'Введіть свої дані' : 'Створіть новий акаунт'}
            </p>
          </div>
          
          {error && (
            <div className="error-alert error-alert-auth">
              {error}
            </div>
          )}

          <form onSubmit={handleAuth}>
            <div className="form-group">
              <label htmlFor="username" className="form-label">
                Ім'я користувача
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="form-input"
                placeholder="Введіть ім'я..."
                required
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Пароль
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="Введіть пароль..."
                required
                minLength={6}
              />
            </div>
            
            <button
              type="submit"
              disabled={isLoading}
              className="auth-btn"
            >
              {isLoading ? 'Завантаження...' : authMode === 'login' ? 'Увійти' : 'Зареєструватися'}
            </button>
          </form>

          <div className="auth-toggle">
            <button
              onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
              className="auth-toggle-btn"
            >
              {authMode === 'login' ? 'Немає акаунту? Зареєструватися' : 'Вже є акаунт? Увійти'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Інтерфейс чату
  return (
    <div className="chat-container">
      {/* Заголовок */}
      <header className="chat-header">
        <div className="header-content">
          <div className="header-info">
            <h1>Чат</h1>
            <p>
              Ви увійшли як: <span className="username">{user.username}</span>
            </p>
          </div>
          <div className="header-status">
            <div className="status-indicator">
              <div className={`status-dot ${isConnected ? 'online' : 'offline'}`}></div>
              <span className="status-text">{isConnected ? 'Онлайн' : 'Оффлайн'}</span>
            </div>
            <button
              onClick={handleLogout}
              className="logout-btn"
            >
              Вийти
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="chat-wrapper">
          <div className="error-alert">
            {error}
          </div>
        </div>
      )}

      {/* Повідомлення */}
      <main className="chat-wrapper">
        <div className="messages-container">
          {isLoadingHistory ? (
            <div className="loading-message">
              <p>Завантаження історії...</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="empty-message">
              <p>Поки що немає повідомлень...</p>
              <p className="empty-message-subtitle">Будьте першим, хто напише!</p>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`message-row ${message.userId === user.id ? 'own' : 'other'}`}
                >
                  <div
                    className={`message-bubble ${message.userId === user.id ? 'own' : 'other'}`}
                  >
                    {message.userId !== user.id && (
                      <p className="message-username">
                        {message.username}
                      </p>
                    )}
                    <p className="message-text">{message.text}</p>
                    <p className="message-meta">
                      {formatTime(message.timestamp)}
                      {message.edited && <span className="message-edited"> (редаговано)</span>}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Форма відправки повідомлення */}
        <form onSubmit={handleSendMessage} className="message-form">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            className="message-input"
            placeholder="Напишіть повідомлення..."
            disabled={!isConnected}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || !isConnected}
            className="send-btn"
          >
            Відправити
          </button>
        </form>
      </main>
    </div>
  );
}