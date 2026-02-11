import axios from "axios";
import { MESSAGE_SERVICE_URL } from "../config";

export async function saveMessage(token: string, text: string): Promise<any> {
  try {
    const response = await axios.post(
      `${MESSAGE_SERVICE_URL}/messages`,
      { text },
      {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
      }
    );

    return response.data;
  } catch (error: any) {
    console.error("Error saving message:", error.response?.data || error.message);
    return null;
  }
}
