import warnings
import  pandas as pd

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
