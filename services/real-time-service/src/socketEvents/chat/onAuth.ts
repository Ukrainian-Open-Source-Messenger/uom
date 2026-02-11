import { WebSocket } from "ws";
import { verifyToken } from "../../utils/auth";
import { broadcast } from "../helpers";
import { clients, Client } from "../../clients";

export default class Auth {
  static async onAuthUser(ws: WebSocket, data: any): Promise<{ success: boolean; client?: Client }> {
    const { token } = data;

    if (!token) {
      ws.send(JSON.stringify({ type: "error", message: "Token is required" }));
      return { success: false };
    }

    const user = verifyToken(token);
    if (!user) {
      ws.send(JSON.stringify({ type: "error", message: "Invalid token" }));
      return { success: false };
    }

    const client: Client = {
      ws,
      userId: user.userId,
      username: user.username,
    };

    clients.set(user.userId, client);

    ws.send(JSON.stringify({ type: "auth_success", user }));

    broadcast({
      type: "user_joined",
      username: user.username,
      timestamp: Date.now(),
      onlineUsers: clients.size,
    });

    return { success: true, client };
  }
}
