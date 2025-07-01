import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class AdaptiveProjectManagementRoboticsOrchestrationAgent(BaseConstructionAgent):
    """
    Manages the overall project plan, orchestrates tasks across other agents,
    integrates data, and prepares project summaries. It's designed to adapt
    to changes and oversee project execution.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Adaptive Project Management & Robotics Orchestration Agent",
            description="Manages project planning, scheduling, and overall coordination.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinates and drafts the master project plan based on inputs from other agents.
        """
        project_id = user_input.get("project_id")
        # Gather outputs from other agents
        cost_supply_chain_analysis = user_input.get("cost_supply_chain_analysis", {})
        estimated_schedule = user_input.get("estimated_schedule", {})
        site_report = user_input.get("site_feasibility_report", {})
        architectural_concept = user_input.get("architectural_concept", {})
        project_description = user_input.get("project_description", "a construction project")

        logger.info(f"Project Management Agent: Kicking off initial planning for {project_id}.")

        try:
            # Use Gemini to synthesize a master project plan
            prompt = (
                f"As a senior project manager for a construction project, synthesize a master project plan "
                f"for '{project_description}'. Integrate the following information: "
                f"\n- Estimated Budget: {cost_supply_chain_analysis.get('total_estimated_cost_usd', 'N/A')}"
                f"\n- Cost Breakdown: {json.dumps(cost_supply_chain_analysis.get('cost_breakdown', {}))}"
                f"\n- Procurement Strategy: {cost_supply_chain_analysis.get('procurement_strategy', 'N/A')}"
                f"\n- Total Duration: {estimated_schedule.get('total_duration_weeks', 'N/A')} weeks"
                f"\n- Key Milestones: {json.dumps(estimated_schedule.get('milestones', []))}"
                f"\n- Site Considerations: {site_report.get('regulatory_summary_ai', 'N/A')}"
                f"\n- Architectural Style: {architectural_concept.get('design_style_summary', 'N/A')}"
                f"\n\nBased on this, outline a master plan including key phases, potential risks, "
                f"and next steps for client approval. "
                f"Output STRICTLY as a JSON object with keys: 'status', 'budget_summary', 'timeline_summary', "
                f"'key_milestones_overview', 'risks_identified' (list of strings), 'next_steps' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.4)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for project plan."
                }

            try:
                simulated_master_plan = json.loads(llm_response)
                # Basic validation
                if not isinstance(simulated_master_plan, dict) or \
                   'status' not in simulated_master_plan or \
                   'budget_summary' not in simulated_master_plan or \
                   'timeline_summary' not in simulated_master_plan or \
                   'key_milestones_overview' not in simulated_master_plan:
                    raise ValueError("LLM response JSON is not in the expected project plan format.")
            except json.JSONDecodeError:
                logger.error(f"Project Management Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                simulated_master_plan = {
                    "status": "master_plan_drafted_with_errors",
                    "budget_summary": f"Approx. ${cost_supply_chain_analysis.get('total_estimated_cost_usd', 'N/A')} (parsing error)",
                    "timeline_summary": f"{estimated_schedule.get('total_duration_weeks', 'N/A')} weeks (parsing error)",
                    "key_milestones_overview": "Milestones parsing failed.",
                    "risks_identified": ["LLM response parsing failed, manual risk review needed."],
                    "next_steps": ["Review generated output manually."]
                }

            simulated_master_plan["project_id"] = project_id
            logger.info(f"Project Management Agent: Master plan drafted for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "master_project_plan": simulated_master_plan
            }

        except Exception as e:
            logger.error(f"Project Management Agent: Error during project planning: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed project planning for {project_id}: {str(e)}"
            }