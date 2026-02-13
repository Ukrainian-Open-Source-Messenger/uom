"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { registerRequest, saveToken } from "@/main/auth/auth";
import { validateRegister } from "@/main/auth/validation";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    const validationError = validateRegister(username, password, email);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);

    try {
      const data = await registerRequest(username, password, email);

      saveToken(data.token);
      router.replace("/web-app");
    } catch (err: any) {
      setError(err.message || "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>Реєстрація</h1>

      {error && <div>{error}</div>}

      <form onSubmit={handleRegister}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Ім'я користувача"
        />

        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Пошта"
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Пароль (мінімум 6 символів)"
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Завантаження..." : "Зареєструватися"}
        </button>
      </form>

      <Link href="/auth/login">Вже є акаунт? Увійти</Link>
    </div>
  );
}
