"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.handleWebSocket = handleWebSocket;
const ws_1 = require("ws");
const onAuth_1 = __importDefault(require("./socketEvents/chat/onAuth"));
const onChatMessage_1 = __importDefault(require("./socketEvents/chat/onChatMessage"));
const onTyping_1 = require("./socketEvents/chat/onTyping");
const clients_1 = require("./clients");
const helpers_1 = require("./socketEvents/helpers");
async function handleWebSocket(ws) {
    let currentClient = null;
    let isAuthenticated = false;
    ws.on("message", async (rawMessage) => {
        try {
            const data = JSON.parse(rawMessage.toString());
            switch (data.type) {
                case "auth": {
                    const result = await onAuth_1.default.onAuthUser(ws, data);
                    if (result.success && result.client) {
                        currentClient = result.client;
                        isAuthenticated = true;
                    }
                    break;
                }
                default:
                    if (!isAuthenticated) {
                        ws.send(JSON.stringify({ type: "error", message: "Not authenticated" }));
                        return;
                    }
                    if (data.type === "message") {
                        await onChatMessage_1.default.onChatMessage(ws, data);
                    }
                    if (data.type === "typing") {
                        (0, onTyping_1.onTyping)(currentClient?.userId, currentClient?.username, data);
                    }
            }
        }
        catch (error) {
            console.error("Error handling WS message:", error);
            ws.send(JSON.stringify({ type: "error", message: "Internal server error" }));
        }
    });
    ws.on("close", () => {
        if (currentClient) {
            clients_1.clients.delete(currentClient.userId);
            (0, helpers_1.broadcast)({
                type: "user_left",
                username: currentClient.username,
                timestamp: Date.now(),
                onlineUsers: clients_1.clients.size,
            });
        }
    });
    ws.on("error", (error) => console.error("WebSocket error:", error));
    const pingInterval = setInterval(() => {
        if (ws.readyState === ws_1.WebSocket.OPEN)
            ws.ping();
        else
            clearInterval(pingInterval);
    }, 30000);
}
