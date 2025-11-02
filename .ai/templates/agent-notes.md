# Agent Notes Template (YAML multi-document)

This template explains how the agent should record live notes for a session using a YAML multi-document file.

File to create for a session:

.ai/chat-sessions/<session-id>/agent-notes.yaml

Each document in that YAML file is a single note (an atomic record). Documents are separated by `---`.

Validation:

- Use the JSON Schema at `schemas/agent-notes.schema.v0.1.json` to validate each YAML document.

Session ID and ID conventions

- Session IDs MUST follow the canonical pattern `YYYYMMDD-NNN` (regex `^\\d{8}-\\d{3}$`) so session folders sort
  lexicographically. Example: `20251101-001`.
- Decision and action IDs SHOULD follow the patterns `DEC-nnn` and `ACT-nnn` respectively (e.g., `DEC-001`, `ACT-002`).
- ID sequencing policy: by default, IDs restart per session (e.g., each session begins with `DEC-001` and `ACT-001`).
  When referencing items externally, include the session-id (e.g., `20251101-001:DEC-001`).

Required fields for each note document:

- session_id: string (the session id)
- recorded_at: string (ISO 8601 timestamp)
- kind: string (one of: "note", "decision", "action", "timestamp")
- body: string (the content of the note)

Optional fields for decision or action kinds:

- id: string (e.g., DEC-001 or ACT-001)
- title: string
- rationale: string (for decisions)
- owner: string (for action items)
- due: string (YYYY-MM-DD)
- status: string (open | in-progress | done)

Example (YAML multi-document):

---

# session_id: 20251101-01

session_id: "20251101-01"
recorded_at: "2025-11-01T14:00:00Z"
kind: "timestamp"
body: "Session started"
---
session_id: "20251101-01"
recorded_at: "2025-11-01T14:05:12Z"
kind: "note"
body: "Reviewed governing docs; identified areas to align with conventions."
---
session_id: "20251101-01"
recorded_at: "2025-11-01T14:20:00Z"
kind: "decision"
id: "DEC-001"
title: "Use YAML session notes"
body: "Adopt a YAML multi-document file for session notes to enable atomic parsing."
rationale: "Simpler to parse and allows incremental appends."
---
session_id: "20251101-01"
recorded_at: "2025-11-01T14:25:00Z"
kind: "action"
id: "ACT-001"
title: "Add agent-notes schema"
body: "Create a JSON Schema for agent notes and store in schemas/"
owner: "wmclifford"
due: "2025-11-05"
status: "open"

Notes for the agent:

- Append new documents to the session `agent-notes.yaml` file as the session progresses. Each append should add a new
  YAML document beginning with `---`.
- Use deterministic ISO 8601 timestamps.
- Use the `id` prefix DEC- and ACT- for decisions and actions respectively.
- Keep the `body` field concise but sufficient to understand the context; include links if needed.
