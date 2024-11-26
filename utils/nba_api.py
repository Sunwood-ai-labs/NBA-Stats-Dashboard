from nba_api.live.nba.endpoints import scoreboard, boxscore, playbyplay
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
from datetime import datetime
import time

class NBADataFetcher:
    def __init__(self):
        self.scoreboard = None
        self.last_update = None

    def get_live_games(self):
        try:
            self.scoreboard = scoreboard.ScoreBoard()
            games = self.scoreboard.get_dict()
            self.last_update = datetime.now()
            return games
        except Exception as e:
            print(f"Error fetching live games: {e}")
            return None

    def get_game_boxscore(self, game_id):
        try:
            box = boxscore.BoxScore(game_id)
            return box.get_dict()
        except Exception as e:
            print(f"Error fetching boxscore: {e}")
            return None

    def get_play_by_play(self, game_id):
        try:
            pbp = playbyplay.PlayByPlay(game_id)
            return pbp.get_dict()
        except Exception as e:
            print(f"Error fetching play-by-play: {e}")
            return None
