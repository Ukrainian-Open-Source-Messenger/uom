'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from "next/link";
import { loginRequest, saveToken } from "@/main/auth/auth";
import { validateLogin } from "@/main/auth/validation";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError('');

    const validationError = validateLogin(username, password, email);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);

    try {
      const data = await loginRequest(username, password, email);

      saveToken(data.token);
      router.replace('/web-app');
    } catch (err: any) {
      setError(err.message || "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1>Вхід в чат</h1>

      {error && <div>{error}</div>}

      <form onSubmit={handleLogin}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Ім'я"
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
          placeholder="Пароль"
        />

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Завантаження...' : 'Увійти'}
        </button>
      </form>

      <Link href="/auth/register">
        Немає акаунту? Зареєструватися
      </Link>
    </div>
  );
}
