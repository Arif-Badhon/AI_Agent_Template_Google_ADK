from src.agents.base.factory import AgentFactory
from .cache_service import SemanticCache
from google import genai # Assuming Google ADK/GenAI SDK

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
        # 1. Generate embedding for the incoming task
        # (Assuming you have an embedding utility)
        task_embedding = await self.get_embedding(task)

        # 2. Check Semantic Cache
        cached_hit = await self.cache.get_cached_response(task_embedding)
        if cached_hit:
            logger.info("🚀 Semantic Cache Hit! Skipping LLM call.")
            return {"agent": "cache", "result": cached_hit, "cached": True}

        # 3. If no hit, proceed with routing and execution
        agent_name = await self.get_best_agent(task)
        selected_agent = self.agents[agent_name]
        result = await selected_agent.execute(task)

        # 4. Save the new result to cache for next time
        await self.cache.save_to_cache(task_embedding, task, result)
        
        return {"agent": agent_name, "result": result, "cached": False}