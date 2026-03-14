from src.agents.base.factory import AgentFactory
from .cache_service import SemanticCache
from google import genai # Assuming Google ADK/GenAI SDK
from loguru import logger
import time

class AgentOrchestrator:
    def __init__(self):
        self.agents = AgentFactory.build_from_config("config/agents.yaml")
        self.client = genai.Client() # Initialize your LLM client
        self.cache = SemanticCache()

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
        # 1. Start the TOTAL timer immediately
        total_start = time.time()
        
        # 2. Measure Embedding Latency (This is often a hidden bottleneck)
        embed_start = time.time()
        task_embedding = await self.get_embedding(task)
        logger.debug(f"⏱️ Embedding generation took: {time.time() - embed_start:.4f}s")

        # 3. Check Semantic Cache
        cache_start = time.time()
        cached_hit = await self.cache.get_cached_response(task_embedding)
        logger.debug(f"⏱️ Cache lookup took: {time.time() - cache_start:.4f}s")
        
        if cached_hit:
            logger.info(f"🚀 Cache Hit! Total time: {time.time() - total_start:.4f}s")
            return {"agent": "cache", "result": cached_hit, "cached": True}

        # 4. Routing Logic (LLM Layer)
        agent_name = await self.get_best_agent(task)
        selected_agent = self.agents[agent_name]
        
        # 5. Execution (Orchestration Layer)
        result = await selected_agent.execute(task)

        # 6. Finalize Cache & Logging
        await self.cache.save_to_cache(task_embedding, task, result)
        
        logger.success(f"✅ Task completed. Total duration: {time.time() - total_start:.4f}s")
        return {"agent": agent_name, "result": result, "cached": False}