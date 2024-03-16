import json
import redis
# redis_client = redis.Redis(host='localhost', port=6379)

class Leaderboard:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def update_player_score(self, player_id, score):
        """Updates player score and publishes leaderboard update."""
        self.redis_client.zadd('leaderboard', {player_id: score})
        leaderboard = self.get_leaderboard()
        self.redis_client.publish('game-update',json.dumps({'leaderboard':leaderboard}))

    def create_player(self, player_id, score):
        """Creates a new player record and publishes create message."""
        self.redis_client.zadd('leaderboard', {player_id: score})
        leaderboard = self.get_leaderboard()
        self.redis_client.publish('game_updates', json.dumps({'leaderboard': leaderboard}))
        # self.publish_leaderboard_update(action='create')

    def get_leaderboard(self):
        """Retrieves top players and publishes read message."""
        leaderboard = self.redis_client.zrevrange('leaderboard', 0, 5, withscores=True)
        leaderboard = [{'player_id': player_id.decode(), 'score': score} for player_id, score in leaderboard]
        self.redis_client.publish('game_updates', json.dumps({'leaderboard': leaderboard}))
        # self.publish_leaderboard_update(action='read')
        return leaderboard

    # def publish_leaderboard_update(self, action=None):
    #     """Publishes leaderboard update to Redis channel."""
    #     leaderboard = self.get_leaderboard()
    #     message = json.dumps({'leaderboard': leaderboard, 'action': action})
    #     self.redis_client.publish('game_updates', message)

# # Example usage:
# redis_client = redis.Redis()  # Assuming a Redis client is available
# leaderboard = Leaderboard(redis_client)

# leaderboard.update_player_score("player1", 1200)
# leaderboard.create_player("player2", 850)
# top_players = leaderboard.get_leaderboard()  # This will also publish a 'read' update
# print(top_players)
