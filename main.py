import redis
import json
import asyncio
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from Pakages.updateprocessor import  UpdateProcessor
from Pakages.leaderboard import  Leaderboard
from Pakages.chatupdateprocessor import  ChatUpdateProcessor


# Leaderboard=Leaderboard(redis)
redis_client = redis.Redis(host='localhost', port=6379)
active_connections = []
active_connections_chat = []
chat_updates = redis_client.pubsub()
chat_updates.subscribe('chat_updates')
# Subscribe to the updates channel
game_updates = redis_client.pubsub()
game_updates.subscribe('game_updates')

app = FastAPI()
# Connect to Redis

leaderboard = Leaderboard(redis_client)
Updateprocessor=UpdateProcessor(active_connections)
ChatUpdateprocessor = ChatUpdateProcessor(active_connections_chat)



# List to store active WebSocket connections


# Endpoint to update player scores
@app.post("/update_score/{player_id}")
async def update_score(player_id: str, new_score: int):
    # Update player score
    leaderboard.update_player_score(player_id, new_score)
    return {"message": "Score updated and published"}

# Endpoint to create a new player record
@app.post("/create_player/{player_id}")
async def create_player_endpoint(player_id: str, score: int):
    # Create a new player record
    leaderboard.create_player(player_id, score)
    return {"message": "Player created and published"}

# Endpoint to retrieve top players
@app.get("/top_players/")
async def get_top_players_endpoint():
    # Retrieve top players
    top_players = leaderboard.get_leaderboard()
    return {"top_players": top_players}





# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)  # Add client connection to list
    try:
        while True:
            # Wait for message from Redis
            message = game_updates.get_message(ignore_subscribe_messages=True, timeout=1)
            if message and message['type'] == 'message':
                await Updateprocessor.process_updates(json.loads(message['data']))
            else:
                await asyncio.sleep(0.1)  # Small sleep to avoid blocking
    except WebSocketDisconnect:
        active_connections.remove(websocket)  # Remove client connection from list

# WebSocket endpoint for real-time chat
@app.websocket("/chat")
async def chat_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections_chat.append(websocket)  # Add client connection to list
    try:
        while True:
            # Wait for message from WebSocket
            message = await websocket.receive_text()
            # Publish chat message to Redis channel
            redis_client.publish('chat_updates', message)
            # Send the chat message to all connected WebSocket client
            await ChatUpdateprocessor.process_updates_chat(message)
    
    except WebSocketDisconnect:
                    active_connections_chat.remove(websocket)  # Remove client connection from list




