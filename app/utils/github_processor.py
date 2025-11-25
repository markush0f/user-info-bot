def normalize_user(data: dict) -> dict:
    return {
        "login": data.get("login"),
        "name": data.get("name"),
        "bio": data.get("bio"),
        "avatar_url": data.get("avatar_url"),
        "followers": data.get("followers"),
        "following": data.get("following"),
        "public_repos": data.get("public_repos"),
    }

def normalize_repo(repo: dict) -> dict:
    return {
        "name": repo.get("name"),
        "description": repo.get("description"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "language": repo.get("language"),
        "topics": repo.get("topics", []),
        "updated_at": repo.get("updated_at"),
    }
