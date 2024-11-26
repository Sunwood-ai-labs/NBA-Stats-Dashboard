import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class DataProcessor:
    @staticmethod
    def process_team_stats(boxscore_data):
        if not boxscore_data:
            return None
        
        team_stats = []
        for team in ['homeTeam', 'awayTeam']:
            stats = boxscore_data.get(team, {})
            team_stats.append({
                'team': stats.get('teamName', ''),
                'points': stats.get('points', 0),
                'rebounds': stats.get('rebounds', 0),
                'assists': stats.get('assists', 0),
                'steals': stats.get('steals', 0),
                'blocks': stats.get('blocks', 0)
            })
        return pd.DataFrame(team_stats)

    @staticmethod
    def create_team_comparison_chart(team_stats):
        if team_stats is None:
            return None
        
        fig = go.Figure()
        categories = ['points', 'rebounds', 'assists', 'steals', 'blocks']
        
        for idx, team in team_stats.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[team[cat] for cat in categories],
                theta=categories,
                fill='toself',
                name=team['team']
            ))
            
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(team_stats[categories].max())]
                )
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        return fig
