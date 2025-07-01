import logging
import json
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class SemanticDataIntegrationOntologyAgent(BaseConstructionAgent):
    """
    Manages and integrates all project data from disparate sources, ensuring data
    consistency, semantic interoperability, and providing a unified view of
    project information through an ontology or knowledge graph.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Semantic Data Integration & Ontology Agent",
            description="Manages project data integration and semantic consistency.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulates identifying key data entities and suggesting integration points and ontologies.
        """
        project_id = user_input.get("project_id")
        # Collect various outputs to describe the data to be integrated
        agent_outputs_summary = {
            "client_requirements": user_input.get("parsed_data", {}).keys(),
            "site_report_keys": user_input.get("site_feasibility_report", {}).keys(),
            "architectural_keys": user_input.get("architectural_concept", {}).keys(),
            "system_design_keys": user_input.get("system_design", {}).keys(),
            "experiential_design_keys": user_input.get("experiential_design", {}).keys(),
            "cost_keys": user_input.get("cost_supply_chain_analysis", {}).keys(),
            "schedule_keys": user_input.get("estimated_schedule", {}).keys(),
            # Add other relevant keys from other agents as they are added
        }

        logger.info(f"Data Integration Agent: Analyzing data sources for project {project_id}.")

        try:
            prompt = (
                f"As a semantic data integration and ontology expert for construction projects, "
                f"analyze the following data entities and types generated for project '{project_id}': "
                f"{json.dumps(agent_outputs_summary, indent=2)}. "
                f"Suggest key data domains (e.g., BIM, GIS, Cost, Schedule, HR), "
                f"potential data integration challenges, and propose relevant construction ontologies "
                f"(e.g., IFC, buildingSMART Data Dictionary, W3C BOT Ontology) for semantic interoperability. "
                f"Output STRICTLY as a JSON object with keys 'data_domains' (list of strings), "
                f"'integration_challenges' (list of strings), 'suggested_ontologies' (list of strings)."
            )
            llm_response = self.gemini_service.generate_text(prompt, temperature=0.3)

            if llm_response is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for data integration."
                }

            try:
                parsed_response = json.loads(llm_response)
                if not isinstance(parsed_response, dict) or \
                   'data_domains' not in parsed_response or \
                   'integration_challenges' not in parsed_response or \
                   'suggested_ontologies' not in parsed_response:
                    raise ValueError("LLM response JSON is not in the expected data integration format.")
            except json.JSONDecodeError:
                logger.error(f"Data Integration Agent: Gemini response was not valid JSON: {llm_response}. Using fallback data.")
                parsed_response = {
                    "data_domains": ["Design", "Cost", "Schedule"],
                    "integration_challenges": ["Data silos", "Format incompatibility"],
                    "suggested_ontologies": ["IFC (Industry Foundation Classes)"]
                }

            simulated_data_integration = {
                "project_id": project_id,
                "status": "data_integration_analysis_complete",
                "data_domains_identified": parsed_response.get("data_domains"),
                "potential_integration_challenges": parsed_response.get("integration_challenges"),
                "recommended_ontologies": parsed_response.get("suggested_ontologies")
            }
            logger.info(f"Data Integration Agent: Completed data integration analysis for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "data_integration_analysis": simulated_data_integration
            }

        except Exception as e:
            logger.error(f"Data Integration Agent: Error during data integration analysis: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed data integration analysis for {project_id}: {str(e)}"
            }