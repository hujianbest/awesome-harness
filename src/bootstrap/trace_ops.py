"""Operator-facing execution trace and evidence summaries (T201)."""

from __future__ import annotations

from typing import Any

from execution import ExecutionOutcome

from .credential_resolution import metadata_str
from redaction import redact_text


def summarize_execution_trace(outcome: ExecutionOutcome) -> dict[str, Any]:
    """
    Serialize execution outcome for ops / Web: trace, gate checkpoint, evidence pointers.

    Secret material is redacted using execution context credential values when present.
    """

    trace = outcome.trace
    checkpoint = outcome.checkpoint
    ctx = outcome.context
    record = outcome.evidence_record
    lineage = outcome.evidence_lineage
    route = outcome.evidence_route
    creds = ctx.credential_values

    events: list[dict[str, Any]] = []
    for ev in trace.events:
        events.append(
            {
                "eventId": ev.event_id,
                "eventType": ev.event_type.value,
                "message": redact_text(ev.message, known_values=creds),
                "metadata": metadata_str(ev.metadata, known_secrets=creds),
            }
        )

    tool_summaries = tuple(
        {
            "callId": tr.call_id,
            "capabilityId": tr.capability_id,
            "success": tr.success,
            "outputPreview": redact_text(tr.output[:200], known_values=creds),
        }
        for tr in outcome.tool_results
    )

    return {
        "traceId": trace.trace_id,
        "executionStatus": trace.status.value,
        "requestId": outcome.request.request_id,
        "sessionId": ctx.session_id,
        "packId": ctx.pack_id,
        "nodeId": ctx.node_id,
        "roleId": ctx.role_id,
        "providerId": outcome.request.provider_id,
        "gateVerdict": checkpoint.verdict.value,
        "gateMissing": checkpoint.missing,
        "events": events,
        "toolResults": tool_summaries,
        "evidence": {
            "evidenceId": record.evidence_id,
            "evidenceType": record.evidence_type,
            "sourcePointer": record.source_pointer,
            "outcomeOrVerdict": record.outcome_or_verdict,
        },
        "lineage": {
            "linkId": lineage.link_id,
            "linkType": lineage.link_type.value,
            "sourceRef": {"kind": lineage.source_ref.kind, "objectId": lineage.source_ref.object_id},
            "targetRef": {"kind": lineage.target_ref.kind, "objectId": lineage.target_ref.object_id},
        },
        "evidenceMaterialization": (
            {
                "surface": route.surface.value,
                "filePath": str(route.file_path),
            }
            if route is not None
            else None
        ),
        "finalOutputPreview": (
            redact_text(outcome.response.output_text[:240], known_values=creds)
            if outcome.response is not None
            else None
        ),
    }
