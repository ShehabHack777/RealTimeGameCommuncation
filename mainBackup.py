import redis
import json
import asyncio
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect


app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379)



# Function to update player score
def update_player_score(player_id, score):
    # Update player score in Redis sorted set
    redis_client.zadd('leaderboard', {player_id: score})

    # Publish leaderboard update message to Redis channel
    leaderboard = get_leaderboard()
    redis_client.publish('game_updates', json.dumps({'leaderboard': leaderboard}))

# Function to create a new player record
def create_player(player_id, score):
    # Create a new player record in Redis sorted set
    redis_client.zadd('leaderboard', {player_id: score})

    top_players = get_leaderboard()

    # Publish create message to Redis channel
    redis_client.publish('game_updates', json.dumps({'leaderboard': top_players, 'action': 'create'}))

# Function to retrieve top players
def get_leaderboard():
    # Retrieve top players from Redis sorted set
    leaderboard = redis_client.zrevrange('leaderboard', 0, 5, withscores=True)
  
    # Publish create message to Redis channel
    leaderboard = [{'player_id': player_id.decode(), 'score': score} for player_id, score in leaderboard]
    redis_client.publish('game_updates', json.dumps({'leaderboard': leaderboard, 'action': 'read'}))
    return leaderboard

# Subscribe to the updates channel
pubsub = redis_client.pubsub()
pubsub.subscribe('game_updates')

# List to store active WebSocket connections
active_connections = []


# Function to process real-time updates
async def process_updates(message):
    # Update leaderboard or perform other actions based on the received message
    print("Received update:", message)

    # Send the update to all connected WebSocket clients
    leaderboard_update = json.dumps(message)
    for connection in active_connections:
        try:
            await connection.send_text(leaderboard_update)
        except WebSocketDisconnect:
            active_connections.remove(connection)

# Endpoint to update player scores
@app.post("/update_score/{player_id}")
async def update_score(player_id: str, new_score: int):
    # Update player score
    update_player_score(player_id, new_score)
    return {"message": "Score updated and published"}

# Endpoint to create a new player record
@app.post("/create_player/{player_id}")
async def create_player_endpoint(player_id: str, score: int):
    # Create a new player record
    create_player(player_id, score)
    return {"message": "Player created and published"}

# Endpoint to retrieve top players
@app.get("/top_players/")
async def get_top_players_endpoint():
    # Retrieve top players
    top_players = get_leaderboard()
    return {"top_players": top_players}


game_updates = redis_client.pubsub()
game_updates.subscribe('game_updates')



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
                await process_updates(json.loads(message['data']))
            else:
                await asyncio.sleep(0.1)  # Small sleep to avoid blocking
    except WebSocketDisconnect:
        active_connections.remove(websocket)  # Remove client connection from list


# Function to process real-time updates (Chat version)-------------------------------------------------------------------
# List to store active WebSocket connections
active_connections_chat = []
async def process_updates_chat(message):
    # Update leaderboard or perform other actions based on the received message
    print("Received update:", message)

    # Send the update to all connected WebSocket clients
    chat_message = json.dumps(message)
    for connection_chat in active_connections_chat:
        try:
            await connection_chat.send_text(chat_message)
        except WebSocketDisconnect:
            active_connections_chat.remove(connection_chat)



# Subscribe to the chat updates channel
chat_updates = redis_client.pubsub()
chat_updates.subscribe('chat_updates')

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

            # Send the chat message to all connected WebSocket clients
                
            await process_updates_chat(message)
    
    except WebSocketDisconnect:
                    active_connections_chat.remove(websocket)  # Remove client connection from list




