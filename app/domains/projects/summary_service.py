from app.core.config import OPENAI_API_KEY
import openai
import os
from app.core.logger import logger
from app.common.SUMMARY_PROMPT import SUMMARY_PROMPT
from app.infrastructure.github.github_files_loader import extract_projects


class SummaryProjectsService:
    def __init__(self) -> None:
        self.openai_api_key = OPENAI_API_KEY
        self.logger = logger

    def summarize_project(self, content: str, model="gpt-4o-mini"):
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": SUMMARY_PROMPT.format(content=content)}
            ],
        )
        message = response.choices[0].message.content
        # self.logger.info("RESPONSE: ", message)
        return response.choices[0].message.content

    def save_summary(self, project_name: str, summary: str, summary_path: str):
        os.makedirs(summary_path, exist_ok=True)
        file_path = os.path.join(summary_path, f"{project_name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(summary)

    def summarize_single_project(self, project: dict):
        logger.info(f"Summarizing single project: {project.get('name')}")

        content = f"""
        Project name: {project.get('name')}
        Description: {project.get('description')}
        Languages: {project.get('languages')}
        Commit count: {project.get('commit_count')}
        README:
        {project.get('readme', '')}
        """
        summary = self.summarize_project(content)
        logger.debug(f"Summary created for project: {project.get('name')}")
        return summary

    # Summarize all projects and save output
    def summarize_all_projects(self):
        logger.info("Loading all extracted projects")
        projects = extract_projects("output")

        for project in projects:
            name = project["name"]
            logger.info(f"Summarizing project: {name}")

            summary = self.summarize_single_project(project)

            summary_path = f"output/projects/{name}/summary.txt"
            save_text(summary, summary_path)  # type: ignore

            logger.debug(f"Summary saved at: {summary_path}")

        logger.info("All project summaries generated successfully")
        return True