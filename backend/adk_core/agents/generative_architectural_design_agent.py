import json
import logging
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class GenerativeArchitecturalDesignAgent(BaseConstructionAgent):
    """
    Generates initial architectural concepts and visual sketches using Gemini and Imagen.
    It interprets project requirements and site feasibility data to propose a design.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Generative Architectural Design Agent",
            description="Generates initial architectural concepts and visual sketches.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates architectural concepts and renders based on provided project data.
        """
        project_id = user_input.get("project_id")
        site_report = user_input.get("site_feasibility_report", {}) # Data from Site Intelligence Agent
        initial_requirements = user_input.get("parsed_data", user_input) # Refined requirements from Client Engagement

        logger.info(f"Architectural Design Agent: Generating concepts for project {project_id}.")

        try:
            # 1. Use Gemini to interpret design brief, site constraints, and propose a concept
            design_prompt = (
                f"Based on the following site feasibility report and initial client requirements, "
                f"propose an architectural concept. Consider the project type '{initial_requirements.get('project_type')}' "
                f"and desired features '{initial_requirements.get('desired_features')}', adhering to "
                f"zoning rules like max height {site_report.get('zoning_data',{}).get('allowed_height_m', 'N/A')}m. "
                f"Summarize the proposed style, key design elements, and how it addresses site constraints. "
                f"Site Report: {json.dumps(site_report)}\nInitial Requirements: {json.dumps(initial_requirements)}\n"
                f"Format output STRICTLY as JSON with keys 'design_summary' (string), 'key_elements' (list of strings), 'considerations' (list of strings)."
            )
            logger.info("Architectural Design Agent: Calling Gemini for design brief interpretation...")
            gemini_design_response_str = self.gemini_service.generate_text(design_prompt, temperature=0.5)

            if gemini_design_response_str is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for design concept."
                }

            try:
                gemini_design_parsed = json.loads(gemini_design_response_str)
            except json.JSONDecodeError:
                logger.error(f"Architectural Design Agent: Gemini design response was not valid JSON: {gemini_design_response_str}. Using fallback data.")
                gemini_design_parsed = {
                    "design_summary": "Could not parse design summary from AI. Manual design review needed.",
                    "key_elements": ["Unspecified"],
                    "considerations": ["Manual design. AI parsing failed or response malformed."]
                }

            # 2. Use Imagen to generate a preliminary visual sketch based on the concept
            image_prompt = (
                f"Architectural sketch of a {initial_requirements.get('project_type')} in {site_report.get('location')} "
                f"with features like {', '.join(initial_requirements.get('desired_features', []))} and a {gemini_design_parsed.get('design_summary')} style. "
                f"Exterior view, clear daylight, high detail, concept art."
            )
            logger.info("Architectural Design Agent: Calling Imagen for conceptual render...")
            image_base64 = self.gemini_service.generate_image(image_prompt)
            
            simulated_design_concept = {
                "project_id": project_id,
                "design_style_summary": gemini_design_parsed.get("design_summary"),
                "key_design_elements": gemini_design_parsed.get("key_elements", []),
                "site_considerations_addressed": gemini_design_parsed.get("considerations", []),
                "conceptual_render_base64": image_base64[:100] + "..." if image_base64 else "N/A", # Truncate for display
                "full_conceptual_render_base64": image_base64, # Full base64 for actual display if needed
                "floor_plan_url_placeholder": "https://placehold.co/600x400/FF0000/FFFFFF?text=Conceptual_Floor_Plan",
            }
            logger.info(f"Architectural Design Agent: Generated concepts for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "architectural_concept": simulated_design_concept
            }

        except Exception as e:
            logger.error(f"Architectural Design Agent: Error during design generation: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed architectural design for {project_id}: {str(e)}"
            }