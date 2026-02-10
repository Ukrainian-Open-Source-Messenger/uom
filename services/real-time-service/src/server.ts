import http from 'http';
import { WebSocketServer, WebSocket } from 'ws';
import { handleWebSocket } from './clients';

export function startServer(PORT: number) {
    const server = http.createServer((req, res) => {
        if (req.url === '/health') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'ok', service: 'real-time-service' }));
        } else {
            res.writeHead(404);
            res.end();
        }
    });

    const wss = new WebSocketServer({ server });
    wss.on('connection', handleWebSocket);

    server.listen(PORT, () => {
        console.log(`Real-time Service running on http://localhost:${PORT}`);
        console.log(`WebSocket available on ws://localhost:${PORT}`);
    });

    // Graceful shutdown
    process.on('SIGTERM', () => {
        console.log('SIGTERM received, closing server...');
        wss.clients.forEach(ws => ws.close());
        server.close(() => {
            console.log('Server closed');
            process.exit(0);
        });
    });
}
