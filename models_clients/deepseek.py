from models_clients.ollama import OllamaClient

class DeepseekClient(OllamaClient):
  def __init__(self, version: str):
    super().__init__("deepseek-r1:" + version)