import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class LearningAdaptationAgent(BaseConstructionAgent):
    """
    Continuously learns from project data, agent interactions, and human feedback
    to improve system performance, optimize workflows, and adapt to new challenges
    or unforeseen circumstances.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Learning & Adaptation Agent",
            description="Analyzes project outcomes to learn and suggest improvements for future projects.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates learning from project outcomes and suggests adaptations.
        This agent would typically run after project completion or major phases.
        For this simulation, it will provide generic learning based on initial inputs.
        """
        project_id = user_input.get("project_id")
        project_description = user_input.get("project_description", "a construction project")
        project_size = user_input.get("project_size", "medium")
        location = user_input.get("location", "unspecified")

        # In a real scenario, this would analyze actual project data and agent performance
        # For simulation, we'll ask Gemini to generalize based on initial input.
        logger.info(f"Learning & Adaptation Agent: Simulating learning for project {project_id}.")

        try:
            prompt = (
                f"Based on a hypothetical '{project_description}' project of '{project_size}' size in '{location}', "
                f"what are common lessons learned or areas for adaptation in similar construction projects? "
                f"Suggest improvements for efficiency, cost-effectiveness, or quality for future projects. "
                f"Output STRICTLY as a JSON object with keys 'lessons_learned' (list of strings), "
                f"'adaptation_suggestions' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.6)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for learning/adaptation."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'lessons_learned' not in parsed_response or \
                   'adaptation_suggestions' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected learning/adaptation format.")
            except json.JSONDecodeError:
                logger.error(f"Learning & Adaptation Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "lessons_learned": ["Generic lesson: communication is key."],
                    "adaptation_suggestions": ["Improve initial planning accuracy."]
                }

            simulated_learning_output = {
                "project_id": project_id,
                "status": "simulated_learning_complete",
                "lessons_learned": parsed_response.get("lessons_learned"),
                "adaptation_suggestions": parsed_response.get("adaptation_suggestions")
            }
            logger.info(f"Learning & Adaptation Agent: Completed simulated learning for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "learning_adaptation_insights": simulated_learning_output
            }

        except Exception as e:
            logger.error(f"Learning & Adaptation Agent: Error during simulated learning: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed simulated learning for {project_id}: {str(e)}"
            }