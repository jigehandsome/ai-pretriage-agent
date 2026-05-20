"""
MediTriage — Base Agent
=======================
Abstract base class for all agents. Provides common LLM call logic
and structured output parsing.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Every agent inherits from this. Handles LLM calls and output formatting."""

    def __init__(self, name: str, model: str = "claude-sonnet-4-20250514"):
        self.name = name
        self.model = model

    def call_llm(self, system_prompt: str, user_input: str) -> str:
        """
        Call the LLM with a system prompt and user input.
        In production, this talks to Claude API or MiMo.
        For demo, returns a mock response.
        """
        # TODO: Replace with real LLM API call
        # Example with Anthropic SDK:
        #   client = anthropic.Anthropic()
        #   response = client.messages.create(
        #       model=self.model,
        #       system=system_prompt,
        #       messages=[{"role": "user", "content": user_input}],
        #   )
        #   return response.content[0].text
        return f"[{self.name}] Mock response for: {user_input[:50]}..."

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """Each agent must implement its own run logic."""
        pass
