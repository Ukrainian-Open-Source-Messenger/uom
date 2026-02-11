import { Message, User } from "@/types";
import Config from "../config";

export function createWebSocket(
  token: string,
  user: User,
  onMessage: (message: Message) => void,
  onUserJoined: (username: string) => void,
  onUserLeft: (username: string) => void,
  onAuthSuccess: () => void,
  onError: (msg: string) => void
): WebSocket {
  const ws = new WebSocket(Config.PUBLIC_API_URL_WS_GETEWAY);

  ws.onopen = () => {
    ws.send(JSON.stringify({ type: 'auth', token }));
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.type === 'auth_success') onAuthSuccess();
      if (data.type === 'message' && data.message) onMessage(data.message);
      if (data.type === 'user_joined') onUserJoined(data.username);
      if (data.type === 'user_left') onUserLeft(data.username);
      if (data.type === 'error') onError(data.message || 'Server error');
    } catch (err) {
      onError('WebSocket parse error');
    }
  };

  ws.onerror = () => onError('WebSocket error');
  ws.onclose = () => console.log('WebSocket closed');

  return ws;
}
