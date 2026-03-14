from src.agents.base.factory import AgentFactory
from google import genai # Assuming Google ADK/GenAI SDK

class AgentOrchestrator:
    def __init__(self):
        self.agents = AgentFactory.build_from_config("config/agents.yaml")
        self.client = genai.Client() # Initialize your LLM client

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
        agent_name = await self.get_best_agent(task)
        
        if agent_name in self.agents:
            selected_agent = self.agents[agent_name]
            result = await selected_agent.execute(task)
            return {"agent": agent_name, "result": result}
        
        return {"error": f"No suitable agent found for: {agent_name}"}