import { broadcast } from "../helpers";

export function onTyping(currentUserId: string | undefined, username: string | undefined, data: any) {
  broadcast(
    {
      type: "typing",
      username,
      isTyping: data.isTyping,
    },
    currentUserId // не відправляємо самому собі
  );
}
