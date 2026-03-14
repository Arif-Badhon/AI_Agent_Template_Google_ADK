from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
from ..core.config import settings

class SemanticCache:
    def __init__(self):
        # Connect to your existing Qdrant instance
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=6333)
        self.collection_name = "llm_cache"
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE), # Size for Gemini Embeddings
            )

    async def get_cached_response(self, embedding: list[float], threshold: float = 0.95):
        """Search for similar previous prompts."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=1
        )
        
        if search_result and search_result[0].score >= threshold:
            return search_result[0].payload.get("response")
        return None

    async def save_to_cache(self, embedding: list[float], prompt: str, response: str):
        """Save a successful LLM interaction."""
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={"prompt": prompt, "response": response}
                )
            ]
        )