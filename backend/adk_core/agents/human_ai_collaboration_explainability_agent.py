import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class HumanAICollaborationExplainabilityAgent(BaseConstructionAgent):
    """
    Facilitates effective communication and collaboration between human stakeholders
    and the AI agent system. It provides explanations of AI decisions,
    interfaces for human oversight, and channels for feedback.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Human-AI Collaboration & Explainability Agent",
            description="Facilitates human interaction, explains AI decisions, and manages feedback.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates preparing summaries and explanations for human stakeholders.
        """
        project_id = user_input.get("project_id")
        master_project_plan = user_input.get("master_project_plan", {})
        risk_safety_assessment = user_input.get("risk_safety_assessment", {})
        qa_plan = user_input.get("quality_assurance_plan", {})
        client_name = user_input.get("client_name", "Valued Client")

        logger.info(f"Human-AI Collaboration Agent: Preparing summary for human review for project {project_id}.")

        try:
            prompt = (
                f"As an AI system liaison, prepare a concise summary for human review "
                f"for a construction project. Consolidate key information from the master project plan, "
                f"risk and safety assessment, and quality assurance plan. "
                f"Explain the key findings clearly and suggest next human actions (e.g., 'review and approve'). "
                f"Address it to '{client_name}'. "
                f"\n\nMaster Project Plan: {json.dumps(master_project_plan, indent=2)}"
                f"\nRisk & Safety Assessment: {json.dumps(risk_safety_assessment, indent=2)}"
                f"\nQuality Assurance Plan: {json.dumps(qa_plan, indent=2)}"
                f"Output STRICTLY as a JSON object with keys 'summary_for_human' (string), "
                f"'key_findings' (list of strings), 'recommended_human_actions' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for human collaboration summary."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'summary_for_human' not in parsed_response or \
                   'key_findings' not in parsed_response or \
                   'recommended_human_actions' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected human collaboration format.")
            except json.JSONDecodeError:
                logger.error(f"Human-AI Collaboration Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "summary_for_human": "Summary generation failed due to parsing error. Please review raw agent outputs.",
                    "key_findings": ["Core data available in raw outputs."],
                    "recommended_human_actions": ["Manually review all agent outputs."]
                }

            simulated_human_collaboration_output = {
                "project_id": project_id,
                "status": "summary_for_human_review_prepared",
                "summary_text": parsed_response.get("summary_for_human"),
                "key_findings": parsed_response.get("key_findings"),
                "recommended_actions": parsed_response.get("recommended_human_actions")
            }
            logger.info(f"Human-AI Collaboration Agent: Prepared summary for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "human_collaboration_summary": simulated_human_collaboration_output
            }

        except Exception as e:
            logger.error(f"Human-AI Collaboration Agent: Error during summary generation: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed to prepare human collaboration summary for {project_id}: {str(e)}"
            }