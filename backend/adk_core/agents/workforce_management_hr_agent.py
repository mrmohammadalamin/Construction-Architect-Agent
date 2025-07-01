import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class WorkforceManagementHRAgent(BaseConstructionAgent):
    """
    Optimizes workforce allocation, manages human resources functions (e.g., onboarding,
    training, performance), and ensures labor compliance for the construction project.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Workforce Management & HR Agent",
            description="Optimizes workforce allocation and manages HR functions.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides preliminary workforce and HR considerations for the project.
        """
        project_id = user_input.get("project_id")
        project_size = user_input.get("project_size", "medium")
        estimated_schedule = user_input.get("estimated_schedule", {})
        location = user_input.get("location", "unspecified")

        logger.info(f"Workforce/HR Agent: Assessing workforce and HR needs for project {project_id}.")

        try:
            prompt = (
                f"As a construction workforce and HR manager, based on a '{project_size}' size project "
                f"with an estimated duration of {estimated_schedule.get('total_duration_weeks', 'N/A')} weeks in '{location}', "
                f"outline the key workforce needs (e.g., required trades, estimated team size), "
                f"important HR considerations (e.g., recruitment challenges, training needs, labor laws), "
                f"and basic labor compliance aspects for this type of project. "
                f"Output STRICTLY as a JSON object with keys 'workforce_needs' (list of strings), "
                f"'hr_considerations' (list of strings), 'labor_compliance_highlights' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for workforce/HR."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'workforce_needs' not in parsed_response or \
                   'hr_considerations' not in parsed_response or \
                   'labor_compliance_highlights' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected workforce/HR format.")
            except json.JSONDecodeError:
                logger.error(f"Workforce/HR Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "workforce_needs": ["Skilled laborers", "Project manager"],
                    "hr_considerations": ["Competitive salaries", "Safety training"],
                    "labor_compliance_highlights": ["Local labor laws adherence"]
                }

            simulated_workforce_hr_analysis = {
                "project_id": project_id,
                "status": "workforce_hr_assessment_complete",
                "workforce_needs": parsed_response.get("workforce_needs"),
                "hr_considerations": parsed_response.get("hr_considerations"),
                "labor_compliance_highlights": parsed_response.get("labor_compliance_highlights")
            }
            logger.info(f"Workforce/HR Agent: Completed workforce and HR assessment for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "workforce_hr_analysis": simulated_workforce_hr_analysis
            }

        except Exception as e:
            logger.error(f"Workforce/HR Agent: Error during workforce/HR assessment: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed workforce/HR assessment for {project_id}: {str(e)}"
            }