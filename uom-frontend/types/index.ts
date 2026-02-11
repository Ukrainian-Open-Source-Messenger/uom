export interface Message {
  id: string;
  userId: string;
  username: string;
  text: string;
  timestamp: number;
  edited?: boolean;
}

export interface User {
  id: string;
  username: string;
}
