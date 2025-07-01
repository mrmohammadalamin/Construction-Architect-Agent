import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class PostConstructionFacilityManagementAgent(BaseConstructionAgent):
    """
    Handles operations and maintenance aspects of the building after project completion.
    This includes managing assets, scheduling maintenance, and optimizing building performance.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Post-Construction & Facility Management Agent",
            description="Manages post-construction operations and facility maintenance.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides preliminary facility management and maintenance considerations.
        """
        project_id = user_input.get("project_id")
        project_type = user_input.get("project_type", "residential")
        project_description = user_input.get("project_description", "a construction project")
        architectural_concept = user_input.get("architectural_concept", {})
        system_design = user_input.get("system_design", {})

        logger.info(f"Post-Construction/FM Agent: Assessing FM needs for project {project_id}.")

        try:
            prompt = (
                f"As a facility management expert, outline key post-construction and facility management "
                f"considerations for a '{project_type}' project described as '{project_description}'. "
                f"Consider its architectural style '{architectural_concept.get('design_style_summary')}' "
                f"and system design elements (e.g., '{system_design.get('mep_notes')}'). "
                f"Suggest typical maintenance requirements, potential operational challenges, "
                f"and smart building technologies for long-term efficiency. "
                f"Output STRICTLY as a JSON object with keys 'fm_overview' (string summary), "
                f"'maintenance_requirements' (list of strings), 'operational_challenges' (list of strings), "
                f"'smart_building_tech_suggestions' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for post-construction/FM."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'fm_overview' not in parsed_response or \
                   'maintenance_requirements' not in parsed_response or \
                   'operational_challenges' not in parsed_response or \
                   'smart_building_tech_suggestions' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected post-construction/FM format.")
            except json.JSONDecodeError:
                logger.error(f"Post-Construction/FM Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "fm_overview": "FM assessment failed due to parsing error.",
                    "maintenance_requirements": ["HVAC checks", "Roof inspections"],
                    "operational_challenges": ["Energy consumption management"],
                    "smart_building_tech_suggestions": ["Automated lighting", "Predictive HVAC"]
                }

            simulated_fm_analysis = {
                "project_id": project_id,
                "status": "fm_assessment_complete",
                "fm_overview": parsed_response.get("fm_overview"),
                "maintenance_requirements": parsed_response.get("maintenance_requirements"),
                "operational_challenges": parsed_response.get("operational_challenges"),
                "smart_building_tech_suggestions": parsed_response.get("smart_building_tech_suggestions")
            }
            logger.info(f"Post-Construction/FM Agent: Completed FM assessment for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "post_construction_fm_analysis": simulated_fm_analysis
            }

        except Exception as e:
            logger.error(f"Post-Construction/FM Agent: Error during FM assessment: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed FM assessment for {project_id}: {str(e)}"
            }