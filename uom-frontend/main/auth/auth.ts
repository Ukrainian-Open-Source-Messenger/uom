import axios from "@/lib/axios";
import Config from "@/main/config";

export interface AuthResponse {
  token: string;
  error?: string;
}

export async function loginRequest(username: string, password: string): Promise<AuthResponse> {
  try {
    const { data } = await axios.post(
      `${Config.PUBLIC_API_URL_GETEWAY}/api/auth/login`,
      { username, password },
      {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      }
    );
    return data;
  } catch (err: any) {
    if (err.response && err.response.data?.error) {
      throw new Error(err.response.data.error);
    }
    throw new Error("Помилка входу");
  }
}

export async function registerRequest(username: string, password: string): Promise<AuthResponse> {
  try {
    const { data } = await axios.post(
      `${Config.PUBLIC_API_URL_GETEWAY}/api/auth/register`,
      { username, password },
      {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      }
    );
    return data;
  } catch (err: any) {
    if (err.response && err.response.data?.error) {
      throw new Error(err.response.data.error);
    }
    throw new Error("Помилка реєстрації");
  }
}

// tockem
export function saveToken(token: string) {
  localStorage.setItem("chat_token", token);
};

export function removeToken() {
  localStorage.removeItem("chat_token");
};

export function getToken() {
  return localStorage.getItem("chat_token");
};
