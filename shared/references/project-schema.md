# Project State Schema

`project.json` is the durable source of truth for one brand, company, app, website, service, or product.

The schema is intentionally broad enough for different project types. Empty irrelevant sections are allowed in JSON but should be hidden in `hub.html`.

```json
{
  "schema_version": "5.0",
  "project": {
    "name": "",
    "type": "saas|web_app|website|brand|company|service|internal_tool|api|mobile_app|other",
    "status": "active|paused|launched|maintenance",
    "current_phase": "understand|discover|define|plan|execute|verify|launch|operate-grow",
    "summary": "",
    "direction": "",
    "geography": "",
    "existing_or_new": "existing|new"
  },
  "context": {
    "known_facts": [],
    "existing_assets": [],
    "existing_stack": [],
    "constraints": [],
    "non_goals": []
  },
  "research": {
    "market": {},
    "trends": [],
    "competitors": [],
    "evidence": [],
    "sources": [],
    "confidence": "low|medium|high",
    "gaps": []
  },
  "users": {
    "primary": [],
    "jobs_to_be_done": [],
    "problems": [],
    "current_alternatives": [],
    "evidence": []
  },
  "strategy": {
    "positioning_candidates": [],
    "selected_positioning": null,
    "differentiators": [],
    "usp_candidates": [],
    "offer": {},
    "business_model": {},
    "success_metrics": []
  },
  "planning": {
    "requirements": [],
    "scope_now": [],
    "scope_later": [],
    "roadmap": [],
    "architecture_decisions": [],
    "stack": [],
    "data_model": {},
    "ux_flows": [],
    "accessibility_requirements": [],
    "security_requirements": []
  },
  "marketing": {
    "relevant": false,
    "funnel": {},
    "messages": [],
    "copy_framework": null,
    "assets": []
  },
  "execution": {
    "work_items": [],
    "in_progress": [],
    "completed": [],
    "blocked": []
  },
  "verification": {
    "acceptance_criteria": [],
    "tests": [],
    "browser_checks": [],
    "security_findings": [],
    "accessibility_findings": [],
    "performance_findings": [],
    "release_blockers": []
  },
  "launch": {
    "environment": {},
    "deployment": {},
    "analytics": {},
    "monitoring": {},
    "release_status": ""
  },
  "operations_growth": {
    "health": {},
    "incidents": [],
    "feedback": [],
    "experiments": [],
    "growth_metrics": {},
    "retention": {},
    "next_review": null
  },
  "assumptions": [
    {
      "id": "A-001",
      "text": "",
      "confidence": "low|medium|high",
      "affects": [],
      "status": "open|confirmed|rejected"
    }
  ],
  "open_questions": [],
  "decisions": [
    {
      "id": "D-001",
      "date": "YYYY-MM-DD",
      "decision": "",
      "reason": "",
      "evidence": [],
      "reversible": true
    }
  ],
  "next_actions": []
}
```

## Update rules

1. Read the existing state before acting.
2. Never erase old decisions silently. Supersede them.
3. Distinguish facts from assumptions.
4. Attach sources/evidence to externally researched claims.
5. A specialist returns a patch; `project-state-manager` applies it.
6. `hub-renderer` never changes state.
7. User corrections outrank inferred assumptions.
8. Current code/product reality outranks stale planning documents.
