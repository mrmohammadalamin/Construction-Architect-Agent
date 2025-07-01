import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class PublicRelationsStakeholderCommunicationAgent(BaseConstructionAgent):
    """
    Manages all external communications for the project, including public relations,
    community engagement, and stakeholder reporting.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Public Relations & Stakeholder Communication Agent",
            description="Manages external communications and stakeholder engagement.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides preliminary communication strategy and identifies key stakeholders.
        """
        project_id = user_input.get("project_id")
        client_name = user_input.get("client_name", "the Client")
        project_description = user_input.get("project_description", "a construction project")
        location = user_input.get("location", "unspecified")

        logger.info(f"Public Relations Agent: Drafting communication strategy for project {project_id}.")

        try:
            prompt = (
                f"As a public relations and stakeholder communication expert for a construction project, "
                f"outline a preliminary communication strategy for the '{project_description}' project "
                f"in '{location}', initiated by '{client_name}'. "
                f"Identify key stakeholder groups (e.g., local community, government, media, investors), "
                f"suggest communication channels (e.g., press releases, community meetings, social media), "
                f"and propose key messages for transparency and positive public image. "
                f"Output STRICTLY as a JSON object with keys 'communication_overview' (string summary), "
                f"'key_stakeholders' (list of strings), 'communication_channels' (list of strings), "
                f"'key_messages' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for public relations."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'communication_overview' not in parsed_response or \
                   'key_stakeholders' not in parsed_response or \
                   'communication_channels' not in parsed_response or \
                   'key_messages' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected public relations format.")
            except json.JSONDecodeError:
                logger.error(f"Public Relations Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "communication_overview": "PR strategy generation failed due to parsing error.",
                    "key_stakeholders": ["Local residents", "Media"],
                    "communication_channels": ["Project website", "Local newspaper"],
                    "key_messages": ["Building for the future", "Minimizing disruption"]
                }

            simulated_pr_strategy = {
                "project_id": project_id,
                "status": "pr_strategy_drafted",
                "communication_overview": parsed_response.get("communication_overview"),
                "key_stakeholders": parsed_response.get("key_stakeholders"),
                "communication_channels": parsed_response.get("communication_channels"),
                "key_messages": parsed_response.get("key_messages")
            }
            logger.info(f"Public Relations Agent: Completed PR strategy for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "public_relations_strategy": simulated_pr_strategy
            }

        except Exception as e:
            logger.error(f"Public Relations Agent: Error during PR strategy generation: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed PR strategy generation for {project_id}: {str(e)}"
            }