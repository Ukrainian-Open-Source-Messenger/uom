import { WebSocket } from "ws";
import { saveMessage } from "../../utils/messages";
import { broadcast } from "../helpers";

export default class ChatMessage {
  static async onChatMessage(ws: WebSocket, data: any) {
    const { text, token } = data;

    if (!text || !token) {
      ws.send(JSON.stringify({ type: "error", message: "Message or token required" }));
      return;
    }

    const savedMessage = await saveMessage(token, text);

    if (!savedMessage?.success) {
      ws.send(JSON.stringify({ type: "error", message: "Failed to save message" }));
      return;
    }

    broadcast({
      type: "message",
      message: savedMessage.message,
    });
  }
}
