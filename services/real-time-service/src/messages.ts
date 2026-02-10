const MESSAGE_SERVICE_URL = process.env.MESSAGE_SERVICE_URL || 'http://localhost:3002';

export async function saveMessage(token: string, text: string): Promise<any> {
    try {
        const response = await fetch(`${MESSAGE_SERVICE_URL}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ text })
        });
        if (!response.ok) throw new Error(`Failed to save message: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error('Error saving message:', error);
        return null;
    }
}
