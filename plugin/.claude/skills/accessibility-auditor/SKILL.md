---
name: accessibility-auditor
description: >
  Checks a UI for basic accessibility problems — color contrast, keyboard
  navigation, missing alt text, and missing ARIA labels — before it ships.
  Use this skill when the user asks about "is this accessible", "check
  contrast on this page", "can this be used with a keyboard only", "does
  this need alt text", "accessibility check before launch", "will this
  pass a basic a11y review", or "someone using a screen reader, will this
  work for them".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "accessibility", "ui-review"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Testing
---

# Accessibility Auditor

Runs a practical, non-legalistic accessibility pass on a page or component: can it be read, can it be used with a keyboard, can it be understood by a screen reader. This is not a full WCAG audit — it's the baseline that keeps a small SaaS from locking out real users and from being an easy target for accessibility complaints.

## Stage
This skill belongs to Stage S4: Testing

## When to Use
- Before shipping any new page, form, or component with visible UI
- When a landing page or app UI is close to final and needs a pre-launch pass
- When a user mentions a customer or prospect who uses assistive tech
- As part of a pre-launch checklist alongside browser-verifier and security-review-lite
- When reusing a UI kit/template — templates are not automatically accessible

## Input Schema
```
target: string                  # page URL, component name, or pasted HTML/JSX
check_scope: [string] (optional) # e.g. ["contrast", "keyboard", "alt-text", "aria"]
has_browser_access: boolean (optional)  # can superpowers-chrome be used to check live?
```

## Workflow
### Step 1: Get the real markup or the real page
If a live URL is available and browser tooling is accessible, load the actual rendered page (ideally via the same browser-verifier mechanism) rather than reasoning from a design mockup — computed contrast and DOM structure matter more than the intended design.

### Step 2: Check color contrast
For every text/background pair, estimate contrast ratio against WCAG AA (4.5:1 for normal text, 3:1 for large text/UI components). Flag anything close to or under the line, especially common offenders: light gray text on white, placeholder text used as a label, disabled-looking buttons that are actually clickable.

### Step 3: Check keyboard navigation
Mentally (or via live browser tab-through if available) walk the page using only Tab/Shift+Tab/Enter/Space/Escape. Flag: anything only clickable with a mouse (div with an onClick and no button/role), focus order that jumps illogically, no visible focus outline, modal/dropdown that traps or loses focus, no way to close a modal with Escape.

### Step 4: Check images and icons
Every meaningful image needs alt text; every purely decorative image needs an empty alt (`alt=""`) so screen readers skip it. Icon-only buttons (a trash icon with no text) need an aria-label or visually-hidden text — flag every one found without it.

### Step 5: Check forms and ARIA
Every input needs an associated label (not just a placeholder). Error messages need to be programmatically associated with their field (aria-describedby) and ideally announced (aria-live or focus-move on submit failure). Custom components (dropdowns, tabs, modals built from divs) need appropriate ARIA roles/states, not just visual styling.

### Step 6: Prioritize findings
Sort into: blocks a user from completing the task (P0 — e.g. unlabeled required form field, unreachable-by-keyboard submit button) vs. degrades the experience (P1 — e.g. borderline contrast) vs. polish (P2 — e.g. missing landmark regions).

### Step 7: Self-Validation
- [ ] Every P0 finding would genuinely stop a keyboard-only or screen-reader user from completing the core task
- [ ] Contrast findings include the actual color values checked, not just "seems low"
- [ ] At least keyboard nav and alt text were checked, not just contrast (contrast alone is not a full pass)
- [ ] Findings are specific to elements (which button, which field), not generic ("improve accessibility")
- [ ] If the page couldn't be loaded live, this is stated and the audit is marked as markup-only, not verified-live

## Output Schema
```
{
  target: string,
  audit_method: "live_browser" | "markup_review",
  findings: [
    {
      id: string,
      category: "contrast" | "keyboard" | "alt_text" | "aria" | "forms",
      priority: "P0" | "P1" | "P2",
      element: string,
      issue: string,
      fix: string
    }
  ]
}
```

## Output Format
```markdown
# Accessibility Audit: [Target]

Method: [live browser / markup review]

## P0 — Blocks task completion
- [element]: [issue] → Fix: [specific fix]

## P1 — Degrades experience
- ...

## P2 — Polish
- ...

## Summary
X P0, X P1, X P2 found.
```

## Error Handling
- Can't load the live page → fall back to reviewing pasted markup/code, and say clearly that contrast especially can't be fully verified without rendering
- No specific scope given → run all four checks (contrast, keyboard, alt text, ARIA) by default rather than guessing which one matters
- Design system/UI library already claims accessibility compliance → verify anyway; libraries are often used in ways that break their own accessibility guarantees (e.g. missing labels added by the developer, not the library)
- User wants a full legal WCAG 2.2 AA compliance audit → clarify this skill gives a practical baseline pass, not a certified compliance audit, and recommend a specialized audit if legal compliance is the actual requirement
- Findings list is huge (legacy app never audited before) → still report everything, but group and lead with P0s so the founder isn't paralyzed by volume

## Examples
1. User: "check the signup form before launch" → Skill finds the password field has no visible label (placeholder-only), the submit button is a styled div with no button role, and error text isn't associated with the field. Outcome: keyboard/screen-reader users can now actually complete signup.
2. User: "is this landing page accessible" → Skill flags the hero CTA button text is white on a light-blue gradient below the 4.5:1 threshold in some areas. Outcome: color adjusted before launch instead of after a complaint.
3. User: "someone using a screen reader, will this dashboard work for them" → Skill finds icon-only nav buttons with no aria-label and a modal that doesn't trap focus or respond to Escape. Outcome: nav becomes usable without sight.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- browser-verifier (S4-Testing)
- ui-component-builder (S3-Building)
- in-app-nav-optimizer (S7-Growth)

### Fed By
- ui-component-builder (S3-Building)
- onboarding-flow-builder (S3-Building)

### Feedback Loop
Recurring findings (e.g. every form missing labels) should get fed back into ui-component-builder's default patterns so new components are built accessible from the start.

```yaml
chain_metadata:
  skill_slug: "accessibility-auditor"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "browser-verifier"
    - "ui-component-builder"
```
