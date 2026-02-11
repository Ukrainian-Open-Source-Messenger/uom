import { WebSocket } from "ws";
import Auth from "./socketEvents/chat/onAuth";
import ChatMessage from "./socketEvents/chat/onChatMessage";
import { onTyping } from "./socketEvents/chat/onTyping";
import { clients, Client } from "./clients";
import { broadcast } from "./socketEvents/helpers";

export async function handleWebSocket(ws: WebSocket) {
  let currentClient: Client | null = null;
  let isAuthenticated = false;

  ws.on("message", async (rawMessage: Buffer) => {
    try {
      const data = JSON.parse(rawMessage.toString());

      switch (data.type) {
        case "auth": {
          const result = await Auth.onAuthUser(ws, data);
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
            await ChatMessage.onChatMessage(ws, data);
          }

          if (data.type === "typing") {
            onTyping(
              currentClient?.userId,
              currentClient?.username,
              data
            );
          }
      }
    } catch (error) {
      console.error("Error handling WS message:", error);
      ws.send(JSON.stringify({ type: "error", message: "Internal server error" }));
    }
  });

  ws.on("close", () => {
    if (currentClient) {
      clients.delete(currentClient.userId);

      broadcast({
        type: "user_left",
        username: currentClient.username,
        timestamp: Date.now(),
        onlineUsers: clients.size,
      });
    }
  });

  ws.on("error", (error) =>
    console.error("WebSocket error:", error)
  );

  const pingInterval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) ws.ping();
    else clearInterval(pingInterval);
  }, 30000);
}
