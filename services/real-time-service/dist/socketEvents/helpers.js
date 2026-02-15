"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.broadcast = broadcast;
const clients_1 = require("../clients");
function broadcast(data, excludeUserId) {
    const message = JSON.stringify(data);
    clients_1.clients.forEach(client => {
        if (client.userId !== excludeUserId && client.ws.readyState === 1) {
            client.ws.send(message);
        }
    });
}
