import json
import logging
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService
from ..utils.common import format_output_json

logger = logging.getLogger(__name__)

class StrategicClientEngagementAgent(BaseConstructionAgent):
    """
    The initial entry point agent. It processes raw client inquiries,
    refines requirements, and provides an initial acknowledgment.
    It can also act as an aggregator for high-level results or
    pass the consolidated client data to the next agent in a workflow.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Strategic Client Engagement Agent",
            description="Manages initial client interaction, requirement gathering, and project initiation.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()
        # Mock data for demonstration purposes. In a real system, this would be dynamic.
        self.mock_project_id = "proj_" + str(hash("initial_project_data"))[:8] # Simple, unique ID

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes initial client inquiry to refine requirements and kick off the workflow.
        """
        client_data = user_input # User input is already structured by main.py's Pydantic model

        logger.info(f"Client Engagement Agent: Processing new client inquiry for {client_data.get('client_name')}")

        try:
            # Use Gemini to parse and refine requirements
            prompt = (
                f"Analyze the following client inquiry for a construction project and extract key, "
                f"structured requirements. Be precise about 'project_type', 'client_name', 'budget_range', "
                f"'location', and 'desired_features'. Identify any ambiguities or areas requiring clarification. "
                f"Also, suggest immediate next steps for the project lifecycle. \n\n"
                f"Client Inquiry: {json.dumps(client_data, indent=2)}"
                f"Format the output STRICTLY as a JSON object with keys like 'parsed_requirements', 'clarification_needed', 'suggested_next_steps'."
            )
            logger.info("Client Engagement Agent: Calling Gemini to parse requirements...")
            gemini_response_str = self.gemini_service.generate_text(prompt, temperature=0.2)

            if gemini_response_str is None:
                 return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for requirement parsing."
                 }

            try:
                gemini_parsed_response = json.loads(gemini_response_str)
            except json.JSONDecodeError:
                logger.error(f"Client Engagement Agent: Gemini response was not valid JSON: {gemini_response_str}. Using raw data as fallback.")
                gemini_parsed_response = {
                    "parsed_requirements": client_data,
                    "clarification_needed": "Gemini could not parse inquiry, manual review needed.",
                    "suggested_next_steps": "Manual review of client inquiry."
                }

            parsed_requirements = gemini_parsed_response.get("parsed_requirements", client_data)
            clarification_needed = gemini_parsed_response.get("clarification_needed", "None")
            suggested_next_steps = gemini_parsed_response.get("suggested_next_steps", "Proceed to site analysis.")

            logger.info(f"Client Engagement Agent: Parsed Requirements: {format_output_json(parsed_requirements)}")
            logger.info(f"Client Engagement Agent: Clarification Needed: {clarification_needed}")
            logger.info(f"Client Engagement Agent: Suggested Next Steps: {suggested_next_steps}")

            # Return the processed client data. In a real ADK workflow, this agent might
            # also send messages to other agents via the resolver.
            return {
                "agent_name": self.name,
                "status": "success",
                "details": "Client inquiry processed. Initial data extracted. Workflow initiated.",
                "parsed_data": parsed_requirements,
                "clarifications": clarification_needed,
                "workflow_suggested": suggested_next_steps,
                "project_id": self.mock_project_id # Pass a consistent project ID
            }

        except Exception as e:
            logger.error(f"Client Engagement Agent: Error processing inquiry: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed to process client inquiry: {str(e)}"
            }