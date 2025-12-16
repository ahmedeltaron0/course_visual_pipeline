from app.service.ai_service import AgentService
from app.service.higgs_service import HiggsService

def get_agent_service():
    return AgentService()

def get_higgs_service():
    return HiggsService()
