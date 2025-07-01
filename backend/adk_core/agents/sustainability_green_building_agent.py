import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class SustainabilityGreenBuildingAgent(BaseConstructionAgent):
    """
    Focuses on optimizing environmental impact, energy efficiency, and ensuring
    adherence to green building certifications (e.g., LEED, BREEAM).
    """
    def __init__(self, resolver):
        super().__init__(
            name="Sustainability & Green Building Agent",
            description="Optimizes environmental impact and ensures green building compliance.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assesses the project's sustainability potential and suggests green building strategies.
        """
        project_id = user_input.get("project_id")
        project_description = user_input.get("project_description", "a construction project")
        architectural_concept = user_input.get("architectural_concept", {})
        system_design = user_input.get("system_design", {})
        experiential_design = user_input.get("experiential_design", {})

        logger.info(f"Sustainability Agent: Assessing green building potential for project {project_id}.")

        try:
            prompt = (
                f"As a sustainability and green building expert, evaluate the potential for "
                f"sustainability for a project described as '{project_description}' "
                f"with architectural style '{architectural_concept.get('design_style_summary')}', "
                f"structural notes '{system_design.get('structural_notes')}', MEP notes '{system_design.get('mep_notes')}', "
                f"and materials like '{experiential_design.get('material_palette_notes')}'. "
                f"Suggest key green building strategies (e.g., energy efficiency, water conservation, material sourcing) "
                f"and potential certifications (e.g., LEED, BREEAM, Passive House) it could aim for. "
                f"Output STRICTLY as a JSON object with keys 'sustainability_potential' (string summary), "
                f"'green_strategies' (list of strings), 'potential_certifications' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for sustainability."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'sustainability_potential' not in parsed_response or \
                   'green_strategies' not in parsed_response or \
                   'potential_certifications' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected sustainability format.")
            except json.JSONDecodeError:
                logger.error(f"Sustainability Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "sustainability_potential": "Assessment failed due to parsing error.",
                    "green_strategies": ["Use energy-efficient lighting", "Recycle construction waste"],
                    "potential_certifications": ["Green Star"]
                }

            simulated_sustainability_analysis = {
                "project_id": project_id,
                "status": "sustainability_assessment_complete",
                "sustainability_potential": parsed_response.get("sustainability_potential"),
                "green_strategies": parsed_response.get("green_strategies"),
                "potential_certifications": parsed_response.get("potential_certifications")
            }
            logger.info(f"Sustainability Agent: Completed sustainability assessment for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "sustainability_analysis": simulated_sustainability_analysis
            }

        except Exception as e:
            logger.error(f"Sustainability Agent: Error during sustainability assessment: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed sustainability assessment for {project_id}: {str(e)}"
            }