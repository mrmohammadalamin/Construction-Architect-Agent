from abc import ABC, abstractmethod
from google.adk.resolver import Resolver # Important for ADK components
from typing import Dict, Any, Optional

class BaseConstructionAgent(ABC):
    """Abstract base class for all construction-related AI agents."""

    def __init__(self, name: str, description: str, resolver: Resolver):
        self.name = name
        self.description = description
        self.resolver = resolver # The ADK resolver instance, passed during initialization

    @abstractmethod
    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Abstract method to process a user request specific to the agent's domain.
        Each specialized agent *must* implement this method.

        Args:
            user_input: A dictionary containing parsed user request details.
                        This dictionary will contain the consolidated input from the main orchestrator.
                        Example: {"project_description": "build a house", "location": "London", ...}
        Returns:
            A dictionary containing the agent's specific output.
            This dictionary should ideally include "agent_name" and "status" ("success" or "error").
        """
        pass

    def get_description(self) -> str:
        """Returns the agent's description."""
        return self.description