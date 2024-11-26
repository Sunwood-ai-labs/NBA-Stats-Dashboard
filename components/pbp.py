import streamlit as st
import pandas as pd

def render_play_by_play(pbp_data):
    if not pbp_data:
        st.error("No play-by-play data available")
        return
    
    st.markdown("## Play-by-Play")
    
    plays = pbp_data.get('plays', [])
    if not plays:
        st.warning("No plays available")
        return
    
    data = []
    for play in plays[-20:]:  # 最新の20プレイを表示
        data.append({
            'Time': play.get('clock', ''),
            'Quarter': play.get('period', ''),
            'Description': play.get('description', ''),
            'Score': play.get('scoreHome', '0') + '-' + play.get('scoreAway', '0')
        })
    
    df = pd.DataFrame(data)
    
    # リバース順で表示（最新が上）
    df = df.iloc[::-1].reset_index(drop=True)
    
    st.markdown("""
        <style>
        .pbp-table {
            font-size: 0.9rem;
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(df, use_container_width=True,
                height=400,
                column_config={
                    "Time": st.column_config.TextColumn("Time", width="small"),
                    "Quarter": st.column_config.TextColumn("Qtr", width="small"),
                    "Description": st.column_config.TextColumn("Play", width="large"),
                    "Score": st.column_config.TextColumn("Score", width="small")
                })
