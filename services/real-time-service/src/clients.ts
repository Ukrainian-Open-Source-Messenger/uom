import { WebSocket } from "ws";

export interface Client {
  ws: WebSocket;
  userId: string;
  username: string;
}

export const clients = new Map<string, Client>();
