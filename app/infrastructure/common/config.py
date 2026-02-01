import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    FLASK_API_URL = os.getenv("FLASK_API_URL", "http://localhost:5000/api")
    MODEL_NAME = os.getenv("MODEL_NAME", "nvidia/nemotron-3-nano-30b-a3b")
    CHATBOT_PORT = int(os.getenv("CHATBOT_PORT", 7842))
    LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

config = Config()
