import base64

from .github_client import GitHubClient
from .logger import logger

class GitHubReader:
    def __init__(self):
        self.client = GitHubClient()

    async def get_user(self, username: str):
        logger.info(f"Reading user: {username}")
        return await self.client.get_json(f"/users/{username}")

    async def get_repos(self, username: str):
        logger.info(f"Reading repositories for: {username}")
        return await self.client.get_json(f"/users/{username}/repos")

    async def get_repo_languages(self, username: str, repo: str):
        logger.info(f"Reading languages for repo: {repo}")
        return await self.client.get_json(f"/repos/{username}/{repo}/languages")

    async def get_readme(self, username: str, repo: str):
        logger.info(f"Decoding README for repo: {repo}")
        raw = await self.client.get_readme_raw(username, repo)
        if not raw:
            return None
        try:
            return base64.b64decode(raw).decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error decoding README for repo {repo}: {e}")
            return None
