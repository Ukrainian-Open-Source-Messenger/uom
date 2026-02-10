import { WebSocket } from 'ws';
import { verifyToken } from './auth';
import { saveMessage } from './messages';
import { broadcast } from './broadcast';

interface Client {
    ws: WebSocket;
    userId: string;
    username: string;
}

export const clients = new Map<string, Client>();

export async function handleWebSocket(ws: WebSocket) {
    let currentClient: Client | null = null;
    let isAuthenticated = false;

    ws.on('message', async (rawMessage: Buffer) => {
        try {
            const data = JSON.parse(rawMessage.toString());

            if (data.type === 'auth') {
                const { token } = data;
                if (!token) return ws.send(JSON.stringify({ type: 'error', message: 'Token is required' }));

                const user = verifyToken(token);
                if (!user) return ws.send(JSON.stringify({ type: 'error', message: 'Invalid token' }));

                currentClient = { ws, userId: user.userId, username: user.username };
                clients.set(user.userId, currentClient);
                isAuthenticated = true;

                ws.send(JSON.stringify({ type: 'auth_success', user }));

                broadcast({ type: 'user_joined', username: user.username, timestamp: Date.now(), onlineUsers: clients.size });
                return;
            }

            if (!isAuthenticated) return ws.send(JSON.stringify({ type: 'error', message: 'Not authenticated' }));

            if (data.type === 'message') {
                const { text, token } = data;
                if (!text || !token) return ws.send(JSON.stringify({ type: 'error', message: 'Message or token required' }));

                const savedMessage = await saveMessage(token, text);
                if (!savedMessage?.success) return ws.send(JSON.stringify({ type: 'error', message: 'Failed to save message' }));

                broadcast({ type: 'message', message: savedMessage.message });
            }

            if (data.type === 'typing') {
                broadcast({ type: 'typing', username: currentClient?.username, isTyping: data.isTyping }, currentClient?.userId);
            }

        } catch (error) {
            console.error('Error handling WS message:', error);
            ws.send(JSON.stringify({ type: 'error', message: 'Internal server error' }));
        }
    });

    ws.on('close', () => {
        if (currentClient) {
            clients.delete(currentClient.userId);
            broadcast({ type: 'user_left', username: currentClient.username, timestamp: Date.now(), onlineUsers: clients.size });
        }
    });

    ws.on('error', (error) => console.error('WebSocket error:', error));

    const pingInterval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) ws.ping();
        else clearInterval(pingInterval);
    }, 30000);
}
