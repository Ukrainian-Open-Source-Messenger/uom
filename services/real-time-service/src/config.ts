import dotenv from 'dotenv';
dotenv.config();

export const PORT: number = Number(process.env.PORT) || 3003;
export const MESSAGE_SERVICE_URL = process.env.MESSAGE_SERVICE_URL || 'http://localhost:3002';
export const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
