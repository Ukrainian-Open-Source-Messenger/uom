import jwt from 'jsonwebtoken';
import { JWT_SECRET } from "../config";

export function verifyToken(token: string): { userId: string; username: string } | null {
  try {
    return jwt.verify(token, JWT_SECRET) as { userId: string; username: string };
  } catch (error) {
    console.error('Token verification failed:', error);
    return null;
  }
}
