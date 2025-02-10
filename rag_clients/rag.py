from models_clients.ollama import OllamaClient


class RAG:
  def __init__(self, model_client: OllamaClient):
    self.model_client = model_client

  def generate_response(self, prompt: str):
    return self.model_client.query(prompt)