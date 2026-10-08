"""
Dependency Injection Factory for AI Coding Agent.
Assembles services into a cohesive orchestrator following Dependency Inversion Principle (DIP).
Binds xAI Grok provider dynamically.
"""
from typing import Optional
from core.config import get_config
from core.interfaces import ILLMProvider
from services.llm.grok import GrokLLMProvider
from services.llm.mock import MockLLMProvider
from services.inspector import CodebaseInspector
from services.relevance import RelevanceAnalyzer
from services.planner import ImplementationPlanner
from services.coder import CodeModificationEngine
from services.validator import SubprocessValidator
from orchestrator.workflow import AgentWorkflowOrchestrator, StepCallback


def create_orchestrator(
    api_key: Optional[str] = None,
    model_name: Optional[str] = None,
    timeout_seconds: Optional[int] = None,
    on_step_change: Optional[StepCallback] = None,
    force_mock: bool = False,
) -> AgentWorkflowOrchestrator:
    """
    Factory function to construct the fully-wired AgentWorkflowOrchestrator.
    Binds GrokLLMProvider directly with the configured xAI API key.
    """
    config = get_config()
    effective_key = (api_key or config.grok_api_key or "").strip()
    effective_model = model_name or config.grok_model
    effective_timeout = timeout_seconds or config.default_timeout_seconds

    llm_provider: ILLMProvider

    if force_mock:
        llm_provider = MockLLMProvider()
    else:
        llm_provider = GrokLLMProvider(api_key=effective_key, model_name=effective_model)

    # Wire up services with proper abstractions
    inspector = CodebaseInspector()
    relevance_analyzer = RelevanceAnalyzer(llm_provider=llm_provider)
    plan_generator = ImplementationPlanner(llm_provider=llm_provider)
    code_patcher = CodeModificationEngine(llm_provider=llm_provider)
    validator = SubprocessValidator(timeout_seconds=effective_timeout)

    return AgentWorkflowOrchestrator(
        inspector=inspector,
        relevance_analyzer=relevance_analyzer,
        plan_generator=plan_generator,
        code_patcher=code_patcher,
        validator=validator,
        on_step_change=on_step_change,
    )
