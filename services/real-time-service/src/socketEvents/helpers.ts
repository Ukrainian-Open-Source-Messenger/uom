import { clients } from '../clients';

export function broadcast(data: any, excludeUserId?: string) {
  const message = JSON.stringify(data);
  
  clients.forEach(client => {
    if (client.userId !== excludeUserId && client.ws.readyState === 1) {
      client.ws.send(message);
    }
  });
}
