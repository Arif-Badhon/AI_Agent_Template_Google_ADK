from src.agents.base.factory import AgentFactory
from .cache_service import SemanticCache
from .llm_utils import LLMMonitor, Guardrail
from google import genai # Assuming Google ADK/GenAI SDK
from ..core.config import settings # Added import
from loguru import logger
import time

class AgentOrchestrator:
    def __init__(self):
        self.agents = AgentFactory.build_from_config("config/agent_config.yaml")
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY) # Initialize your LLM client
        self.cache = SemanticCache()

    async def get_embedding(self, text: str):
        # Implementation for Google embedding
        response = self.client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return response.embeddings[0].values

    async def get_best_agent(self, task: str) -> str:
        # Create a "menu" of available agents for the LLM
        agent_menu = "\n".join([f"- {name}: {a.description}" for name, a in self.agents.items()])
        
        prompt = f"""
        Given the following task: "{task}"
        Which of these agents is best suited to handle it?
        {agent_menu}
        
        Respond with ONLY the name of the agent.
        """
        
        response = self.client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        return response.text.strip().lower()

    async def run_task(self, task: str):
        total_start = time.time()
        
        # 1. Embedding & Cache
        task_embedding = await self.get_embedding(task)
        cached_hit = await self.cache.get_cached_response(task_embedding)
        
        if cached_hit:
            logger.info(f"Cache Hit! Total time: {time.time() - total_start:.4f}s")
            return {"agent": "cache", "result": cached_hit, "cached": True}

        # 2. Routing
        agent_name = await self.get_best_agent(task)
        selected_agent = self.agents.get(agent_name)
        if not selected_agent:
            return {"error": "Agent not found"}
        
        # 3. Execution & Guardrails
        raw_result = await selected_agent.execute(task)
        safe_result = Guardrail.validate_output(raw_result)

        # 4. Save to Cache
        await self.cache.save_to_cache(task_embedding, task, safe_result)
        
        logger.success(f"✅ Task completed in {time.time() - total_start:.4f}s")
        return {"agent": agent_name, "result": safe_result, "cached": False}