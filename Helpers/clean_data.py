import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')

class CleanData:
    def __init__(self, data_route: str):
        self.data_route = data_route
        self.df = pd.read_csv(data_route)

    def _clean_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.data_route)
        df = df.fillna(0)
        return df

    def reshaping_data(self) -> pd.DataFrame:
        df = self._clean_data()
        new_df = df.replace({"IR Iran": "Iran", "Costarica": "Costa Rica", "Korea Republic": "South Korea"})

        fifa_rank = new_df[['date', 'home_team', 'away_team', 'home_team_fifa_rank', 'away_team_fifa_rank',
                            'home_team_total_fifa_points', 'away_team_total_fifa_points', 'home_team_result']]

        home = fifa_rank[['date', 'home_team', 'home_team_fifa_rank', 'home_team_total_fifa_points', 'home_team_result']].rename(
            columns={'home_team': 'team',
                     'home_team_fifa_rank': 'rank',
                     'home_team_total_fifa_points': 'rank_points'})

        away = fifa_rank[['date', 'away_team', 'away_team_fifa_rank', 'away_team_total_fifa_points']].rename(
            columns={'away_team': 'team',
                     'away_team_fifa_rank': 'rank',
                     'away_team_total_fifa_points': 'rank_points'})

        away['home_team_result'] = home['home_team_result'].values

        fifa_rank = pd.concat([home, away])
        fifa_rank = fifa_rank.sort_values(['team', 'date'], ascending=[True, False])
        fifa_rank['row_number'] = fifa_rank.groupby('team').cumcount() + 1
        fifa_rank_top = fifa_rank[fifa_rank['row_number'] == 1].drop('row_number', axis=1).nsmallest(10, 'rank')

        return fifa_rank_top

    def filter_by_result(self) -> pd.DataFrame:
        df = self.reshaping_data()
        result_options = df['home_team_result'].dropna().unique().tolist()
        selected_result = st.sidebar.selectbox("Selecciona el resultado", result_options)
        return df[df['home_team_result'] == selected_result]

    def filter_by_rank(self) -> pd.DataFrame:
        df = self.reshaping_data()
        min_rank, max_rank = int(df['rank'].min()), int(df['rank'].max())
        selected_rank = st.sidebar.slider("Selecciona el ranking", min_rank, max_rank, min_rank)
        return df[df['rank'] == selected_rank]

    def filter_by_rank_points(self) -> pd.DataFrame:
        df = self.reshaping_data()
        min_points, max_points = int(df['rank_points'].min()), int(df['rank_points'].max())
        selected_points = st.sidebar.slider("Selecciona los puntos de ranking", min_points, max_points, min_points)
        return df[df['rank_points'] == selected_points]

    def filter_by_team(self) -> pd.DataFrame:
        df = self.reshaping_data()
        team_options = df['team'].dropna().unique().tolist()
        selected_team = st.sidebar.selectbox("Selecciona el equipo", team_options)
        return df[df['team'] == selected_team]
