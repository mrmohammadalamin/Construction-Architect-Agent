import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class PredictiveCostSupplyChainAgent(BaseConstructionAgent):
    """
    Estimates project costs, analyzes material and labor requirements, and develops
    a preliminary procurement plan. It takes consolidated design data as input.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Predictive Cost & Supply Chain Agent",
            description="Estimates project costs and develops a preliminary procurement plan.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimates project costs and develops procurement plan.
        """
        project_id = user_input.get("project_id")
        # Extract relevant data from previous agents' outputs
        architectural_concept = user_input.get("architectural_concept", {})
        system_design = user_input.get("system_design", {})
        experiential_design = user_input.get("experiential_design", {})
        project_description = user_input.get("project_description", "a construction project")
        project_size = user_input.get("project_size", "medium")


        logger.info(f"Cost/Supply Chain Agent: Estimating costs for project {project_id}.")

        try:
            # Use Gemini to generate a detailed cost estimate and procurement strategy
            cost_prompt = (
                f"As a construction cost estimator and supply chain analyst, provide a detailed "
                f"cost breakdown and preliminary procurement strategy for a '{project_description}' "
                f"project of '{project_size}' size. "
                f"Consider insights from the architectural concept ('{architectural_concept.get('design_style_summary')}'), "
                f"system design notes ('{system_design.get('structural_notes')}', '{system_design.get('mep_notes')}'), "
                f"and interior design material palette ('{experiential_design.get('material_palette_notes')}'). "
                f"Break down costs into: materials, labor, equipment, permits/fees, and contingency (e.g., 10%). "
                f"Suggest a procurement strategy focusing on efficiency and cost-effectiveness. "
                f"Output STRICTLY as a JSON object with 'total_estimated_cost_usd' (number), "
                f"'cost_breakdown' (object with breakdown), and 'procurement_strategy' (string)."
            )
            llm_response = self.gemini_service.generate_text(cost_prompt, temperature=0.3)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for cost/supply chain."
                }

            try:
                simulated_cost_estimate = json.loads(llm_response)
                # Basic validation for expected keys
                if not isinstance(simulated_cost_estimate, dict) or \
                   'total_estimated_cost_usd' not in simulated_cost_estimate or \
                   'cost_breakdown' not in simulated_cost_estimate or \
                   'procurement_strategy' not in simulated_cost_estimate:
                    raise ValueError("LLM response JSON is not in the expected cost/supply chain format.")
            except json.JSONDecodeError:
                logger.error(f"Cost/Supply Chain Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                simulated_cost_estimate = {
                    "total_estimated_cost_usd": 700000 + (hash(project_id) % 100000), # Fallback value
                    "cost_breakdown": {"materials": "N/A", "labor": "N/A", "equipment": "N/A", "permits_fees": "N/A", "contingency": "N/A"},
                    "procurement_strategy": "Generic procurement strategy due to parsing error."
                }

            simulated_cost_estimate["project_id"] = project_id
            simulated_cost_estimate["status"] = "cost_estimation_complete"

            logger.info(f"Cost/Supply Chain Agent: Completed cost estimation for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "cost_supply_chain_analysis": simulated_cost_estimate
            }

        except Exception as e:
            logger.error(f"Cost/Supply Chain Agent: Error during cost/supply chain analysis: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed cost and supply chain analysis for {project_id}: {str(e)}"
            }