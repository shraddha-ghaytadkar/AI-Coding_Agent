"""
Integration tests for AgentWorkflowOrchestrator.
"""
import os
import unittest
from orchestrator.factory import create_orchestrator
from core.models import WorkflowStep


class TestAgentOrchestrator(unittest.TestCase):
    def setUp(self):
        self.sample_dir = os.path.join(
            os.path.dirname(__file__), "..", "sample_codebases", "task_tracker"
        )
        self.orchestrator = create_orchestrator(force_mock=True)

    def test_full_agent_workflow_execution(self):
        task_prompt = "Add priority filtering method to TaskManager in service.py"
        state = self.orchestrator.execute(task_prompt, self.sample_dir)

        # 1. Workflow should reach COMPLETED
        self.assertEqual(state.current_step, WorkflowStep.COMPLETED)
        self.assertIsNone(state.error_message)

        # 2. Files should be scanned and AST extracted
        self.assertGreater(len(state.file_map), 0)
        self.assertGreater(len(state.ast_summaries), 0)

        # 3. Relevant files identified
        self.assertIsNotNone(state.relevance_result)
        self.assertGreater(len(state.relevance_result.selected_files), 0)

        # 4. Plan generated
        self.assertIsNotNone(state.plan)
        self.assertTrue(len(state.plan.markdown_plan) > 50)

        # 5. Patch generated with diffs
        self.assertIsNotNone(state.patch_result)
        self.assertGreater(len(state.patch_result.modified_files), 0)
        self.assertGreater(len(state.patch_result.diffs), 0)

        # 6. Validation executed
        self.assertIsNotNone(state.validation_result)
        self.assertTrue(state.validation_result.passed)


if __name__ == "__main__":
    unittest.main()
