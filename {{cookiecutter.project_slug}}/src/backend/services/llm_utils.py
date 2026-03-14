import time
from loguru import logger
from ..core.config import settings

class LLMMonitor:
    @staticmethod
    def calculate_cost(input_tokens: int, output_tokens: int) -> float:
        input_cost = (input_tokens / 1_000_000) * settings.COST_PER_1M_INPUT_TOKENS
        output_cost = (output_tokens / 1_000_000) * settings.COST_PER_1M_OUTPUT_TOKENS
        total = input_cost + output_cost
        logger.info(f"💰 Cost for this request: ${total:.6f}")
        return total

class Guardrail:
    @staticmethod
    def validate_output(text: str) -> str:
        """Checks if the LLM output violates any rules."""
        for word in settings.BANNED_KEYWORDS:
            if word.lower() in text.lower():
                logger.warning(f"🚨 Guardrail Triggered: Banned keyword '{word}' found!")
                return "I'm sorry, but I cannot provide that information as it violates safety guidelines."
        return text