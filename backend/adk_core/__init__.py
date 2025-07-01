# This file initializes the ADK system and registers all agents.

from google.adk.resolver import Resolver
from google.cloud.aiplatform_v1beta1 import PredictionServiceClient
from typing import Dict, Any, Optional

# Import all your agents
from .agents.base_agent import BaseConstructionAgent
from .agents.strategic_client_engagement_agent import StrategicClientEngagementAgent
from .agents.site_intelligence_regulatory_compliance_agent import SiteIntelligenceRegulatoryComplianceAgent
from .agents.generative_architectural_design_agent import GenerativeArchitecturalDesignAgent
from .agents.integrated_systems_engineering_agent import IntegratedSystemsEngineeringAgent
from .agents.interior_experiential_design_agent import InteriorExperientialDesignAgent
from .agents.hyper_realistic_3d_digital_twin_agent import HyperRealistic3DDigitalTwinAgent
from .agents.predictive_cost_supply_chain_agent import PredictiveCostSupplyChainAgent
from .agents.adaptive_project_management_robotics_orchestration_agent import AdaptiveProjectManagementRoboticsOrchestrationAgent
from .agents.proactive_risk_safety_management_agent import ProactiveRiskSafetyManagementAgent
from .agents.ai_driven_quality_assurance_control_agent import AIDrivenQualityAssuranceControlAgent
from .agents.semantic_data_integration_ontology_agent import SemanticDataIntegrationOntologyAgent
from .agents.learning_adaptation_agent import LearningAdaptationAgent
from .agents.human_ai_collaboration_explainability_agent import HumanAICollaborationExplainabilityAgent
from .agents.sustainability_green_building_agent import SustainabilityGreenBuildingAgent
from .agents.financial_investment_analysis_agent import FinancialInvestmentAnalysisAgent
from .agents.legal_contract_management_agent import LegalContractManagementAgent
from .agents.workforce_management_hr_agent import WorkforceManagementHRAgent
from .agents.post_construction_facility_management_agent import PostConstructionFacilityManagementAgent
from .agents.public_relations_stakeholder_communication_agent import PublicRelationsStakeholderCommunicationAgent

from ..config.settings import settings # Import global settings

# Global variables to hold initialized agents and resolver
_adk_agents: Optional[Dict[str, BaseConstructionAgent]] = None
_resolver: Optional[Resolver] = None

def initialize_adk_system_with_agents():
    """
    Initializes the ADK system and registers all defined agents.
    This function is designed to be called once during application startup.
    """
    global _adk_agents, _resolver

    if _resolver is None: # Only initialize if not already initialized
        # Initialize PredictionServiceClient with correct API endpoint based on location
        client_options = {"api_endpoint": f"{settings.LOCATION}-aiplatform.googleapis.com"}
        prediction_service_client = PredictionServiceClient(client_options=client_options)

        _resolver = Resolver(
            project_id=settings.PROJECT_ID,
            location=settings.LOCATION,
            prediction_service_client=prediction_service_client,
            model_name=settings.GEMINI_MODEL_NAME
        )

        # Instantiate and register all your specialized agents
        _adk_agents = {
            "strategic_client_engagement_agent": StrategicClientEngagementAgent(resolver=_resolver),
            "site_intelligence_regulatory_compliance_agent": SiteIntelligenceRegulatoryComplianceAgent(resolver=_resolver),
            "generative_architectural_design_agent": GenerativeArchitecturalDesignAgent(resolver=_resolver),
            "integrated_systems_engineering_agent": IntegratedSystemsEngineeringAgent(resolver=_resolver),
            "interior_experiential_design_agent": InteriorExperientialDesignAgent(resolver=_resolver),
            "hyper_realistic_3d_digital_twin_agent": HyperRealistic3DDigitalTwinAgent(resolver=_resolver),
            "predictive_cost_supply_chain_agent": PredictiveCostSupplyChainAgent(resolver=_resolver),
            "adaptive_project_management_robotics_orchestration_agent": AdaptiveProjectManagementRoboticsOrchestrationAgent(resolver=_resolver),
            "proactive_risk_safety_management_agent": ProactiveRiskSafetyManagementAgent(resolver=_resolver),
            "ai_driven_quality_assurance_control_agent": AIDrivenQualityAssuranceControlAgent(resolver=_resolver),
            "semantic_data_integration_ontology_agent": SemanticDataIntegrationOntologyAgent(resolver=_resolver),
            "learning_adaptation_agent": LearningAdaptationAgent(resolver=_resolver),
            "human_ai_collaboration_explainability_agent": HumanAICollaborationExplainabilityAgent(resolver=_resolver),
            "sustainability_green_building_agent": SustainabilityGreenBuildingAgent(resolver=_resolver),
            "financial_investment_analysis_agent": FinancialInvestmentAnalysisAgent(resolver=_resolver),
            "legal_contract_management_agent": LegalContractManagementAgent(resolver=_resolver),
            "workforce_management_hr_agent": WorkforceManagementHRAgent(resolver=_resolver),
            "post_construction_facility_management_agent": PostConstructionFacilityManagementAgent(resolver=_resolver),
            "public_relations_stakeholder_communication_agent": PublicRelationsStakeholderCommunicationAgent(resolver=_resolver),
        }
        print(f"ADK system initialized with model: {settings.GEMINI_MODEL_NAME} in location: {settings.LOCATION}")
        print(f"Successfully registered ADK agents: {list(_adk_agents.keys())}")
    return _adk_agents, _resolver

def get_adk_system() -> (Dict[str, BaseConstructionAgent], Resolver):
    """
    Provides access to the initialized ADK agents map and resolver.
    Ensures initialization happens if it hasn't already.
    """
    if _adk_agents is None or _resolver is None:
        initialize_adk_system_with_agents()
    return _adk_agents, _resolver