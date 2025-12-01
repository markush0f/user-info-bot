from openai import OpenAI
from app.infrastructure.repositories.embedding_repository import EmbeddingRepository
from core.db import get_session


class VectorSearchService:
    def __init__(self):
        self.session = get_session()
        self.client = OpenAI()
        self.embedding_repository = EmbeddingRepository(self.session)


    async def search(self, query: str, user_id: str, top_k: int = 5):
        query_embedding = self._embed(query)

        results = self.embedding_repository.search(user_id, query_embedding, top_k)

        return results

    def _embed(self, text: str):
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
