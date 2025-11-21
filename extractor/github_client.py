import httpx
from .config import get_github_token
from .logger import logger

class GitHubClient:
    def __init__(self):
        token = get_github_token()
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    async def get_json(self, endpoint: str):
        logger.info(f"Requesting endpoint: {endpoint}")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_readme_raw(self, username: str, repo: str):
        logger.info(f"Requesting README for repo: {repo}")
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/repos/{username}/{repo}/readme"
            response = await client.get(url, headers=self.headers)
            if response.status_code == 404:
                logger.warning(f"No README found for repo: {repo}")
                return None
            response.raise_for_status()
            return response.json().get("content")
