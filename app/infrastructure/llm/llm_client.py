from openai import OpenAI


class LLMClient:
    def __init__(self):
        self.client = OpenAI()

    def generate(self, prompt: str, model: str = "gpt-4.1-mini") -> str:
        completion = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )

        content = completion.choices[0].message.content or ""

        return content
