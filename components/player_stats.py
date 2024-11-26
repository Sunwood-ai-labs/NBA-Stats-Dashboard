import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_player_stats(boxscore_data):
    if not boxscore_data:
        st.error("No player stats available")
        return

    st.markdown("## Player Statistics")
    
    tab1, tab2 = st.tabs(["Home Team", "Away Team"])
    
    with tab1:
        home_players = boxscore_data.get('homeTeam', {}).get('players', [])
        render_team_players(home_players, "Home")
    
    with tab2:
        away_players = boxscore_data.get('awayTeam', {}).get('players', [])
        render_team_players(away_players, "Away")

def render_team_players(players, team_type):
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
    
    # 基本的なスタッツテーブル
    st.dataframe(df, use_container_width=True)
    
    # プレイヤー選択機能
    selected_players = st.multiselect(
        f"Select players to compare ({team_type} Team)",
        options=df['Name'].tolist(),
        max_selections=3
    )
    
    if selected_players:
        selected_df = df[df['Name'].isin(selected_players)]
        
        # バーチャートの作成
        st.subheader("Player Comparison - Key Stats")
        fig_bar = go.Figure()
        
        stats = ['PTS', 'REB', 'AST', 'STL', 'BLK']
        for player in selected_players:
            player_stats = selected_df[selected_df['Name'] == player]
            fig_bar.add_trace(go.Bar(
                name=player,
                x=stats,
                y=[player_stats[stat].iloc[0] for stat in stats],
                marker_color=px.colors.qualitative.Set3[selected_players.index(player)]
            ))
        
        fig_bar.update_layout(
            barmode='group',
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # レーダーチャートの作成
        st.subheader("Player Comparison - Radar Chart")
        fig_radar = go.Figure()
        
        for player in selected_players:
            player_stats = selected_df[selected_df['Name'] == player]
            fig_radar.add_trace(go.Scatterpolar(
                r=[player_stats[stat].iloc[0] for stat in stats],
                theta=stats,
                fill='toself',
                name=player
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max([
                        selected_df[stat].max() for stat in stats
                    ])]
                )
            ),
            showlegend=True,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)
