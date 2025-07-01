import logging
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class IntegratedSystemsEngineeringAgent(BaseConstructionAgent):
    """
    Develops preliminary structural and MEP (Mechanical, Electrical, Plumbing) designs
    based on architectural concepts and site reports.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Integrated Systems Engineering Agent",
            description="Develops preliminary structural and MEP designs.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Develops preliminary structural and MEP designs.
        """
        project_id = user_input.get("project_id")
        architectural_concept = user_input.get("architectural_concept", {})
        site_report = user_input.get("site_feasibility_report", {})
        project_type = user_input.get("project_type", "residential")

        logger.info(f"Systems Engineering Agent: Starting preliminary structural and MEP design for {project_id}.")

        try:
            # Use Gemini to generate structural and MEP considerations/summaries
            prompt = (
                f"Given the architectural concept '{architectural_concept.get('design_style_summary')}' "
                f"for a {project_type} project and site conditions related to '{site_report.get('environmental_risk')}', "
                f"propose preliminary structural considerations (e.g., foundation type, material recommendations) "
                f"and MEP (Mechanical, Electrical, Plumbing) system recommendations (e.g., HVAC type, smart home integration, water efficiency). "
                f"Highlight any potential integration challenges. "
                f"Format output STRICTLY as a JSON object with keys 'structural_notes' (string), 'mep_notes' (string), 'integration_challenges' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.4)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for systems engineering."
                }
            
            try:
                parsed_response = json.loads(llm_response)
            except json.JSONDecodeError:
                logger.error(f"Systems Engineering Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "structural_notes": "Generic structural design considerations.",
                    "mep_notes": "Standard MEP system recommendations.",
                    "integration_challenges": ["LLM response parsing failed."]
                }


            simulated_system_design = {
                "project_id": project_id,
                "structural_design_status": "preliminary_complete",
                "mep_design_status": "preliminary_complete",
                "structural_notes": parsed_response.get("structural_notes"),
                "mep_notes": parsed_response.get("mep_notes"),
                "design_conflicts_detected": len(parsed_response.get("integration_challenges", [])) > 0,
                "integration_challenges": parsed_response.get("integration_challenges", [])
            }
            logger.info(f"Systems Engineering Agent: Completed preliminary design for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "system_design": simulated_system_design
            }

        except Exception as e:
            logger.error(f"Systems Engineering Agent: Error during systems engineering: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed systems engineering for {project_id}: {str(e)}"
            }