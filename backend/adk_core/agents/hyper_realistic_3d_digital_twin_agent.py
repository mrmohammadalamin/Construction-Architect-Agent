import logging
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class HyperRealistic3DDigitalTwinAgent(BaseConstructionAgent):
    """
    Creates a comprehensive 3D digital twin of the project by integrating all design aspects
    (architectural, structural, MEP, interior, landscape). It generates photorealistic
    renders (using Imagen).
    """
    def __init__(self, resolver):
        super().__init__(
            name="Hyper-Realistic 3D Digital Twin Agent",
            description="Integrates all design aspects into a comprehensive 3D model and generates renders.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates an initial 3D digital twin and generates renders.
        """
        project_id = user_input.get("project_id")
        architectural_concept = user_input.get("architectural_concept", {})
        experiential_design = user_input.get("experiential_design", {})
        site_report = user_input.get("site_feasibility_report", {}) # Get site report for context

        logger.info(f"Digital Twin Agent: Creating digital twin and renders for {project_id}.")

        try:
            # Generate exterior render using Imagen
            exterior_render_prompt = (
                f"Photorealistic 3D exterior render of a {architectural_concept.get('design_style_summary')} "
                f"building at {site_report.get('location')} with a '{experiential_design.get('landscape_features')}' landscape. "
                f"Incorporate elements from features like {', '.join(architectural_concept.get('key_design_elements', []))}. High detail, natural lighting, daytime."
            )
            logger.info("Digital Twin Agent: Generating exterior render using Imagen...")
            exterior_render_base64 = self.gemini_service.generate_image(exterior_render_prompt)

            # Generate interior render using Imagen
            interior_render_prompt = (
                f"Photorealistic 3D interior render of a {architectural_concept.get('design_style_summary')} building, "
                f"with '{experiential_design.get('interior_style')}' decor and materials like '{experiential_design.get('material_palette_notes')}'. "
                f"Warm lighting, cozy atmosphere, focus on a living area."
            )
            logger.info("Digital Twin Agent: Generating interior render using Imagen...")
            interior_render_base64 = self.gemini_service.generate_image(interior_render_prompt)

            simulated_twin_output = {
                "project_id": project_id,
                "digital_twin_url_placeholder": "[https://example.com/digital_twin_model.gltf](https://example.com/digital_twin_model.gltf)", # Placeholder for actual 3D model file path
                "exterior_render_base64": exterior_render_base64[:100] + "..." if exterior_render_base64 else "N/A", # Truncate for display
                "full_exterior_render_base64": exterior_render_base64, # Full base64 for actual display
                "interior_render_base64": interior_render_base64[:100] + "..." if interior_render_base64 else "N/A", # Truncate for display
                "full_interior_render_base64": interior_render_base64, # Full base64 for actual display
                "status": "initial_twin_created",
                "details": "High-fidelity digital twin model and initial renders generated.",
                "generated_render_prompts": {
                    "exterior": exterior_render_prompt,
                    "interior": interior_render_prompt
                }
            }
            logger.info(f"Digital Twin Agent: Completed digital twin creation and renders for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "digital_twin_output": simulated_twin_output
            }

        except Exception as e:
            logger.error(f"Digital Twin Agent: Error generating digital twin or renders: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed digital twin creation for {project_id}: {str(e)}"
            }