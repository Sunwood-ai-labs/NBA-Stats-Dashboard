import streamlit as st
import pandas as pd

def render_player_stats(boxscore_data):
    if not boxscore_data:
        st.error("No player stats available")
        return

    st.markdown("## Player Statistics")
    
    tab1, tab2 = st.tabs(["Home Team", "Away Team"])
    
    with tab1:
        render_team_players(boxscore_data.get('homeTeam', {}).get('players', []))
    
    with tab2:
        render_team_players(boxscore_data.get('awayTeam', {}).get('players', []))

def render_team_players(players):
    if not players:
        st.warning("No player data available")
        return
    
    data = []
    for player in players:
        data.append({
            'Name': player.get('name', ''),
            'MIN': player.get('minutes', '0'),
            'PTS': player.get('points', 0),
            'REB': player.get('rebounds', 0),
            'AST': player.get('assists', 0),
            'STL': player.get('steals', 0),
            'BLK': player.get('blocks', 0),
            'FG%': f"{player.get('fieldGoalsPercentage', 0):.1f}"
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df.style.background_gradient(cmap='YlOrRd', subset=['PTS', 'REB', 'AST']),
                use_container_width=True)
