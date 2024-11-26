import streamlit as st
import time
from utils.nba_api import NBADataFetcher
from utils.data_processor import DataProcessor
from components.scoreboard import render_scoreboard
from components.player_stats import render_player_stats
from components.team_stats import render_team_stats, render_shooting_chart
from components.pbp import render_play_by_play

# ページ設定
st.set_page_config(
    page_title="NBA Live Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSSの読み込み
with open('assets/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ヘッダー画像の表示
st.image("https://images.unsplash.com/photo-1533923156502-be31530547c4", use_column_width=True)

# タイトルとサブタイトル
st.title("🏀 NBA Live Dashboard")
st.markdown("### Real-time NBA game tracking and statistics")

# サイドバーの設定
st.sidebar.image("https://images.unsplash.com/photo-1519861531473-9200262188bf", use_column_width=True)
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 10, 60, 30)

# NBA APIクライアントの初期化
nba_client = NBADataFetcher()
data_processor = DataProcessor()

def main():
    # リアルタイムデータの取得
    games_data = nba_client.get_live_games()
    
    if games_data and games_data.get('games'):
        selected_game = st.selectbox(
            "Select Game",
            options=games_data['games'],
            format_func=lambda x: f"{x['homeTeam']['teamName']} vs {x['awayTeam']['teamName']}"
        )
        
        if selected_game:
            game_id = selected_game['gameId']
            
            # スコアボードの表示
            render_scoreboard({'games': [selected_game]})
            
            # ゲームの詳細データを取得
            boxscore_data = nba_client.get_game_boxscore(game_id)
            pbp_data = nba_client.get_play_by_play(game_id)
            
            # 統計データの処理
            team_stats = data_processor.process_team_stats(boxscore_data)
            team_stats_fig = data_processor.create_team_comparison_chart(team_stats)
            
            # レイアウト
            col1, col2 = st.columns(2)
            
            with col1:
                render_team_stats(team_stats_fig)
            
            with col2:
                if boxscore_data:
                    render_shooting_chart(boxscore_data)
            
            # プレイヤー統計
            render_player_stats(boxscore_data)
            
            # Play-by-Play
            render_play_by_play(pbp_data)
            
    else:
        st.warning("No live games available at the moment")
        st.image("https://images.unsplash.com/photo-1519009843775-0105e5e6d92c", use_column_width=True)

def auto_refresh_data():
    if auto_refresh:
        time.sleep(refresh_interval)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
    auto_refresh_data()
