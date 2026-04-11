---
name: writing-docs
description: Use when adding, updating, or relocating Garage system documentation under docs/, especially when choosing between architecture, design, features, tasks, and wiki; deciding whether to update an existing source-of-truth doc; checking whether a docs edit needs coordinated changes across architecture/design/features; or assigning document IDs, filenames, H1 titles, and meta headers.
---

# Writing Docs

## Overview

`docs/` is the design source of truth for `Garage`.

The main failure mode is not "bad prose". It is **putting the right idea in the wrong place**, creating a second truth source when an existing document already owns that question, or updating one mainline doc while leaving related `architecture / design / features` docs semantically out of sync.

When writing Garage system docs, decide **placement first, then mainline consistency, then naming, then header format**.

## When to Use

Use this skill when:

- The user wants to "落盘" a `Garage` system document under `docs/`
- You need to choose between `architecture / design / features / tasks / wiki`
- You need to decide whether to update an existing doc or create a new one
- You are editing an existing `architecture`, `design`, or `features` doc and need to know whether adjacent mainline docs must move with it
- You need an exact doc ID, filename, H1, and meta header
- You are writing or reorganizing docs about `Garage` platform semantics, pack design, feature cuts, task breakdown, or reference knowledge

Do not use this skill when:

- The document belongs under `packs/*/skills/` or `.agents/skills/`
- The work is code implementation rather than system documentation
- The file is an external reference artifact under `references/`

## Core Pattern

Always decide in this order:

1. **Update vs new file**
2. **Correct directory**
3. **Mainline consistency sweep**
4. **Correct ID namespace**
5. **Correct filename**
6. **Correct H1 and meta header**

### 1. Update vs New

Default to **updating an existing document** if that document already owns the question.

Use these ownership rules first:

- `docs/README.md` owns docs tree structure, directory meanings, ID rules, naming rules, and formatting rules
- `docs/ROADMAP.md` owns feature map and `Fxxx` planning/indexing
- `docs/tasks/README.md` owns task ordering and the `Txxx` task index
- Existing same-topic docs own their stable question and should usually be extended instead of duplicated
- `docs/wiki/W120-ahe-workflow-externalization-guide.md` and `docs/wiki/W130-ahe-path-mapping-guide.md` already own AHE externalization/path-mapping guidance

Create a **new** document only when the user is introducing a genuinely new question that is not already owned by an existing doc.

### 2. Choose the Right Directory

| Directory | Put the doc here when it answers... | Do not put here when it is really... |
| --- | --- | --- |
| `docs/architecture/` | top-level `Garage` platform architecture, system boundaries, core subsystem boundaries, continuity architecture | pack-specific design, task breakdown, external reference |
| `docs/design/` | subsystem design or pack-specific detailed design | top-level platform architecture, stable cross-system feature semantics |
| `docs/features/` | stable capability cuts and shared system semantics, e.g. contracts, governance, bridge, runtime, artifact surfaces | pack-internal design, task execution plan |
| `docs/tasks/` | executable implementation decomposition and delivery sequencing | design rationale or long-form architecture discussion |
| `docs/wiki/` | external analysis, historical/background references, adoption notes, path mapping, supporting references | current main-line truth source |

### 3. Mainline Consistency Sweep

`architecture / design / features` together own the main system truth. If you change one of them, check whether the same topic is also expressed in the other two families before you write.

Use this minimum sweep:

- Start from the current doc's `关联文档` header and nearby same-topic filenames; use them as the first candidate set for the sweep
- If you change top-level boundaries, canonical objects, runtime topology, lifecycle ordering, or diagrams, check the same-topic docs in `docs/architecture/` and `docs/features/`
- If you change stable shared semantics in `docs/features/`, check whether `docs/architecture/` still describes the same boundary story and whether any relevant `docs/design/` detail now contradicts it
- If you change pack-specific or subsystem detail in `docs/design/`, make sure it does not silently contradict upstream `docs/architecture/` or `docs/features/`; if it does, update the upstream doc first or escalate that it must change first
- If adjacent docs stay correct, say so explicitly in your reasoning instead of assuming they are unaffected

Do not let `docs/tasks/` resolve these conflicts. `tasks` follow `architecture / features / design`; they do not override them.

### 4. Choose the ID Namespace

Use the current repo conventions:

- `Mxxx`: top-level main docs
- `Axxx`: architecture
- `Dxxx`: design
- `Fxxx`: features
- `Txxx`: tasks
- `Wxxx`: wiki

General rules:

- IDs are stable once assigned
- File ID, H1 ID, and meta ID must match
- Use the next coherent slot in the same family; do not renumber existing docs

### 5. Choose the Filename

Use the directory-specific filename pattern:

| Doc type | Filename rule |
| --- | --- |
| top-level main docs | keep canonical names such as `docs/README.md`, `docs/VISION.md`, `docs/GARAGE.md`, `docs/ROADMAP.md` |
| architecture | `Axxx-<slug>.md` |
| design | `Dxxx-<slug>.md` |
| features | `Fxxx-<slug>.md` |
| tasks index | `docs/tasks/README.md` |
| task docs | `Txxx-<title-slug>.md` |
| wiki | `Wxxx-<slug>.md` |

Do not use deleted categories like `docs/guides/` or `docs/plans/`.

Do not leave filename placeholders like `<repo-slug>` when the user asked for an exact path. Choose a concrete slug or ask one focused question before writing.

If the upstream project name is genuinely unspecified and the user still wants an exact path with no follow-up question, use a concrete generic slug such as `reference-upstream` rather than leaving a conditional note or placeholder.

### 6. Choose the H1 and Meta Header

All docs use:

```markdown
# ID: Title
```

And must include the matching ID line in the header, for example:

```markdown
# F010: Garage Shared Contracts

- Feature ID: `F010`
- 状态: 草稿
- 日期: 2026-04-11
```

Important:

- Mirror the **nearest same-directory exemplar**
- Do not invent a brand-new header schema for one file
- `tasks` often use `关联设计文档`
- `wiki` often omits `当前阶段`
- top-level main docs use `Document ID`

## Quick Reference

### Directory and Pattern Cheatsheet

| Need | Directory | Pattern | Nearby example |
| --- | --- | --- | --- |
| top-level doc tree rule | `docs/` | canonical filename + `Mxxx` header | `docs/README.md` |
| product philosophy / why | `docs/` | canonical filename + `Mxxx` header | `docs/VISION.md` |
| system/project main entry | `docs/` | canonical filename + `Mxxx` header | `docs/GARAGE.md` |
| feature index / roadmap | `docs/` | canonical filename + `Mxxx` header | `docs/ROADMAP.md` |
| top-level Garage architecture | `docs/architecture/` | `Axxx-<slug>.md` | `A110`, `A120`, `A130` |
| pack or subsystem detailed design | `docs/design/` | `Dxxx-<slug>.md` | `D020`, `D110`, `D120` |
| shared capability semantics | `docs/features/` | `Fxxx-<slug>.md` | `F010`, `F050`, `F110` |
| implementation breakdown | `docs/tasks/` | `Txxx-<title-slug>.md` | `T010`, `T120` |
| external or historical reference | `docs/wiki/` | `Wxxx-<slug>.md` | `W010`, `W120`, `W140` |

### Update Existing Before Creating New

If the request is about one of these, prefer updating:

- docs tree rules, naming, numbering, format: `docs/README.md`
- feature numbering / feature map: `docs/ROADMAP.md`
- task ordering / task table: `docs/tasks/README.md`
- AHE externalization guidance: `docs/wiki/W120-ahe-workflow-externalization-guide.md`
- AHE path mapping guidance: `docs/wiki/W130-ahe-path-mapping-guide.md`

### Mainline Consistency Cheatsheet

If the edit touches one of the mainline truth families, run this check before drafting:

- `architecture`: did the change alter boundaries, layers, canonical objects, or diagrams that `features` also names?
- `features`: did the change alter stable semantics, lifecycle, or object names that `architecture` or `design` also depends on?
- `design`: did the change alter pack or subsystem detail in a way that now conflicts with upstream `architecture` or `features`?
- If the answer is yes, update the adjacent owner docs or explicitly say which doc must change first

## Implementation

When the user asks to write a Garage system doc:

1. Restate the document's primary question in one sentence.
2. Check whether an existing doc already owns that question.
3. If yes, update that doc instead of creating a new one.
4. If the edit lands in `architecture / design / features`, inspect the same-topic docs in the other mainline directories, starting from `关联文档` and nearby same-topic docs.
5. If names, boundaries, lifecycle, diagrams, or cross-doc claims would drift, update those docs too or say which owner doc must change first.
6. If no existing doc owns the question, classify the new doc into `architecture / design / features / tasks / wiki`.
7. Pick the next stable ID in that namespace.
8. Generate one exact filename, one exact H1, and one exact header shape.
9. Match the header keys to the nearest same-directory exemplar.
10. Only then draft the body.

### One Worked Example

User asks:

> 我要补一篇文档，讲外部仓库采用 Garage/AHE workflow family 时怎么做 externalization 和 path mapping，给后来的 agent 当参考。

Correct move:

- **Do not** create a new umbrella file just because the request sounds broader
- First check `docs/wiki/W120-ahe-workflow-externalization-guide.md`
- Then check `docs/wiki/W130-ahe-path-mapping-guide.md`
- If the new content only deepens those existing questions, update one or both existing docs
- Only create a new wiki doc if the request introduces a truly new reference question that is not already owned by `W120` or `W130`

Why:

- `docs/` follows `一文一问`
- Creating a synthetic "single entry" doc can split truth and duplicate existing guidance

## Rationalization Table

| Rationalization | Reality |
| --- | --- |
| "I can leave `<repo-slug>` in the filename for now." | If the user asked for an exact path, choose a concrete slug or ask one focused question before writing. Do not ship placeholders into the truth source. |
| "I can make the path partly concrete and then add a conditional note." | Exact path requests still require one fully concrete answer. If the upstream name is unknown, use a stable generic slug like `reference-upstream`. |
| "This deserves a new summary doc so agents have one place to look." | If an existing doc already owns the question, update it. Duplicated entry docs split truth. |
| "This is system-related, so `architecture/` is probably fine." | `architecture/` is only for top-level Garage architecture and boundaries. Pack or subsystem detail belongs in `design/`; stable shared semantics belong in `features/`. |
| "I am only editing `features`, so `architecture` and `design` can catch up later." | If the edit changes names, boundaries, lifecycle, or other shared semantics, adjacent mainline docs must stay aligned now, or you must explicitly escalate which owner doc changes first. |
| "This is only a pack detail in `design`, so it can diverge from `features` for a while." | `design` can add detail, but it must not silently contradict upstream `architecture` or `features`. If it no longer fits, the mainline truth has to move intentionally. |
| "I can keep the header vague until later." | Header meta is part of retrieval and indexing. Choose a concrete, repository-consistent value now. |

## Red Flags

Stop and re-check if any of these happen:

- You are about to use `docs/guides/` or `docs/plans/`
- You are creating a new file before checking whether `docs/README.md`, `docs/ROADMAP.md`, `docs/tasks/README.md`, `W120`, or `W130` already owns the question
- Filename ID, H1 ID, and meta ID do not match
- You are using placeholders like `<slug>` or `(待定)` in a path or H1
- You are returning a conditional path like "use X, but replace it later if..."
- You are inventing a new header shape instead of copying the nearest same-directory pattern
- You changed `architecture`, `design`, or `features` without checking same-topic docs in the other mainline directories
- The edit changes object names, boundaries, lifecycle, or diagrams in one doc, but the neighboring owner docs still describe the old story

## Common Mistakes

- Putting pack-specific design into `docs/features/` instead of `docs/design/`
- Putting reference analysis into `docs/architecture/` instead of `docs/wiki/`
- Creating a brand-new doc for numbering rules instead of updating `docs/README.md`
- Using the old `garage-phase1-XX-...` pattern for task docs instead of `Txxx-<title-slug>.md`
- Creating a combined wiki entry that duplicates `W120` and `W130`
- Updating `docs/features/` semantics or terminology without checking whether related `docs/architecture/` docs now drift
- Updating `docs/design/` to reflect a new pack behavior that contradicts stable `docs/features/` semantics

