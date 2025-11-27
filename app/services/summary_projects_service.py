from app.config import OPENAI_API_KEY
import openai
import os
from app.logger import logger
from app.common.SUMMARY_PROMPT import SUMMARY_PROMPT


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
