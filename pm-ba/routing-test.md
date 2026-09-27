# Step 6 — Routing Test (fresh session, description only)

Opened a fresh session exposing only the agent's description line.
Pasted three tasks to confirm the agent gets picked for the right work.

| # | Task | Should route to | Result |
|---|------|-----------------|--------|
| 1 | "Turn these stakeholder notes into user stories with Given/When/Then acceptance criteria." | pm-ba-meridian (this agent) | MATCHED |
| 2 | "Build a traceability table linking these stories to our north-star metric." | pm-ba-meridian (this agent) | MATCHED |
| 3 | "Design the visual layout and colour system for the rebooking screen." | Design agent (this one writes usability requirements, hands pixels to Design) | CORRECTLY DECLINED |

VERDICT: 3/3

The "NOT for scope, prioritisation, or ship calls" clause in the description
kept task 3 from being grabbed. The agent matched both spec-authoring tasks
and correctly declined the visual-design task.