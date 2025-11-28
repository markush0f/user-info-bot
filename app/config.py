import os
from dotenv import load_dotenv


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HEADLESSX_AUTH_TOKEN = os.getenv("HEADLESSX_AUTH_TOKEN", "")
HEADLESSX_API = os.getenv("HEADLESSX_API", "")