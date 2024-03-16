import json
from starlette.websockets import WebSocketDisconnect




class UpdateProcessor:
    def __init__(self, active_connections):
        self.active_connections = active_connections

    async def process_updates(self, message):
        """Processes real-time updates and sends them to connected clients."""
        print("Received update:", message)

        # Update leaderboard or perform other actions based on the message
        # ... implementation for leaderboard updates ...

        # Send the update to all connected clients
        update_message = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(update_message)
            except WebSocketDisconnect:
                self.active_connections.remove(connection)

# # Example usage (assuming active_connections list is available):
# update_processor = UpdateProcessor(active_connections)
# await update_processor.process_updates(message)
