from nba_api.live.nba.endpoints import scoreboard, boxscore
from nba_api.stats.endpoints import playbyplay, leaguegamefinder
from datetime import datetime

class NBADataFetcher:
    def __init__(self):
        self.debug_mode = False

    def set_debug_mode(self, debug_mode):
        self.debug_mode = debug_mode

    def get_live_games(self):
        try:
            board = scoreboard.ScoreBoard()
            games = board.get_dict()
            if self.debug_mode:
                print(f"Live games response: {games}")
            
            if not games.get('scoreboard') or not games['scoreboard'].get('games'):
                return {'games': []}

            formatted_games = []
            for game in games['scoreboard']['games']:
                game_data = {
                    'gameId': str(game['gameId']),
                    'gameStatusText': game['gameStatusText'],
                    'homeTeam': {
                        'teamId': str(game['homeTeam']['teamId']),
                        'teamName': game['homeTeam']['teamName'],
                        'teamLogoUrl': f"https://cdn.nba.com/logos/nba/{game['homeTeam']['teamId']}/global/L/logo.svg",
                        'score': game['homeTeam']['score']
                    },
                    'awayTeam': {
                        'teamId': str(game['awayTeam']['teamId']),
                        'teamName': game['awayTeam']['teamName'],
                        'teamLogoUrl': f"https://cdn.nba.com/logos/nba/{game['awayTeam']['teamId']}/global/L/logo.svg",
                        'score': game['awayTeam']['score']
                    }
                }
                formatted_games.append(game_data)
            
            return {'games': formatted_games}
        except Exception as e:
            error_msg = f"Error fetching live games: {e}"
            if self.debug_mode:
                print(error_msg)
            return {'games': []}

    def get_game_boxscore(self, game_id):
        try:
            game_boxscore = boxscore.BoxScore(game_id=game_id)
            data = game_boxscore.get_dict()
            if self.debug_mode:
                print(f"Boxscore response: {data}")
            return self._format_boxscore_data(data)
        except Exception as e:
            error_msg = f"Error fetching boxscore: {e}"
            if self.debug_mode:
                print(error_msg)
            return None

    def get_play_by_play(self, game_id):
        try:
            pbp = playbyplay.PlayByPlay(game_id=game_id)
            data = pbp.get_dict()
            if self.debug_mode:
                print(f"Play-by-play response: {data}")
            return self._format_pbp_data(data)
        except Exception as e:
            error_msg = f"Error fetching play-by-play: {e}"
            if self.debug_mode:
                print(error_msg)
            return None

    def get_recent_games(self):
        try:
            game_finder = leaguegamefinder.LeagueGameFinder()
            games = game_finder.get_dict()
            if self.debug_mode:
                print(f"Recent games response: {games}")
            return games
        except Exception as e:
            error_msg = f"Error fetching recent games: {e}"
            if self.debug_mode:
                print(error_msg)
            return None

    def _format_boxscore_data(self, data):
        if not data or not data.get('game'):
            return None

        game = data['game']
        formatted_data = {
            'homeTeam': self._extract_team_stats(game['homeTeam']),
            'awayTeam': self._extract_team_stats(game['awayTeam'])
        }
        return formatted_data

    def _extract_team_stats(self, team_data):
        team_stats = team_data['statistics']
        team_players = [
            self._format_player_stats(player)
            for player in team_data['players']
        ]

        return {
            'teamId': str(team_data['teamId']),
            'teamName': team_data['teamName'],
            'points': team_stats['points'],
            'rebounds': team_stats['reboundsTotal'],
            'assists': team_stats['assists'],
            'steals': team_stats['steals'],
            'blocks': team_stats['blocks'],
            'fieldGoalsPercentage': float(team_stats['fieldGoalsPercentage']),
            'threePointersPercentage': float(team_stats['threePointersPercentage']),
            'freeThrowsPercentage': float(team_stats['freeThrowsPercentage']),
            'players': team_players
        }

    def _format_player_stats(self, player_data):
        stats = player_data['statistics']
        return {
            'name': player_data['name'],
            'minutes': stats['minutesCalculated'],
            'points': stats['points'],
            'rebounds': stats['reboundsTotal'],
            'assists': stats['assists'],
            'steals': stats['steals'],
            'blocks': stats['blocks'],
            'fieldGoalsPercentage': float(stats['fieldGoalsPercentage'])
        }

    def _format_pbp_data(self, data):
        if not data or not data.get('resultSets') or not data['resultSets'][0].get('rowSet'):
            return None

        plays = []
        for play in data['resultSets'][0]['rowSet']:
            plays.append({
                'clock': play[6],
                'period': play[4],
                'description': play[7],
                'scoreHome': str(play[8]),
                'scoreAway': str(play[9])
            })

        return {'plays': plays}

    def get_team_game_history(self, team_id, last_n_games=10):
        try:
            game_finder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team_id,
                last_n_games_nullable=last_n_games
            )
            games = game_finder.get_dict()
            
            if self.debug_mode:
                print(f"Team game history response: {games}")
            
            if not games or not games.get('resultSets') or not games['resultSets'][0].get('rowSet'):
                return None
            
            headers = games['resultSets'][0]['headers']
            rows = games['resultSets'][0]['rowSet']
            
            game_history = []
            for row in rows:
                game_data = dict(zip(headers, row))
                game_history.append({
                    'date': game_data['GAME_DATE'],
                    'matchup': game_data['MATCHUP'],
                    'win_loss': game_data['WL'],
                    'points': game_data['PTS'],
                    'opponent_points': game_data['PLUS_MINUS'],
                    'fg_pct': game_data['FG_PCT'],
                    'fg3_pct': game_data['FG3_PCT'],
                    'ft_pct': game_data['FT_PCT'],
                    'rebounds': game_data['REB'],
                    'assists': game_data['AST'],
                    'steals': game_data['STL'],
                    'blocks': game_data['BLK']
                })
            
            return game_history
        except Exception as e:
            error_msg = f"Error fetching team game history: {e}"
            if self.debug_mode:
                print(error_msg)
            return None