"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JWT_SECRET = exports.MESSAGE_SERVICE_URL = exports.PORT = void 0;
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
exports.PORT = Number(process.env.PORT) || 3003;
exports.MESSAGE_SERVICE_URL = process.env.MESSAGE_SERVICE_URL || 'http://localhost:3002';
exports.JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';
