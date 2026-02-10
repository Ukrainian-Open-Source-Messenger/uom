import dotenv from 'dotenv';
dotenv.config();

import { startServer } from './server';

const PORT = process.env.PORT || 3003;

startServer(PORT);
