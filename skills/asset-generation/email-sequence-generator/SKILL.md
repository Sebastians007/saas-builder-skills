---
name: email-sequence-generator
description: >
  Use this skill to write any multi-email sequence for a marketing funnel. This
  includes: nurture sequences, onboarding sequences, launch sequences, cart open
  and close sequences, reminder sequences, re-engagement sequences, win-back
  sequences, post-purchase sequences, webinar follow-up sequences, challenge
  daily emails, and flash sale sequences. Trigger whenever the user needs a
  series of emails for any marketing purpose.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "email", "nurture-sequence", "lifecycle"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Email Sequence Generator

Every email in a sequence should earn the right to the next one. You write
emails that get opened, get read, and get clicked — because they deliver real
value and speak to the reader like a person, not a platform.

---

## Sequence Types & Frameworks

### Nurture Sequence (post opt-in, 3–5 emails)
Goal: Build trust, demonstrate expertise, prime for the offer.

- **Email 1 (immediate):** Welcome + deliver the lead magnet. Set expectations
  for what's coming. One quick win.
- **Email 2 (Day 2):** Teach something useful related to their problem. No ask.
- **Email 3 (Day 3–4):** Story — yours or a client's. The transformation is
  possible. Soft mention of offer.
- **Email 4 (Day 5–6):** Social proof + direct offer introduction.
- **Email 5 (Day 7):** Last call / reason to act now.

### Onboarding Sequence (post-purchase, 3–5 emails)
Goal: Reduce buyer's remorse, get them started, build a success habit.

- **Email 1 (immediate):** Welcome + access/login details. Celebrate their
  decision. One thing to do right now.
- **Email 2 (Day 1):** Quick win walkthrough. Set them up for early success.
- **Email 3 (Day 3):** Common mistake to avoid. Positions you as a guide.
- **Email 4 (Day 5–7):** Community / support / check-in. Opens dialogue.
- **Email 5 (Day 10–14):** Results story from another customer. Reaffirms the
  purchase.

### Launch / Cart Open Sequence
Goal: Build excitement before cart opens, drive sales during open cart.

- **Pre-launch 1 (3–5 days before):** Tease the announcement. Curiosity hook.
- **Pre-launch 2 (1–2 days before):** Behind the scenes / story. Build
  anticipation.
- **Cart open (Day 0):** It's live. Full offer presentation. Direct CTA.
- **Value email (Day 1–2):** FAQ or objection-busting. Keep momentum.
- **Social proof (Day 3–4):** Early buyer results or testimonials.
- **Urgency (Day 5–6):** Limited time / bonus deadline reminder.
- **Last chance (Final day):** Cart closes tonight. One clear CTA. No new info.

### Webinar Reminder Sequence
- **Confirmation (immediate):** You're registered. Here's what to expect.
- **24-hour reminder:** "Tomorrow at [TIME]." Tease 1 thing they'll learn.
- **1-hour reminder:** "We go live in 60 minutes." Direct link.
- **Live now:** "We're starting. Join here." Short. Urgent.

### Webinar Follow-up — Attended
- **Email 1 (same day):** Replay link + key takeaway recap.
  IMPORTANT: If a webinar script was already produced in this session, use
  the actual teaching titles and stream names in the recap — do NOT leave
  [Brief recap of Stream 1] placeholders when you already know what was taught.
  The attended follow-up email should reference what the attendee actually saw.
- **Email 2 (Day 2):** Offer reminder with FAQ.
- **Email 3 (Day 3):** Last chance / bonus expiring.

### Webinar Follow-up — No-Show
- **Email 1 (next day):** "You missed it — here's the replay."
- **Email 2 (Day 2):** Summary of what they missed + offer intro.
- **Email 3 (Day 3):** Final replay access + offer deadline.

### Re-engagement Sequence (5–7 emails for cold lists)
Goal: Pattern interrupt → re-establish value → present offer → sunset.

- **Email 1:** Pattern interrupt. Unusual subject line. Ask a direct question.
- **Email 2:** Valuable content. No ask. Remind them why they subscribed.
- **Email 3:** Story — something that's changed or happened since they went cold.
- **Email 4:** Soft offer. "Here's what I have for you right now."
- **Email 5:** Urgency. "This is your last chance before I remove you."
- **Email 6 (optional):** Final warning. Transparent. "I'm cleaning my list."
- **Email 7:** Sunset email. They didn't respond. Unsubscribe them cleanly.

### Flash Sale Countdown Sequence
- **Announcement:** Sale is live. Here's what's on offer and why now.
- **Midpoint:** Reminder + a reason to act (testimonial, stat, story).
- **Last chance:** Closes tonight. One CTA. No new content.

### 5-Day Challenge Emails (daily)
Each daily email contains:
- Subject: Day [X]: [Action or insight title]
- Welcome / context (2–3 sentences)
- Today's lesson (short, specific, actionable)
- Today's challenge / action step (one clear thing to do)
- Preview of tomorrow
- CTA (community, reply, post their result)

---

## Output Format

For each email, provide:

```
### Email [N] — [Name/Purpose]
**Send timing:** [When relative to sequence start]
**Subject line:** [Primary]
**Subject line (B variant):** [Alternative test]
**Preview text:** [45–90 characters]

---
[Full body copy — complete and ready to paste]

---
**CTA:** [Link text] → [Destination]
```

---

## Rules
- One CTA per email. No exceptions.
- Subject lines: 35–55 characters ideal. Test curiosity vs. direct benefit.
- Preview text supports the subject — does not repeat it.
- Conversational tone. Write like a person, not a brand.
- Short paragraphs. 1–3 sentences max. White space is your friend.
- Never use "I hope this email finds you well" or any corporate opener.
- Open with a hook — a question, a bold statement, or a story fragment.
- `[PRICE]` for any price not provided. Never invent numbers.
- `[LINK]` for any URL not yet known.
- `[FIRST NAME]` for personalization tags.


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `trial-to-paid-converter` (S7-Growth) — the nurture sequence's later emails hand off directly into trial-to-paid conversion messaging for SaaS offers
- `thank-you-page-generator` — the sequence's first email and the thank-you page should tell one continuous story, not two disconnected onboarding experiences

### Fed By
- `lead-magnet-creator` — supplies the promised outcome the delivery email must fulfill
- `avatar-extraction` (S10-Copywriting) — supplies the language and objections the sequence needs to address

### Feedback Loop
If open rates are fine but click-through is low, the fix is usually CTA placement and specificity within each email, not subject lines — check that before rewriting the sequence from scratch.

```yaml
chain_metadata:
  skill_slug: "email-sequence-generator"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "trial-to-paid-converter"
    - "thank-you-page-generator"
    - "ab-test-generator"
```
