import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
from sklearn.preprocessing import LabelEncoder
import joblib
from clean_data import CleanData

warnings.filterwarnings("ignore")

class MLModel:
    def __init__(self, data_route: str):
        self.cleaner = CleanData(data_route)
        self.data = self.cleaner.reshaping_data()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)

    def _prepare_data(self):
        label_mapping = {"Win": 1, "Loss": 0, "Draw": 2}
        self.data = self.data.dropna(subset=['home_team_result'])
        self.data["result"] = self.data["home_team_result"].map(label_mapping)
        self.data = self.data.dropna(subset=['result'])
        X = self.data[['rank', 'rank_points']]
        y = self.data['result']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self):
        X_train, X_test, y_train, y_test = self._prepare_data()
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Precisión del modelo: {accuracy:.2f}")
        
        joblib.dump(self.model, "fifa_winner_model.pkl")
        joblib.dump(accuracy, "model_accuracy.pkl")
        print("Modelo guardado como fifa_winner_model.pkl")

