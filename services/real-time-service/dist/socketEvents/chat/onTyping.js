"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.onTyping = onTyping;
const helpers_1 = require("../helpers");
function onTyping(currentUserId, username, data) {
    (0, helpers_1.broadcast)({
        type: "typing",
        username,
        isTyping: data.isTyping,
    }, currentUserId // не відправляємо самому собі
    );
}
