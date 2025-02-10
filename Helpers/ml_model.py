import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings

from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

class MLModel:
    def __init__(self , data : pd.DataFrame):
        self.data = data
        self.model = RandomForestClassifier(n_estimators=100 , random_state=42 , max_depth=10)

    def _prepare_data(self):
        label_mapping = {"Win":1 , "Loss":0 , "Draw":2}
        self.data["result"] = self.data["home_team_result"].map(label_mapping)

        X = self.data[['home_team_fifa_rank', 'away_team_fifa_rank',
                       'home_team_total_fifa_points', 'away_team_total_fifa_points']]
        y = self.data['result']

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self):
        pass


