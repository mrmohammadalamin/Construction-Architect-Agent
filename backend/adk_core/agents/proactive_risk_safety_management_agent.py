import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class ProactiveRiskSafetyManagementAgent(BaseConstructionAgent):
    """
    Identifies, assesses, and mitigates project risks (e.g., financial, schedule, technical)
    and ensures safety compliance throughout the construction lifecycle.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Proactive Risk & Safety Management Agent",
            description="Identifies, assesses, and mitigates project risks and ensures safety compliance.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assesses risks and safety concerns for the project.
        """
        project_id = user_input.get("project_id")
        master_project_plan = user_input.get("master_project_plan", {})
        site_report = user_input.get("site_feasibility_report", {})
        project_description = user_input.get("project_description", "a construction project")

        logger.info(f"Risk/Safety Agent: Assessing risks and safety for project {project_id}.")

        try:
            prompt = (
                f"As a construction risk and safety manager, analyze the following project details "
                f"and identify potential risks (financial, schedule, technical, safety). "
                f"Suggest mitigation strategies for these risks. "
                f"\nProject Description: {project_description}"
                f"\nMaster Plan Summary: {master_project_plan.get('budget_summary')}, {master_project_plan.get('timeline_summary')}, Milestones: {master_project_plan.get('key_milestones_overview')}"
                f"\nSite Report Environmental Risk: {site_report.get('environmental_risk')}"
                f"\nSite Compliance Challenges: {', '.join(site_report.get('compliance_challenges_ai', []))}"
                f"Output STRICTLY as a JSON object with keys 'identified_risks' (list of strings with description and type), "
                f"'mitigation_strategies' (list of strings), 'safety_highlights' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for risk/safety."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'identified_risks' not in parsed_response or \
                   'mitigation_strategies' not in parsed_response or \
                   'safety_highlights' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected risk/safety format.")
            except json.JSONDecodeError:
                logger.error(f"Risk/Safety Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "identified_risks": ["Generic risk identified due to parsing error."],
                    "mitigation_strategies": ["Generic mitigation strategy."],
                    "safety_highlights": ["General safety practices applicable."]
                }

            simulated_risk_safety = {
                "project_id": project_id,
                "status": "risk_safety_assessment_complete",
                "risks": parsed_response.get("identified_risks"),
                "mitigation_strategies": parsed_response.get("mitigation_strategies"),
                "safety_highlights": parsed_response.get("safety_highlights")
            }
            logger.info(f"Risk/Safety Agent: Completed risk and safety assessment for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "risk_safety_assessment": simulated_risk_safety
            }

        except Exception as e:
            logger.error(f"Risk/Safety Agent: Error during risk/safety assessment: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed risk/safety assessment for {project_id}: {str(e)}"
            }