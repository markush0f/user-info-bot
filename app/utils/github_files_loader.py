import os
import json


def load_json(path: str):
    # Load JSON file
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_text(path: str):
    # Load text file
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def normalize_text(text: str):
    # Basic normalization applied to text blocks
    text = text.replace("\r", "")
    text = text.strip()
    return text


def extract_user_data(base_path: str):
    # Extract user data
    user_json = load_json(os.path.join(base_path, "user/user.json"))
    readme_path = os.path.join(base_path, "user/readme.md")

    user_json["readme"] = (
        load_text(readme_path) if os.path.exists(readme_path) else None
    )
    if user_json["readme"]:
        user_json["readme"] = normalize_text(user_json["readme"])

    return user_json


def extract_languages(base_path: str):
    # Extract global language usage
    return load_json(os.path.join(base_path, "languages/top_languages.json"))


def extract_projects(base_path: str):
    # Extract all project data
    projects_dir = os.path.join(base_path, "projects")
    os.makedirs(projects_dir, exist_ok=True)

    projects = []

    for repo_name in os.listdir(projects_dir):
        repo_path = os.path.join(projects_dir, repo_name)

        if not os.path.isdir(repo_path):
            continue

        repo_json_path = os.path.join(repo_path, "repo.json")
        readme_path = os.path.join(repo_path, "readme.md")
        languages_path = os.path.join(repo_path, "languages.json")
        summary_path = os.path.join(repo_path, "summary.txt")

        repo_data = load_json(repo_json_path)

        if os.path.exists(readme_path):
            repo_data["readme"] = normalize_text(load_text(readme_path))

        repo_data["languages"] = load_json(languages_path)
        repo_data["summary"] = (
            normalize_text(load_text(summary_path))
            if os.path.exists(summary_path)
            else None
        )
        projects.append(repo_data)

    return projects


# Added: extract summaries from output/summaries
def extract_summaries(base_path: str):
    summaries_dir = os.path.join(base_path, "summaries")
    summaries = {}

    if not os.path.exists(summaries_dir):
        return summaries

    for project_name in os.listdir(summaries_dir):
        project_path = os.path.join(summaries_dir, project_name)
        if not os.path.isdir(project_path):
            continue

        summary_path = os.path.join(project_path, "summary.txt")
        if os.path.exists(summary_path):
            summaries[project_name] = normalize_text(load_text(summary_path))
        else:
            summaries[project_name] = None

    return summaries


def extract_all_output():
    base_path = "output"

    user = extract_user_data(base_path)
    languages = extract_languages(base_path)
    projects = extract_projects(base_path)
    # Controlar de que si nio hay summaries devuelva False u otra
    # summaries = extract_summaries(base_path)

    return {
        "user": user,
        "languages": languages,
        "projects": projects,
        # "summaries": summaries ,
    }
