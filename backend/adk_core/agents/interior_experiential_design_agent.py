import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class InteriorExperientialDesignAgent(BaseConstructionAgent):
    """
    Focuses on designing the interior spaces and surrounding landscape to enhance user experience.
    It considers architectural concepts and client features to propose aesthetic and functional designs.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Interior Experiential Design Agent",
            description="Designs interior spaces and surrounding landscape.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Develops interior and landscape designs.
        """
        project_id = user_input.get("project_id")
        architectural_concept = user_input.get("architectural_concept", {}) # Data from Architectural Agent
        desired_features = user_input.get("desired_features", [])
        project_type = user_input.get("project_type", "residential")

        logger.info(f"Experiential Design Agent: Starting interior/landscape design for {project_id}.")

        try:
            # Use Gemini to interpret client's desired features and propose design elements
            prompt = (
                f"Based on a '{project_type}' project with architectural style '{architectural_concept.get('design_style_summary')}' "
                f"and desired features '{', '.join(desired_features)}', propose interior design elements (style, materials, key spaces) "
                f"and landscape design features (garden style, outdoor elements). "
                f"Focus on enhancing user experience and functionality. "
                f"Output STRICTLY as a JSON object with keys 'interior_style' (string), 'landscape_features' (string), 'material_palette_notes' (string)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.6)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for experiential design."
                }

            try:
                parsed_response = json.loads(llm_response)
            except json.JSONDecodeError:
                logger.error(f"Experiential Design Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "interior_style": "Modern generic",
                    "landscape_features": "Basic garden layout",
                    "material_palette_notes": "Standard materials"
                }

            simulated_experiential_design = {
                "project_id": project_id,
                "interior_style": parsed_response.get("interior_style"),
                "landscape_features": parsed_response.get("landscape_features"),
                "material_palette_notes": parsed_response.get("material_palette_notes"),
                "mood_board_url_placeholder": "https://placehold.co/600x400/996633/FFFFFF?text=Interior_Mood_Board",
            }
            logger.info(f"Experiential Design Agent: Completed interior/landscape design for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "experiential_design": simulated_experiential_design
            }

        except Exception as e:
            logger.error(f"Experiential Design Agent: Error during experiential design: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed experiential design for {project_id}: {str(e)}"
            }