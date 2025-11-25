from app.logger import logger
from app.services.github_client_service import GithubClientService
from config import GITHUB_TOKEN
import httpx
import base64
from app.utils.github_processor import normalize_repo, normalize_user


class GithubInfoService:

    def __init__(self) -> None:
       self.github_client = GithubClientService()

    async def extract(self, username: str):
        user_raw = await self.github_client.get_user(username)
        repos_raw = await self.github_client.get_repos(username)

        user = normalize_user(user_raw)
        main_readme = await self.github_client.get_readme(username, username)
        user["readme"] = main_readme

        repos = []

        for repo in repos_raw:
            repo_data = await self._process_single_repo(username, repo)
            repos.append(repo_data)

        user["top_languages"] = self._compute_top_languages(repos)

        return {"user": user, "repos": repos}

    async def _process_single_repo(self, username: str, repo: dict):
        repo_data = normalize_repo(repo)
        name = repo_data["name"]

        readme = await self.github_client.get_readme(username, name)
        languages = await self.github_client.get_repo_languages(username, name)
        branches = await self.github_client.get_branches(username, name)
        commit_count = await self.github_client.get_commit_count(username, name)

        repo_data["readme"] = readme
        repo_data["languages"] = languages
        repo_data["branches"] = [b["name"] for b in branches]
        repo_data["commit_count"] = commit_count

        return repo_data

    def _compute_top_languages(self, repos: list):
        # Sum languages used across all repositories
        totals = {}
        for repo in repos:
            langs = repo.get("languages", {})
            for lang, value in langs.items():
                totals[lang] = totals.get(lang, 0) + value

        sorted_langs = dict(
            sorted(totals.items(), key=lambda item: item[1], reverse=True)
        )
        return sorted_langs
