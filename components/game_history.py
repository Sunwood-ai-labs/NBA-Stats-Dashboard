import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def render_game_history(nba_client):
    st.markdown("## 過去の試合データ分析")
    
    # チームIDの辞書（チーム名：チームID）
    team_ids = {
        'Atlanta Hawks': 1610612737,
        'Boston Celtics': 1610612738,
        'Brooklyn Nets': 1610612751,
        'Charlotte Hornets': 1610612766,
        'Chicago Bulls': 1610612741,
        'Cleveland Cavaliers': 1610612739,
        'Dallas Mavericks': 1610612742,
        'Denver Nuggets': 1610612743,
        'Detroit Pistons': 1610612765,
        'Golden State Warriors': 1610612744,
        'Houston Rockets': 1610612745,
        'Indiana Pacers': 1610612754,
        'LA Clippers': 1610612746,
        'Los Angeles Lakers': 1610612747,
        'Memphis Grizzlies': 1610612763,
        'Miami Heat': 1610612748,
        'Milwaukee Bucks': 1610612749,
        'Minnesota Timberwolves': 1610612750,
        'New Orleans Pelicans': 1610612740,
        'New York Knicks': 1610612752,
        'Oklahoma City Thunder': 1610612760,
        'Orlando Magic': 1610612753,
        'Philadelphia 76ers': 1610612755,
        'Phoenix Suns': 1610612756,
        'Portland Trail Blazers': 1610612757,
        'Sacramento Kings': 1610612758,
        'San Antonio Spurs': 1610612759,
        'Toronto Raptors': 1610612761,
        'Utah Jazz': 1610612762,
        'Washington Wizards': 1610612764
    }

    # チーム選択
    selected_team = st.selectbox(
        "チームを選択",
        options=list(team_ids.keys()),
        index=0
    )

    # 表示する試合数の選択
    num_games = st.slider("表示する試合数", min_value=5, max_value=20, value=10)

    if selected_team:
        team_id = team_ids[selected_team]
        game_history = nba_client.get_team_game_history(team_id, num_games)

        if game_history:
            # DataFrameの作成
            df = pd.DataFrame(game_history)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            # 試合結果の表示
            st.markdown("### 直近の試合結果")
            results_df = df[['date', 'matchup', 'win_loss', 'points', 'opponent_points']].copy()
            results_df['date'] = results_df['date'].dt.strftime('%Y-%m-%d')
            st.dataframe(results_df, use_container_width=True)

            # 得点推移のグラフ
            st.markdown("### 得点推移")
            fig_points = go.Figure()
            fig_points.add_trace(go.Scatter(
                x=df['date'],
                y=df['points'],
                mode='lines+markers',
                name='得点',
                line=dict(color='#1d428a')
            ))
            fig_points.update_layout(
                xaxis_title="日付",
                yaxis_title="得点",
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_points, use_container_width=True)

            # シューティング統計の推移
            st.markdown("### シューティング統計の推移")
            fig_shooting = go.Figure()
            shooting_stats = ['fg_pct', 'fg3_pct', 'ft_pct']
            labels = {'fg_pct': 'FG%', 'fg3_pct': '3P%', 'ft_pct': 'FT%'}
            colors = ['#1d428a', '#ce1141', '#fdb927']

            for stat, color in zip(shooting_stats, colors):
                fig_shooting.add_trace(go.Scatter(
                    x=df['date'],
                    y=df[stat],
                    mode='lines+markers',
                    name=labels[stat],
                    line=dict(color=color)
                ))

            fig_shooting.update_layout(
                xaxis_title="日付",
                yaxis_title="シュート成功率",
                yaxis=dict(tickformat='.1%'),
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_shooting, use_container_width=True)

            # 勝敗の分析
            wins = len(df[df['win_loss'] == 'W'])
            losses = len(df[df['win_loss'] == 'L'])
            
            st.markdown("### 勝敗分析")
            col1, col2 = st.columns(2)
            with col1:
                fig_wins = go.Figure(data=[go.Pie(
                    labels=['勝利', '敗北'],
                    values=[wins, losses],
                    hole=.3,
                    marker_colors=['#1d428a', '#ce1141']
                )])
                fig_wins.update_layout(
                    title=f"直近{num_games}試合の勝敗",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_wins, use_container_width=True)

            with col2:
                avg_stats = {
                    '平均得点': df['points'].mean(),
                    'FG%': df['fg_pct'].mean(),
                    '3P%': df['fg3_pct'].mean(),
                    'FT%': df['ft_pct'].mean(),
                    'リバウンド': df['rebounds'].mean(),
                    'アシスト': df['assists'].mean()
                }
                st.markdown("### チーム平均統計")
                for stat, value in avg_stats.items():
                    if stat in ['FG%', '3P%', 'FT%']:
                        st.metric(stat, f"{value:.1%}")
                    else:
                        st.metric(stat, f"{value:.1f}")

        else:
            st.error("試合データを取得できませんでした。")
