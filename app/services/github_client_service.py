import base64
import httpx
from app.config import GITHUB_TOKEN
from app.logger import logger


class GithubClientService:
    def __init__(self) -> None:
        token = GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}


    async def get_json(self, endpoint: str):
        logger.info(f"Requesting endpoint: {endpoint}")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{endpoint}", headers=self.headers
            )
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

    async def get_user(self, username: str):
        logger.info(f"Reading user: {username}")
        return await self.get_json(f"/users/{username}")

    async def get_repos(self, username: str):
        logger.info(f"Reading repositories for: {username}")
        return await self.get_json(f"/users/{username}/repos")

    async def get_repo_languages(self, username: str, repo: str):
        logger.info(f"Reading languages for repo: {repo}")
        return await self.get_json(f"/repos/{username}/{repo}/languages")

    async def get_readme(self, username: str, repo: str):
        logger.info(f"Decoding README for repo: {repo}")
        raw = await self.get_readme_raw(username, repo)
        if not raw:
            return None
        try:
            return base64.b64decode(raw).decode("utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error decoding README for repo {repo}: {e}")
            return None

    async def get_branches(self, username: str, repo: str):
        return await self.get_json(f"/repos/{username}/{repo}/branches")

    async def get_commit_count(self, username: str, repo: str):
        url = f"{self.base_url}/repos/{username}/{repo}/stats/contributors"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

            # GitHub may return 202 when stats are being generated
            if response.status_code == 202:
                return None

            if response.status_code == 404:
                return 0

            response.raise_for_status()
            data = response.json()

            # Sum total commits from all contributors
            return sum(item.get("total", 0) for item in data)



    async def get_user_commits(self, username: str, repo_owner: str, repo: str):
        return await self.get_json(
            f"/repos/{repo_owner}/{repo}/commits?author={username}"
        )

    async def get_commit_detail(self, repo_owner: str, repo: str, sha: str):
        return await self.get_json(f"/repos/{repo_owner}/{repo}/commits/{sha}")
