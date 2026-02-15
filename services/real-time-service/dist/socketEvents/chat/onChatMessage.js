"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const messages_1 = require("../../utils/messages");
const helpers_1 = require("../helpers");
class ChatMessage {
    static async onChatMessage(ws, data) {
        const { text, token } = data;
        if (!text || !token) {
            ws.send(JSON.stringify({ type: "error", message: "Message or token required" }));
            return;
        }
        const savedMessage = await (0, messages_1.saveMessage)(token, text);
        if (!savedMessage?.success) {
            ws.send(JSON.stringify({ type: "error", message: "Failed to save message" }));
            return;
        }
        (0, helpers_1.broadcast)({
            type: "message",
            message: savedMessage.message,
        });
    }
}
exports.default = ChatMessage;
