// ====== login ======
export function validateLogin(username: string, password: string, email: string): string | null {
  if (!username.trim() || !password.trim()) {
    return "Введіть ім'я користувача та пароль";
  }

  if (password.length < 6) {
    return "Пароль має бути мінімум 6 символів";
  }

  return null;
};

// ====== register ======
export function validateRegister(username: string, password: string, email: string): string | null {
  if (!username.trim() || !password.trim()) {
    return "Введіть ім'я користувача та пароль";
  }

  if (password.length < 6) {
    return "Пароль має бути мінімум 6 символів";
  }

  return null;
};
