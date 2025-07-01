import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class LegalContractManagementAgent(BaseConstructionAgent):
    """
    Manages all legal documentation, contracts, permits, and ensures compliance
    with local, national, and international regulations. It also assists in dispute resolution.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Legal & Contract Management Agent",
            description="Manages legal documents, contracts, and regulatory compliance.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provides high-level legal and contract considerations for the project.
        """
        project_id = user_input.get("project_id")
        location = user_input.get("location", "unspecified")
        project_type = user_input.get("project_type", "construction")
        site_report = user_input.get("site_feasibility_report", {})

        logger.info(f"Legal Agent: Assessing legal and contract aspects for project {project_id}.")

        try:
            prompt = (
                f"As a construction legal and contract management expert, outline key legal considerations "
                f"and common contract types for a '{project_type}' project in '{location}'. "
                f"Consider regulatory challenges mentioned in the site report: '{site_report.get('regulatory_summary_ai')}' "
                f"and potential compliance challenges: {', '.join(site_report.get('compliance_challenges_ai', []))}. "
                f"Suggest important contract clauses and necessary permits/licenses. "
                f"Output STRICTLY as a JSON object with keys 'legal_overview' (string summary), "
                f"'common_contract_types' (list of strings), 'key_contract_clauses' (list of strings), "
                f"'required_permits_licenses' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.5)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for legal/contract management."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'legal_overview' not in parsed_response or \
                   'common_contract_types' not in parsed_response or \
                   'key_contract_clauses' not in parsed_response or \
                   'required_permits_licenses' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected legal/contract format.")
            except json.JSONDecodeError:
                logger.error(f"Legal Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "legal_overview": "Legal assessment failed due to parsing error.",
                    "common_contract_types": ["Fixed Price", "Cost-Plus"],
                    "key_contract_clauses": ["Scope of Work", "Payment Terms"],
                    "required_permits_licenses": ["Building Permit", "Zoning Approval"]
                }

            simulated_legal_analysis = {
                "project_id": project_id,
                "status": "legal_assessment_complete",
                "legal_overview": parsed_response.get("legal_overview"),
                "common_contract_types": parsed_response.get("common_contract_types"),
                "key_contract_clauses": parsed_response.get("key_contract_clauses"),
                "required_permits_licenses": parsed_response.get("required_permits_licenses")
            }
            logger.info(f"Legal Agent: Completed legal and contract assessment for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "legal_contract_analysis": simulated_legal_analysis
            }

        except Exception as e:
            logger.error(f"Legal Agent: Error during legal/contract assessment: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed legal/contract assessment for {project_id}: {str(e)}"
            }