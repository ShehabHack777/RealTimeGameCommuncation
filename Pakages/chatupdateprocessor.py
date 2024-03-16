import json
from starlette.websockets import WebSocketDisconnect




class ChatUpdateProcessor:
    def __init__(self, active_connections_chat):
        self.active_connections_chat = active_connections_chat

    async def process_updates_chat(self, message):
        """Processes chat updates and sends them to connected chat clients."""
        print("Received chat message:", message)

        # Send the chat message to all connected chat clients
        chat_message = json.dumps(message)
        for connection in self.active_connections_chat:
            try:
                await connection.send_text(chat_message)
            except WebSocketDisconnect:
                self.active_connections_chat.remove(connection)

# Example usage (assuming active_connections_chat list is available):
# chat_processor = ChatUpdateProcessor(active_connections_chat)
# await chat_processor.process_updates_chat(message)
