"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.verifyToken = verifyToken;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const config_1 = require("../config");
function verifyToken(token) {
    try {
        return jsonwebtoken_1.default.verify(token, config_1.JWT_SECRET);
    }
    catch (error) {
        console.error('Token verification failed:', error);
        return null;
    }
}
