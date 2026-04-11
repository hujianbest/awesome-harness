---
name: vision-obey
description: Use when proposing, reviewing, or implementing changes in Garage that may affect product direction, docs truth sources, runtime topology, core-versus-pack boundaries, governance artifacts, growth paths, bridge design, workspace surfaces, or provider placement, especially when a shortcut is described as temporary, harmless metadata, or implementation convenience.
---

# Vision Obey

## Overview

Use this skill to decide whether a Garage change still fits the current `docs/` truth sources.

Judge against the current docs, not a hypothetical future rewrite. If a proposal would only work after changing `architecture`, `features`, or `design` docs, the current verdict is `misaligned`, and the output should say which source-of-truth doc would need to change first.

## When to Use

- New docs, runtime, contract, pack, host adapter, governance, evidence, continuity, bridge, or topology changes
- Any proposal framed as `temporary shortcut`, `just metadata`, `just packaging`, `we can generalize later`, `backfill docs later`, or `only implementation convenience`
- Any change that moves boundaries between `core`, `packs`, `entry surfaces`, `runtime home`, `workspace`, `memory`, `skill`, `session`, `evidence`, or `growthProposal`

Do not skip this skill just because the change is small. Small boundary leaks are how the architecture drifts.

Do not use this skill for purely editorial wording changes that do not move system semantics, ownership, or runtime boundaries.

## Source-Of-Truth Order

1. Start with `docs/README.md`, `docs/VISION.md`, and `docs/GARAGE.md`.
2. Then read the owner docs for the proposed change.

| If the change touches | Read these first |
| --- | --- |
| Product direction or user priority | `docs/VISION.md`, `docs/GARAGE.md` |
| Docs ownership or task/design conflicts | `docs/README.md`, `docs/tasks/README.md` |
| Core vs pack vs entry vs host | `docs/architecture/A110-garage-extensible-architecture.md`, `docs/architecture/A120-garage-core-subsystems-architecture.md`, `docs/features/F010-shared-contracts.md`, `docs/features/F220-runtime-bootstrap-and-entrypoints.md`, `docs/features/F230-runtime-provider-and-tool-execution.md` |
| Continuity, growth, evidence, or governance | `docs/architecture/A130-garage-continuity-memory-skill-architecture.md`, `docs/features/F050-governance-model.md`, `docs/features/F060-artifact-and-evidence-surface.md`, `docs/features/F080-garage-self-evolving-learning-loop.md` |
| Runtime home vs workspace | `docs/features/F210-runtime-home-and-workspace-topology.md`, `docs/tasks/README.md` |
| Bridge or cross-pack handoff | `docs/architecture/A170-garage-cross-pack-bridge-architecture.md`, `docs/features/F120-cross-pack-bridge.md`, `docs/features/F010-shared-contracts.md` |

If a task doc conflicts with `architecture`, `features`, or `design`, trust `architecture / features / design` and treat the task doc as needing correction.

## Non-Negotiable Checks

Run every relevant proposal through these checks.

### 1. Vision Fit

- Does this still serve `solo creator` first?
- Does it preserve the AI team model instead of collapsing Garage into a single assistant or tool shell?

### 2. One Runtime, Many Entries

- Entry surfaces may differ in UX.
- They may not own private runtime semantics or private pack truth.

### 3. Core Stays Neutral

- `Garage Core` should understand neutral objects, not pack nouns such as `spec`, `diff`, or other domain terms.
- New capability should prefer packs, contracts, registration, and mapping.

### 4. Packs Declare Capabilities, Not Vendors

- Treat vendor and provider placement as a boundary check, not a tuning detail.
- If a pack manifest becomes the primary authority for vendor choice, that is `misaligned` unless the source-of-truth docs are changed first.
- Provider differences stay below core.

### 5. Workspace-First Facts

- `artifacts`, `evidence`, `sessions`, `archives`, and `.garage` are workspace facts.
- `runtime home` carries profile, cache, and install/runtime binding information. It does not swallow workspace truth.

### 6. Continuity Stays Layered

- `memory`, `session`, `skill`, `evidence`, and `growthProposal` are distinct.
- Reject "single history bucket" simplifications unless the docs themselves are deliberately changed first.

### 7. Growth Stays Evidence-First

- The canonical path is `evidence -> proposal -> governance -> update`.
- Do not bless direct auto-promotion just because it looks low-risk or reversible.

### 8. Governance Stays Artifact-First

- Rules, gates, review checklists, approvals, exceptions, and archive semantics must stay as explicit artifacts.
- Prompt text, code, or habits can enforce them, but must not become the only truth source.

### 9. Tasks Do Not Define The System

- `docs/tasks/` explains implementation slices.
- `docs/architecture/`, `docs/features/`, and `docs/design/` own the main system truth.

### 10. Bridge Is A Seam, Not A Privileged Contract

- Cross-pack bridge should compose existing contracts.
- Do not create a special `BridgeContract` unless the architecture docs are intentionally rewritten first.

## Decision Rule

- `aligned`: Fits current truth sources with no broken invariant.
- `borderline`: The docs are genuinely ambiguous, or the proposal can fit without moving a frozen system boundary.
- `misaligned`: Breaks a frozen invariant, or only becomes acceptable after hypothetical doc changes.

Important: do not upgrade a proposal to `borderline` or `aligned` just because it could be rewritten later. Judge the proposal as written.

## Output Template

Always return:

```markdown
## Vision Consistency Check
- Verdict: aligned | borderline | misaligned
- Scope: <what changed>
- Docs checked: <authoritative docs only>
- Broken invariants: <names, or `none`>
- Why:
  - <2-5 concrete findings>
- Smallest compliant rewrite:
  - <how to preserve the useful intent without breaking docs>
- Escalation:
  - `none`, or `update <doc-path>` before implementation
```

## Example

**Proposal:** Put `default model vendor` and `provider-specific knobs` in `PackManifest`, with host override support.

**Correct review shape:**

- Verdict: `misaligned`
- Why: packs declare capabilities, not vendors; provider choice lives below core and runtime binding; host override does not erase the boundary violation if the manifest remains primary authority
- Smallest compliant rewrite: keep required capabilities in the pack contract, move local defaults to runtime or host profile, or place them in clearly non-authoritative developer-experience metadata

## Red Flags: Stop And Verify

- "This is only metadata."
- "It is only a temporary shortcut."
- "We can generalize later."
- "We will backfill architecture docs later."
- "Runtime home already exists, so it can own workspace facts too."
- "Defaults are fine because host can override."
- "It is cleaner if bridge gets its own contract."
- "The rules live in prompts and code anyway."
- "It looks better in practice, so we do not need explicit evidence."

Any of these means: re-check the relevant source-of-truth docs before approving the change.

## Common Rationalizations

| Excuse | Reality |
| --- | --- |
| `只是 metadata / default` | If it changes authority or seam placement, it is architecture, not metadata. |
| `host 可以 override，所以 pack 默认 vendor 没问题` | Override does not fix a pack manifest becoming primary vendor authority. |
| `只是临时 shortcut` | Temporary boundary leaks still create drift against current truth sources. |
| `先写 task，架构之后补` | Tasks follow `architecture / features / design`; they do not own the main truth. |
| `runtime home 统一起来更方便` | Convenience does not let `runtime home` swallow workspace facts. |
| `规则写在 prompts 或 code 里就够了` | Governance in Garage is artifact-first and evidence-linked. |
| `再加一个 BridgeContract 更清晰` | Current docs deliberately keep bridge as a seam composed from existing contracts. |

## Common Mistakes

- Reading only `docs/tasks/`
- Citing broad principles without naming the owning doc
- Approving a change because "the docs could be updated later"
- Missing the distinction between `workspace facts` and `runtime home`
- Missing provider or vendor leakage into pack or core
- Treating `evidence` as optional because the change feels low risk
