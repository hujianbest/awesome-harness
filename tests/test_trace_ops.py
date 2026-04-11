import tempfile
import unittest
from pathlib import Path

from bootstrap import summarize_execution_trace
from bootstrap.session_api import SessionApi
from core import GateVerdict
from execution import (
    ExecutionContext,
    ExecutionRequest,
    ExecutionRuntime,
    ExecutionStatus,
    ProviderAdapter,
    ProviderResponse,
    ToolCapability,
    ToolResult,
)
from foundation import WorkspaceBinding
from governance import GateType, GovernanceRule, GovernanceRuntime, GovernanceScope
from surfaces import FileBackedSurfaceManager


class _EchoProvider(ProviderAdapter):
    adapter_id = "provider.echo"

    def execute(self, request: ExecutionRequest, context: ExecutionContext) -> ProviderResponse:
        return ProviderResponse(output_text="done")


class TraceOpsTests(unittest.TestCase):
    def test_summarize_execution_trace_links_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = WorkspaceBinding.from_root("garage-test", Path(tmp_dir))
            runtime = ExecutionRuntime(
                governance=GovernanceRuntime(),
                surfaces=FileBackedSurfaceManager(workspace),
            )
            runtime.register_provider(_EchoProvider())
            runtime.tool_registry.register(
                ToolCapability(capability_id="workspace.read", description="r", allowed_pack_ids=("coding",)),
                lambda call, ctx: ToolResult(call_id=call.call_id, capability_id=call.capability_id, success=True, output="ok"),
            )
            outcome = runtime.execute(
                ExecutionRequest(
                    request_id="exec.traceops",
                    pack_id="coding",
                    node_id="n",
                    role_id="r",
                    provider_id="provider.echo",
                    prompt="p",
                ),
                ExecutionContext(
                    workspace_id=workspace.workspace_id,
                    session_id="session.x",
                    pack_id="coding",
                    node_id="n",
                    role_id="r",
                ),
            )
            summary = summarize_execution_trace(outcome)
            self.assertEqual(summary["traceId"], "trace.exec.traceops")
            self.assertEqual(summary["executionStatus"], ExecutionStatus.COMPLETED.value)
            self.assertEqual(summary["sessionId"], "session.x")
            self.assertEqual(summary["evidence"]["evidenceType"], "execution-trace")
            self.assertIsNotNone(summary["evidenceMaterialization"])
            self.assertTrue(Path(summary["evidenceMaterialization"]["filePath"]).exists())

    def test_session_api_summarize_step_outcome_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = WorkspaceBinding.from_root("garage-test", Path(tmp_dir))
            runtime = ExecutionRuntime(
                governance=GovernanceRuntime(
                    rules=(
                        GovernanceRule(
                            rule_id="block",
                            scope=GovernanceScope.NODE,
                            gate_type=GateType.ENTRY,
                            verdict=GateVerdict.NEEDS_APPROVAL,
                            rationale="r",
                            applies_to=("coding.n", "execution.block"),
                            missing=("approval",),
                        ),
                    )
                ),
                surfaces=FileBackedSurfaceManager(workspace),
            )
            runtime.register_provider(_EchoProvider())
            outcome = runtime.execute(
                ExecutionRequest(
                    request_id="exec.blocked",
                    pack_id="coding",
                    node_id="coding.n",
                    role_id="r",
                    provider_id="provider.echo",
                    prompt="p",
                    action_name="execution.block",
                ),
                ExecutionContext(
                    workspace_id=workspace.workspace_id,
                    session_id="session.x",
                    pack_id="coding",
                    node_id="coding.n",
                    role_id="r",
                ),
            )
        summary = SessionApi.summarize_step_outcome(outcome)
        self.assertEqual(summary["executionStatus"], ExecutionStatus.BLOCKED.value)
        self.assertEqual(summary["gateMissing"], ("approval",))


if __name__ == "__main__":
    unittest.main()
