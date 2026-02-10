import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

export function verifyToken(token: string): { userId: string; username: string } | null {
    try {
        return jwt.verify(token, JWT_SECRET) as { userId: string; username: string };
    } catch (error) {
        console.error('Token verification failed:', error);
        return null;
    }
}
