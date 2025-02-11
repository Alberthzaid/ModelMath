import os

import pandas as pd

from models_clients.deepseek import DeepseekClient
from models_clients.ollama import OllamaClient
from rag import RAG


class WorldCupRAG(RAG):
  def __init__(self, model_client: OllamaClient):
    super().__init__(model_client)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    groups_path = os.path.join(base_dir, "datasets", "groups.csv")
    matches_path = os.path.join(base_dir, "datasets", "international_matches.csv")

    self.groups = pd.read_csv(groups_path)
    self.matches = pd.read_csv(matches_path)

  def retrieve_match_data(self, team1: str, team2: str):
    filtered_matches = self.matches[
      ((self.matches["home_team"] == team1) & (self.matches["away_team"] == team2)) |
      ((self.matches["home_team"] == team2) & (self.matches["away_team"] == team1))
      ]

    if filtered_matches.empty:
      return f"No se encontraron partidos previos entre {team1} y {team2}."

    stats = filtered_matches[[
      "date", "home_team", "away_team", "home_team_score", "away_team_score",
      "home_team_fifa_rank", "away_team_fifa_rank", "home_team_result"
    ]]

    return stats.to_dict(orient="records")

  def predict_match(self, team1: str, team2: str):
    match_history = self.retrieve_match_data(team1, team2)

    prompt = f"""
        Basado en los siguientes datos históricos, predice el resultado del partido entre {team1} y {team2} en el Mundial 2026.

        Historial de enfrentamientos:
        {match_history}

        Responde con un análisis del rendimiento de ambos equipos y una posible predicción de marcador.
        """

    return self.generate_response(prompt)

  def get_team_matches(self, team_name):
    matches = self.matches[
      (self.matches["home_team"] == team_name) | (self.matches["away_team"] == team_name)
      ]
    return matches[["date", "home_team", "away_team", "home_team_score", "away_team_score"]]

  def get_match_result(self, team1, team2):
    match = self.matches[
      ((self.matches["home_team"] == team1) & (self.matches["away_team"] == team2)) |
      ((self.matches["home_team"] == team2) & (self.matches["away_team"] == team1))
      ]

    if match.empty:
      return f"No se encontró un partido entre {team1} y {team2}."

    row = match.iloc[0]
    return f"{row['home_team']} {row['home_team_score']} - {row['away_team_score']} {row['away_team']}"

  def get_top_scorers(self, n=5):
    teams = pd.concat([
      self.matches[["home_team", "home_team_score"]].rename(columns={"home_team": "team", "home_team_score": "goals"}),
      self.matches[["away_team", "away_team_score"]].rename(columns={"away_team": "team", "away_team_score": "goals"})
    ])

    top_scorers = teams.groupby("team")["goals"].sum().sort_values(ascending=False).head(n)
    return top_scorers

  def get_team_stats(self, team_name):
    home_matches = self.matches[self.matches["home_team"] == team_name]
    away_matches = self.matches[self.matches["away_team"] == team_name]

    total_played = len(home_matches) + len(away_matches)
    total_wins = len(home_matches[home_matches["home_team_score"] > home_matches["away_team_score"]]) + \
                 len(away_matches[away_matches["away_team_score"] > away_matches["home_team_score"]])
    total_draws = len(home_matches[home_matches["home_team_score"] == home_matches["away_team_score"]]) + \
                  len(away_matches[away_matches["away_team_score"] == away_matches["home_team_score"]])
    total_losses = total_played - total_wins - total_draws
    total_goals = home_matches["home_team_score"].sum() + away_matches["away_team_score"].sum()

    return {
      "team": team_name,
      "played": total_played,
      "wins": total_wins,
      "draws": total_draws,
      "losses": total_losses,
      "goals_scored": total_goals
    }
