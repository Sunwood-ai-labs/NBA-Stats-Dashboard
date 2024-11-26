import streamlit as st
import plotly.graph_objects as go

def render_team_stats(team_stats_fig):
    if team_stats_fig is None:
        st.error("No team stats available")
        return
    
    st.markdown("## Team Comparison")
    st.plotly_chart(team_stats_fig, use_container_width=True)

def render_shooting_chart(boxscore_data):
    if not boxscore_data:
        return
    
    home_team = boxscore_data.get('homeTeam', {})
    away_team = boxscore_data.get('awayTeam', {})
    
    fig = go.Figure()
    
    # Home team shooting
    fig.add_trace(go.Bar(
        name=home_team.get('teamName', 'Home'),
        x=['FG%', '3P%', 'FT%'],
        y=[home_team.get('fieldGoalsPercentage', 0),
           home_team.get('threePointersPercentage', 0),
           home_team.get('freeThrowsPercentage', 0)],
        marker_color='#1d428a'
    ))
    
    # Away team shooting
    fig.add_trace(go.Bar(
        name=away_team.get('teamName', 'Away'),
        x=['FG%', '3P%', 'FT%'],
        y=[away_team.get('fieldGoalsPercentage', 0),
           away_team.get('threePointersPercentage', 0),
           away_team.get('freeThrowsPercentage', 0)],
        marker_color='#ce1141'
    ))
    
    fig.update_layout(
        title='Shooting Percentages',
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)
