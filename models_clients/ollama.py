import requests

class OllamaClient:
  def __init__(self, model: str, ollama_url: str = "http://localhost:11434"):
    self.ollama_url = ollama_url
    self.model = model

  def query(self, prompt: str) -> str:
    payload = {
      "model": self.model,
      "prompt": prompt,
      "stream": False
    }

    response = requests.post(self.ollama_url + "/api/generate", json=payload)

    try:
      return response.json()["response"]
    except requests.exceptions.JSONDecodeError as e:
      print(f"JSON decode error: {e}")
      return response.text
