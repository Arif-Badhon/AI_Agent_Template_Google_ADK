import yaml
import importlib
from typing import Dict
from ..base.base_agent import BaseAgent

class AgentFactory:
    @staticmethod
    def build_from_config(config_path: str) -> Dict[str, BaseAgent]:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        registry = {}
        for entry in config['agents']:
            # Dynamically import the class based on the name
            # Assumes classes are in src.agents.specialized
            module = importlib.import_module(f"src.agents.specialized.{entry['name']}")
            agent_class = getattr(module, entry['class'])
            
            instance = agent_class()
            instance.description = entry['description'] # Inject description for routing
            registry[entry['name']] = instance
            
        return registry