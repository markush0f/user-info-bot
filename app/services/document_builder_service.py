import json
from openai import OpenAI


class DocumentBuilderService:
    def __init__(self):
        self.client = OpenAI()

    def build_document(self, entity: dict):
        prompt = f"""
        You are an assistant that converts entities into documents.
        
        Return ONLY valid JSON inside <json> tags.
        
        JSON format:
        {{
            "title": string,
            "content": string
        }}

        Do not include explanations.
        Do not include markdown.
        Do not include backticks.

        <json>
        Convert this entity into a title + content JSON:
        {json.dumps(entity, indent=2)}
        </json>
        """

        response = self.client.responses.create(model="gpt-4.1-mini", input=prompt)

        text = response.output[0].content[0].text

        # Extract JSON between <json>...</json>
        cleaned = self._extract_json(text)

        data = json.loads(cleaned)

        return data["title"], data["content"]

    def _extract_json(self, text: str) -> str:
        start = text.find("<json>")
        end = text.rfind("</json>")

        if start == -1 or end == -1:
            raise ValueError("Model did not return JSON")

        return text[start + 6 : end].strip()
