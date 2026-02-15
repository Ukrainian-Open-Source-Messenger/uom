"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.saveMessage = saveMessage;
const axios_1 = __importDefault(require("axios"));
const config_1 = require("../config");
async function saveMessage(token, text) {
    try {
        const response = await axios_1.default.post(`${config_1.MESSAGE_SERVICE_URL}/messages`, { text }, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        });
        return response.data;
    }
    catch (error) {
        console.error("Error saving message:", error.response?.data || error.message);
        return null;
    }
}
