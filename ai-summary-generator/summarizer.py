import os
import json
from dotenv import load_dotenv
import openai
from pathlib import Path

env_path = Path(os.getcwd()) / ".env"
load_dotenv(env_path)

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """
You will receive metadata and README content extracted from a GitHub project. Your task is to generate a detailed, structured, and comprehensive summary suitable for storing in a vector database for a chatbot system. The output must be in plain text only.

Important rules:
- Do not include code, commands, routes, file paths, configuration examples, or markdown syntax.
- Do not use symbols like *, -, •, #, or any markdown-style formatting.You will receive metadata and README content extracted from a GitHub project. Your task is to generate a detailed, structured, and comprehensive summary suitable for storing in a vector database for a chatbot system. The output must be in plain text only.

Important rules:
- Do not include code, commands, routes, file paths, configuration examples, or markdown syntax.
- Do not use symbols like *, -, •, #, or any markdown-style formatting.
- Do not speculate. Only describe what is present in the provided content.
- Write in a descriptive, neutral, and technical tone.
- The summary must be long, exhaustive, and information-dense.

Output format (plain text, exactly as shown, without markdown or symbols):

PROJECT SUMMARY
Purpose:
Key technologies:
Architecture:
Main features:
Developer skill insights:
Complexity level:
Additional notes:

Now generate a long and detailed summary based strictly on the following project content:

{content}

- Write in a descriptive, neutral, and technical tone.
- The summary must be long, exhaustive, and information-dense.

Output format (plain text, exactly as shown, without markdown or symbols):

PROJECT SUMMARY
Purpose:
Key technologies:
Architecture:
Main features:
Developer skill insights:
Complexity level:
Additional notes:

Now generate a long and detailed summary based strictly on the following project content:

{content}
"""


def summarize_project(content: str, model="gpt-4o-mini"):
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT.format(content=content)}],
    )
    return response.choices[0].message.content


def save_summary(project_name: str, summary: str, summary_path: str):
    os.makedirs(summary_path, exist_ok=True)
    file_path = os.path.join(summary_path, f"{project_name}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(summary)
