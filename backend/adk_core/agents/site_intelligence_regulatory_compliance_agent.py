import json
import logging
from typing import Dict, Any

from .base_agent import BaseConstructionAgent
from ..services.gemini_service import GeminiService
from ..utils.common import format_output_json

logger = logging.getLogger(__name__)

class SiteIntelligenceRegulatoryComplianceAgent(BaseConstructionAgent):
    """
    Analyzes site data and regulatory constraints for a construction project.
    It simulates data retrieval (e.g., zoning, environmental risks) and uses Gemini
    to interpret common building codes and assess potential compliance challenges.
    """
    def __init__(self, resolver):
        super().__init__(
            name="Site Intelligence & Regulatory Compliance Agent",
            description="Analyzes site feasibility, zoning, and regulatory compliance.",
            resolver=resolver
        )
        self.gemini_service = GeminiService()
        # Mock data for site analysis and regulations. In a real application,
        # this would involve calling external APIs (e.g., geospatial services,
        # local government databases for zoning and building codes).
        self.mock_zoning_data = {
            "London, UK": {
                "residential": {"allowed_height_m": 12, "setbacks_m": {"front": 5, "sides": 3, "rear": 7}},
                "commercial": {"allowed_height_m": 20, "setbacks_m": {"front": 3, "sides": 1, "rear": 5}},
                "max_coverage_percent": 40,
                "environmental_risk": "Low (potential for minor soil contamination near old industrial sites)",
                "common_building_codes": "UK Building Regulations Part B (Fire Safety), Part M (Access to and use of buildings), Part L (Conservation of fuel and power)."
            },
            "New York, USA": {
                "residential": {"allowed_height_m": 150, "setbacks_m": {"front": 0, "sides": 0, "rear": 0}},
                "commercial": {"allowed_height_m": 300, "setbacks_m": {"front": 0, "sides": 0, "rear": 0}},
                "max_coverage_percent": 100,
                "environmental_risk": "Medium (urban heat island effect, historical underground infrastructure)",
                "common_building_codes": "NYC Building Code, ADA Compliance."
            },
            "Rural, California, USA": {
                "residential": {"allowed_height_m": 10, "setbacks_m": {"front": 10, "sides": 5, "rear": 10}},
                "commercial": {"allowed_height_m": 15, "setbacks_m": {"front": 8, "sides": 4, "rear": 8}},
                "max_coverage_percent": 25,
                "environmental_risk": "High (wildfire risk, seismic activity, water scarcity, protected species habitats)",
                "common_building_codes": "California Building Standards Code (Title 24), Wildland-Urban Interface (WUI) codes."
            }
        }

    def process_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs site analysis and regulatory compliance checks.
        """
        project_id = user_input.get("project_id") # Passed from Client Engagement Agent
        location = user_input.get("location")
        project_type = user_input.get("project_type")
        initial_requirements = user_input.get("parsed_data", user_input) # Get refined requirements

        logger.info(f"Site Intelligence Agent: Starting site analysis for project {project_id} at {location} for a {project_type} building.")

        try:
            # 1. Simulate Site Data Retrieval (replace with real API calls in production)
            # Selects mock data based on location, defaults if not found.
            site_info = self.mock_zoning_data.get(location, self.mock_zoning_data["London, UK"])
            
            zoning_rules = site_info.get(project_type, {})
            environmental_risk = site_info.get("environmental_risk", "Unknown")
            common_codes = site_info.get("common_building_codes", "Standard building codes apply.")

            # 2. Use Gemini for Regulatory Interpretation and Risk Assessment Summary
            regulatory_prompt = (
                f"Given the following site information and common building codes for a '{location}' located project "
                f"of type '{project_type}', summarize the key regulatory constraints and primary environmental risks. "
                f"Focus on aspects like maximum height, setbacks, and notable code sections. "
                f"Also, identify any potential compliance challenges given the initial requirements: {json.dumps(initial_requirements)}. "
                f"Site Info: {json.dumps(site_info)}"
                f"Format the output STRICTLY as a JSON object with keys like 'summary', 'compliance_challenges' (list of strings), 'recommendations' (list of strings)."
            )
            logger.info("Site Intelligence Agent: Calling Gemini for regulatory interpretation...")
            gemini_regulatory_response_str = self.gemini_service.generate_text(regulatory_prompt, temperature=0.2)

            if gemini_regulatory_response_str is None:
                return {
                    "agent_name": self.name,
                    "status": "error",
                    "message": "LLM did not generate a valid response for regulatory interpretation."
                }

            try:
                gemini_regulatory_parsed = json.loads(gemini_regulatory_response_str)
            except json.JSONDecodeError:
                logger.error(f"Site Intelligence Agent: Gemini regulatory response was not valid JSON: {gemini_regulatory_response_str}. Using fallback data.")
                gemini_regulatory_parsed = {
                    "summary": "Could not parse regulatory summary from AI. Manual review required.",
                    "compliance_challenges": ["AI parsing failed or response malformed."],
                    "recommendations": ["Consult local regulations directly for detailed compliance."]
                }

            # 3. Compile the comprehensive Site Feasibility Report
            site_feasibility_report = {
                "project_id": project_id,
                "location": location,
                "project_type": project_type,
                "status": "initial_analysis_complete",
                "zoning_data": {
                    "allowed_height_m": zoning_rules.get("allowed_height_m", "N/A"),
                    "setbacks_m": zoning_rules.get("setbacks_m", {}),
                    "max_coverage_percent": site_info.get("max_coverage_percent", "N/A")
                },
                "environmental_risk": environmental_risk,
                "common_building_codes": common_codes,
                "regulatory_summary_ai": gemini_regulatory_parsed.get("summary", "N/A"),
                "compliance_challenges_ai": gemini_regulatory_parsed.get("compliance_challenges", []),
                "site_recommendations_ai": gemini_regulatory_parsed.get("recommendations", [])
            }
            logger.info(f"Site Intelligence Agent: Generated Site Feasibility Report for {project_id}.")

            return {
                "agent_name": self.name,
                "status": "success",
                "site_feasibility_report": site_feasibility_report
            }

        except Exception as e:
            logger.error(f"Site Intelligence Agent: Error during site analysis: {e}", exc_info=True)
            return {
                "agent_name": self.name,
                "status": "error",
                "message": f"Failed site analysis for {project_id}: {str(e)}"
            }