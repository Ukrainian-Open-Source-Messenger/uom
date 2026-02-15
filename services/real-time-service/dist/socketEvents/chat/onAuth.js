"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const auth_1 = require("../../utils/auth");
const helpers_1 = require("../helpers");
const clients_1 = require("../../clients");
class Auth {
    static async onAuthUser(ws, data) {
        const { token } = data;
        if (!token) {
            ws.send(JSON.stringify({ type: "error", message: "Token is required" }));
            return { success: false };
        }
        const user = (0, auth_1.verifyToken)(token);
        if (!user) {
            ws.send(JSON.stringify({ type: "error", message: "Invalid token" }));
            return { success: false };
        }
        const client = {
            ws,
            userId: user.userId,
            username: user.username,
        };
        clients_1.clients.set(user.userId, client);
        ws.send(JSON.stringify({ type: "auth_success", user }));
        (0, helpers_1.broadcast)({
            type: "user_joined",
            username: user.username,
            timestamp: Date.now(),
            onlineUsers: clients_1.clients.size,
        });
        return { success: true, client };
    }
}
exports.default = Auth;
