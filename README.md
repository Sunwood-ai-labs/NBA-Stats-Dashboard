



<div align="center">
  <img src="assets/nba-header-modern.svg" alt="NBA Dashboard Header" width="100%">
  
  # 🏀 NBA リアルタイムダッシュボード
</div>

## 概要
NBAの試合をリアルタイムで追跡し、詳細な統計情報を可視化するStreamlitベースのダッシュボードアプリケーションです。

## 主な機能
- リアルタイムのスコアボード表示
- 選手の詳細な統計情報の可視化
- チーム比較分析
- Play-by-Play（試合経過）のリアルタイム表示
- 過去の試合データ分析

## 使用技術
- Streamlit
- NBA API
- Plotly
- Pandas
- Python 3.11

## インストール方法
```bash
# 依存パッケージのインストール
pip install streamlit nba_api plotly pandas
```

## 使用方法
1. アプリケーションの起動
```bash
streamlit run main.py
```

2. 機能
- 自動更新：サイドバーで更新間隔を設定可能（10-60秒）
- チーム比較：レーダーチャートとバーチャートで視覚的に比較
- 選手統計：最大3選手までの詳細な統計比較が可能
- Play-by-Play：試合の詳細な経過をリアルタイムで表示

## データの更新頻度
- スコア：30秒ごと（デフォルト、調整可能）
- 選手統計：試合中リアルタイム
- Play-by-Play：リアルタイム

## 注意事項
- NBA APIの利用制限に従って実装されています
- 試合がない時間帯は、最近の試合結果が表示されます

## 開発環境
- Replit
- Python 3.11
- 各種データ可視化ライブラリ
