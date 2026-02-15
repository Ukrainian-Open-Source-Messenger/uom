"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const http_1 = __importDefault(require("http"));
const ws_1 = require("ws");
const webSocketServer_1 = require("./webSocketServer");
const config_1 = require("./config");
const server = http_1.default.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', service: 'real-time-service' }));
    }
    else {
        res.writeHead(404);
        res.end();
    }
});
const wss = new ws_1.WebSocketServer({ server });
wss.on('connection', webSocketServer_1.handleWebSocket);
server.listen(config_1.PORT, () => {
    console.log(`Real-time Service running on http://localhost:${config_1.PORT}`);
    console.log(`WebSocket available on ws://localhost:${config_1.PORT}`);
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
