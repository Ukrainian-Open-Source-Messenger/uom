import axios from "@/lib/axios";
import { Message, User } from "@/types";
import Config from "../config";

export async function verifyToken(token: string): Promise<{ user: User }> {
  const response = await axios.post(`${Config.PUBLIC_API_URL_GETEWAY}/api/auth/verify`, { token });
  return response.data;
}

export async function loadMessageHistory(token: string): Promise<Message[]> {
  const response = await axios.get(`${Config.PUBLIC_API_URL_GETEWAY}/api/messages/recent?limit=50`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data.messages || [];
}
