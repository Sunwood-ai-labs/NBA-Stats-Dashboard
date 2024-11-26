import streamlit as st
import time

def render_scoreboard(game_data):
    if not game_data:
        st.error("No live games available")
        return

    st.markdown("""
        <style>
        .scoreboard {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background: linear-gradient(45deg, #1a1a1a, #2d2d2d);
            border-radius: 15px;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    games = game_data.get('games', [])
    
    for game in games:
        col1, col2, col3 = st.columns([2,1,2])
        
        with col1:
            st.image(game['homeTeam']['teamLogoUrl'], width=100, use_container_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{game['homeTeam']['teamName']}</h3>",
                       unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div style='text-align: center;'>
                    <h2>{game['homeTeam']['score']} - {game['awayTeam']['score']}</h2>
                    <p>{game['gameStatusText']}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.image(game['awayTeam']['teamLogoUrl'], width=100, use_container_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{game['awayTeam']['teamName']}</h3>",
                       unsafe_allow_html=True)
