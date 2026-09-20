---
name: lead-magnet-creator
description: >
  Use this skill to create an actual lead magnet deliverable — the thing the
  user gives away to build their list. Trigger when the user needs any of the
  following created as a real file or interactive experience: checklist, cheat
  sheet, quiz, scorecard, assessment, interactive quiz, calculator, ROI tool,
  pricing tool, lead magnet PDF, mini eBook, short guide, swipe file, template
  pack, copy swipe file, infographic, one-pager, full-length eBook, journal
  prompts PDF, worksheet, workbook, exercises, email course, email mini-course,
  5-day email series, or any free downloadable resource intended to attract
  subscribers. This skill produces the actual deliverable — not just the copy
  around it. Use alongside funnel-builder for complete lead magnet funnels.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "lead-magnet", "opt-in", "content-creation"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# Lead Magnet Creator

A lead magnet is only as good as the result it delivers. Your job is to
create the actual deliverable — a finished, polished file the user can hand
to a subscriber the moment they opt in. Not a template to fill in later. Not
a list of instructions. The real thing.

Nine formats are supported. Choose based on the content type and goal —
or ask if it's unclear.

---

## Format Selection Guide

| Content type | Best format |
|-------------|-------------|
| Step-by-step action items | PDF Checklist / Cheat Sheet |
| "Which one am I?" content | Interactive Quiz (HTML) |
| "How much / how long / what should I charge?" | Calculator / Tool (HTML) |
| Framework or visual system | Infographic (HTML) |
| 3–10 page educational guide | Mini eBook (PDF) |
| 20+ page comprehensive resource | Full-Length eBook (PDF) |
| Journal prompts, reflection questions | PDF Checklist / Cheat Sheet |
| Copywriting examples, scripts, templates | Swipe File / Template Pack (PDF) |
| Exercises, fill-in-the-blank, reflection | Worksheet / Workbook (PDF) |
| Teaching delivered over time via email | Email Course |
| Scorecard or self-assessment | Interactive Quiz (HTML) |

**Tie-breaker rules:**
- Can be absorbed in under 5 minutes → checklist, cheat sheet, or infographic
- Requires real reading → mini eBook or full eBook
- Value comes from personalization → quiz or calculator
- Recipient needs to *do* something, not just read → worksheet or email course
- Value is in the collection (examples, scripts, templates) → swipe file

---

## FORMAT 1 — Interactive Quiz (HTML)

The highest-converting lead magnet format. It qualifies the audience, delivers
personalized value, and converts at higher rates because the result feels
tailored to each person.

### What to build

A fully functional single-file HTML interactive quiz that:
- Walks the user through 5–10 questions
- Calculates a score or assigns a result segment
- Gates the result behind an email capture form
- Shows a personalized result page for each segment
- Works on mobile and desktop
- Is complete and functional — not a mockup

### Quiz Architecture

**Step 1 — Define result segments (2–4 segments)**

Based on the quiz topic, create 2–4 distinct result types. Each should:
- Have a memorable name ("The Builder", "The Optimizer", "The Visionary")
- Map to a specific profile or situation the reader will recognize
- Include a score range or answer pattern that leads to it
- Have a personalized 3–5 sentence result description
- Have a specific CTA ("Here's your next step...")

**Step 2 — Write 5–10 questions**

Each question should:
- Be easy to answer (no jargon, no hard thinking required)
- Reveal something real about the respondent
- Point naturally toward one of the segments
- Have 3–4 answer choices (not yes/no — too binary)

Use point values or answer tags to determine the result.

**Step 3 — Build the HTML file**

The quiz must include all of the following:

```
REQUIRED COMPONENTS:
- Welcome screen: title, promise, "Start Quiz" button
- Question screens: one at a time, progress bar, back/next navigation
- Email capture screen: "Get your personalized result" form
  (first name + email fields, privacy note)
- Result screen: segment title, personalized description, specific CTA
  and recommended next step
- Responsive CSS: works on mobile (375px min) and desktop
- Smooth transitions between screens (CSS fade or slide)
- Score calculation logic in JavaScript
```

**Design standards:**
- Clean, modern design — NOT the default browser look
- Use CSS custom properties (`--primary`, `--bg`, `--text`) so colors
  can be swapped easily
- Default palette: white background, dark navy text, brand accent color
  for buttons and progress bar
- Inter or system-sans-serif font (Google Fonts CDN acceptable)
- Selected answer highlights with a colored border and checkmark
- Progress bar shows question X of Y
- "Back" button on every question screen

**Email gate placement:** Before showing the result — not after. Copy:
"Enter your email to get your personalized [Quiz Topic] result" — not
"sign up for updates."

**HTML structure reference:**
```html
<div id="app">
  <div id="screen-welcome" class="screen active">...</div>
  <div id="screen-q1" class="screen">...</div>
  <!-- one div per question -->
  <div id="screen-email" class="screen">...</div>
  <div id="screen-result-a" class="screen">...</div>
  <!-- one result div per segment -->
</div>
<script>
  // State: currentQuestion, answers[], scores{}
  // Functions: startQuiz(), nextQuestion(), prevQuestion(),
  //   selectAnswer(), showEmailGate(), calculateResult(), showResult()
  // Form submit: validate → 1s loading → show correct result screen
  // TODO: Connect to [ESP] API or replace form action with your endpoint
</script>
```

**Output:** Save as `[topic-slug]-quiz.html`

---

## FORMAT 2 — Interactive Calculator / Tool (HTML)

The second most powerful HTML lead magnet. No right/wrong answers — just
inputs that produce a meaningful, personalized number or recommendation.
High perceived value because the output is immediately useful.

### What to build

A fully functional single-file HTML calculator where the user inputs their
situation and instantly sees a calculated result — a dollar amount, a score,
a timeline, a recommendation. Examples:

- "What Should You Charge?" → service pricing calculator
- "How Long Until You Can Retire?" → savings/timeline calculator
- "What's Your Revenue Leakage?" → lost income estimator
- "What's Your Marketing ROI?" → ad spend return calculator
- "How Much Is Your Time Worth?" → hourly rate / opportunity cost tool

### Calculator Architecture

**Step 1 — Define the inputs (3–7 fields)**

Use sliders, dropdowns, or number inputs. Each should:
- Be clearly labeled with a plain-English description
- Have sensible defaults pre-filled (so the result is visible immediately)
- Include a tooltip or helper text explaining what to enter if needed

**Step 2 — Define the output(s)**

One primary result (big, prominent number or label) and 2–3 supporting
results or breakdowns. Example: primary = "Your Recommended Rate: $X/hr",
supporting = "Annual income at this rate: $Y", "vs. market average: $Z".

**Step 3 — Add interpretation copy**

Below the result, show a short 2–3 sentence interpretation that changes
based on the output range. Low/medium/high thresholds each show different
guidance copy — this makes the tool feel like a real advisor, not just math.

**Step 4 — Email gate for the detailed report**

After showing the basic result, offer: "Get your full [Topic] Report
emailed to you" — first name + email → shows a more detailed breakdown
screen and/or triggers the email with the result embedded.

**Required components:**
```
- Clean header: tool name + one-line description of what it calculates
- Input section: labeled fields with real-time calculation on change
- Result section: primary result (large, prominent), supporting figures
- Interpretation copy: 2–3 sentences that shift by result range
- Email capture: "Get your detailed report" gate below the live result
- Mobile-responsive layout (inputs stack on small screens)
- All calculation in JavaScript — no server required
```

**Design standards:**
- Result number should be visually dominant (large font, accent color)
- Use range sliders where appropriate — more tactile than number inputs
- Show a simple bar or progress indicator for score-type outputs
- Same CSS variable system as the quiz format for easy rebranding
- Real-time recalculation as inputs change (no "Calculate" button needed)

**Output:** Save as `[topic-slug]-calculator.html`

---

## FORMAT 3 — PDF Checklist / Cheat Sheet

Best for: action-item lists, journal prompts, quick reference guides,
"things to do before X" content, and any resource consumed in one sitting.

### Target length
- Checklist: 1 page (letter or A4)
- Cheat sheet / reference: 1–2 pages
- Journal prompts: 1–2 pages

### Content requirements

Write the complete content including:
- Title (clear and specific — "The 10-Point Launch Checklist" not "Checklist")
- Subtitle (who it's for and what they'll accomplish)
- The full list (10–25 items for checklists; 5–15 for prompts)
- Brief intro sentence or context note (1–2 sentences max)
- Footer: brand name, website URL, and one CTA

For checklists: write each item as an action ("Confirm your tech stack
is tested" not "Tech stack"). For journal prompts: write each as a
complete, thoughtful question.

### PDF generation

Use the `pdf` skill. Specify:
- Clean two-column or single-column layout
- Checkbox squares for checklist items (□ or styled boxes)
- Brand accent color for header bar and section dividers
- White background, dark body text
- Logo placeholder at top (`[LOGO]`)

**Output:** Save as `[topic-slug]-checklist.pdf`

---

## FORMAT 4 — Worksheet / Workbook (PDF)

Best for: content that requires the reader to *do* something — fill in
answers, complete an exercise, map out their situation. Higher engagement
than a passive guide. Often used as "homework" before a call or class.

### Distinction from a checklist

A checklist is a reference you check off. A worksheet is something you
actively complete — it has blanks to fill in, prompts to respond to,
space for the reader's own thinking, and a logical flow that builds toward
an output (a plan, a score, a decision, a realization).

### Target length
- 2–6 pages
- Each page should have substantial white space for writing/filling in

### Required structure

```
Cover / Title page:
- Title + subtitle
- Instructions: "Complete this before [event/call/session]" or
  "Set aside 20 minutes to work through this"
- What you'll have when you're done (the output)

Section 1–N (one section per major exercise):
- Section title + 1–2 sentence framing ("Why this matters")
- The exercise prompt (clear, specific instruction)
- Lined or boxed space for written response
- Optional: example answer in a shaded "Example" box

Summary / Output page (final page):
- Synthesis prompt: "Based on your answers above, your [X] is:"
- A structured output space the reader fills in (their key insight,
  their plan, their score, etc.)
- CTA: "Now that you know [X], here's your next step: [URL]"
```

Write ALL prompts and framing copy — not just section labels. Each
exercise should have enough context that someone can complete it without
any additional instruction.

### PDF generation

Use the `pdf` skill. Specify:
- Generous line spacing and margins for writing space
- Exercise response areas as clearly delineated boxes or lined sections
- Example boxes in a light gray or pale brand-color background
- Section headers with a left-border accent (3px brand color)
- Logo and page numbers in footer

**Output:** Save as `[topic-slug]-worksheet.pdf`

---

## FORMAT 5 — Swipe File / Template Pack (PDF)

Best for: ready-to-use copy, scripts, subject line banks, DM templates,
ad hook libraries, proposal templates, and any collection where the value
is in having the actual text to adapt — not in learning a concept.

### Distinction from an eBook

An eBook teaches. A swipe file hands you the weapon. The reader's job is
to adapt, not to learn. Each item should be immediately usable with minimal
editing.

### Target length
- 5–20 pages depending on quantity
- Quality over quantity — 10 great templates beat 40 mediocre ones

### Required structure

```
Cover / Intro (1 page):
- Title + subtitle
- How to use this swipe file (2–3 sentences)
- "Replace [brackets] with your specifics"

Section 1–N (grouped by type or use case):
- Section header + brief context (when to use these)
- Each item labeled clearly (e.g., "Subject Line #1 — Curiosity Hook")
- The actual template text, formatted for easy scanning
- Optional: 1-line note on why it works / when to deploy it

Quick Reference Index (optional, for large packs):
- Table of contents organized by use case
```

Write ALL template items in full. Do not leave placeholder content within
the templates themselves beyond the bracketed variables the user must fill
in (e.g., `[OFFER NAME]`, `[PAIN POINT]`, `[RESULT]`).

**Aim for at least:**
- Subject line swipe files: 20–30 lines
- DM / cold outreach scripts: 5–10 complete scripts
- Ad hook libraries: 15–25 hooks with format labels
- Email templates: 5–10 complete emails
- Proposal templates: 1–3 complete frameworks

### PDF generation

Use the `pdf` skill. Specify:
- Clean, scannable layout — this is a reference doc, not a narrative
- Each template item in a lightly bordered box for visual separation
- Monospace or slightly differentiated font for the actual template text
  (distinguishes it from the surrounding explanation)
- Color-coded section headers if multiple categories
- "How to use" callout at the start of each section

**Output:** Save as `[topic-slug]-swipe-file.pdf`

---

## FORMAT 6 — Mini eBook / Guide (PDF)

Best for: "5 steps to X", "The beginner's guide to Y", "7 mistakes to
avoid", and resources that need real depth without being overwhelming.

### Target length
- 4–12 pages
- 800–2,500 words of body copy

### Required sections

```
Cover page: Title + subtitle + author name + brand
Introduction (½ page): Who this is for, what they'll get, your credibility
Main content (3–8 pages): 3–7 sections, each with:
  - Headline + 2–4 paragraphs + callout box (key takeaway or action)
Conclusion (½ page): Recap + one clear CTA
Back cover: About the author + CTA with URL
```

Write ALL body copy — finished, readable paragraphs throughout.

### PDF generation

Use the `pdf` skill:
- Designed cover with title treatment
- Section headers in brand color (H2 style, 18–22pt)
- Callout boxes: light background, border-left accent
- Body text: 11pt, 1.5 line height, dark gray
- Page numbers + brand URL in footer

**Output:** Save as `[topic-slug]-guide.pdf`

---

## FORMAT 7 — Full-Length eBook (PDF)

Best for: comprehensive guides, industry reports, "ultimate" resources,
and high perceived-value lead magnets for sophisticated audiences.

### Target length
- 15–40 pages
- 3,000–8,000 words of body copy

### Required structure

```
Cover page (designed)
Table of contents
Introduction: Who this is for + outcomes (1 page)
Chapter 1–5+: (3–6 pages each)
  - Chapter title + subtitle
  - Opening hook paragraph
  - Body with H3 subheadings
  - Callout boxes (tips, warnings, examples)
  - Chapter summary + 1–2 action items
Conclusion: What they now know + next step (1 page)
Resources (optional, ½ page)
About the author + CTA (1 page)
```

Write in full. Do not abbreviate chapters. Include real research,
frameworks, and examples — genuinely educational, not padded.

### PDF generation

Use the `pdf` skill in phases:
1. Generate full markdown content
2. Apply styling: chapter headers, running footer, callout boxes, cover
3. Output multi-page PDF with TOC links if supported

**Output:** Save as `[topic-slug]-ebook.pdf`

---

## FORMAT 8 — Infographic (HTML/SVG)

Best for: frameworks, processes, comparisons, "how it works" visuals,
and stat-heavy content that benefits from visual structure.

### What to build

A single-page HTML file (print-to-PDF friendly) with a real designed
layout. Must look like a designed asset — not a table with color.

### Layout types

- **Framework / Process:** Numbered steps in a flow with titles and
  1–2 sentence descriptions per step
- **Comparison:** Two or three columns (Before/After, Old Way/New Way)
  with ✗ and ✓ icons
- **Stats + insights:** Large stat numbers with context captions in a
  3–6 block grid
- **Visual checklist:** Category-grouped items with icons

### Design standards

- Full-bleed colored header with white title text
- White or off-white (#f8f9fa) body background
- Brand accent color for numbering, icons, and highlights
- Unicode or inline SVG icons — no external icon font dependencies
- Clean sans-serif font (system-ui or Inter from Google Fonts CDN)
- Fixed width: 800px (scales on mobile)
- All content visible without scrolling — one-page asset

**Output:** Save as `[topic-slug]-infographic.html`
Add note: "To export as PDF: open in Chrome → File → Print → Save as PDF
(Letter size, no margins)."

---

## FORMAT 9 — Email Course (Multi-Part Email Sequence)

Best for: teaching a framework or skill over time, training the open habit
before a pitch, or delivering value that requires spaced practice to stick.
The sequence *is* the lead magnet — no download file. Subscribers get
one lesson per day (or every other day) for 5–10 days.

### Distinction from a nurture sequence

A nurture sequence builds toward an offer. An email course IS the promise
— subscribers sign up specifically because they want the lessons. Each
email delivers a complete, standalone lesson. The offer is introduced
naturally at the end, not woven throughout.

### Structure

**Day 0 — Welcome / Orientation**
- Confirm they're enrolled, set expectations
- Preview the full curriculum (all lessons listed)
- One quick win or interesting fact to reward the opt-in immediately
- "Lesson 1 arrives tomorrow at [TIME]" — creates anticipation

**Days 1–5 (or 1–7, 1–10) — Daily Lessons**

Each lesson email:
- Subject line: "Day [N]: [Lesson Title]" (builds a habit of recognition)
- One focused lesson — concept + real example + one actionable takeaway
- 300–600 words (long enough to be valuable, short enough to finish)
- Ends with: preview of tomorrow's lesson ("Tomorrow we cover...")
- No hard pitch until the final lesson

**Final lesson — Lesson + Transition to Offer**
- Deliver the final teaching as promised
- Natural bridge: "Now that you have [X], the next level is [Y]..."
- Introduce the offer as the logical next step — not a pivot

### Content requirements

Write ALL emails in full — complete subject lines, preview text, and body
copy for every lesson. This is not a curriculum outline; it's the finished
email content, ready to load into an ESP.

Use the `email-sequence-generator` skill output format for each email:
```
### Day [N] — [Lesson Title]
**Subject:** [Subject line]
**Preview text:** [45–90 chars]
---
[Full body copy]
---
**CTA:** [Link text] → [Destination or placeholder]
```

**Output:** Deliver as a markdown document: `[topic-slug]-email-course.md`
Include a setup note at the top: "Load these into your ESP in sequence,
starting with Day 0 immediately on opt-in. Set Day 1 for +1 day, Day 2
for +2 days, etc."

---

## Integration with the Funnel Builder

When `lead-magnet-creator` is used as part of a Lead Magnet, Quiz, or
Email Course funnel:

1. **Build the deliverable first** — before any funnel pages or emails
2. **Reference the actual content in funnel copy** — the opt-in page
   headline should mention specific items (quiz result types, checklist
   items, lesson titles, calculator outputs). Never use generic
   "you'll get a free guide" language when the specifics are known.
3. **The delivery email should link directly to the file** — use
   `[DELIVERABLE DOWNLOAD LINK]` placeholder in the placeholder map.
   For email courses, the delivery mechanism is the sequence itself —
   note this in the funnel overview.

---

## Output Rules

- **Build the full content** — no "fill this in later" sections
- **Functional over decorative** — for HTML outputs, all interactive
  elements must work before delivery
- **Mobile-first** — all HTML outputs must work on a 375px screen
- **One file for HTML formats** — self-contained, no external
  dependencies except Google Fonts CDN
- **Use `[PLACEHOLDER]` only for things the user must supply:**
  `[LOGO_URL]`, `[BRAND_COLOR]`, `[FORM_ENDPOINT]`, `[DOWNLOAD_LINK]`
- **Name files with a descriptive slug:**
  `income-stacking-quiz.html`, `5-journal-prompts-checklist.pdf`,
  `options-trading-guide.pdf`, `marketing-audit-worksheet.pdf`,
  `dm-scripts-swipe-file.pdf`, `roi-calculator.html`,
  `email-marketing-course.md`

---

## PDF Technical Standards (Apply to ALL PDF outputs)

These rules prevent the most common PDF quality failures — content overflowing
table cells, text disappearing off page edges, and layout that looks amateur.
Follow every rule below whenever generating a PDF with ReportLab.

### Rule 1 — Always Use Paragraph Objects in Table Cells

Plain strings in ReportLab table cells **do not wrap**. They overflow off the
page edge and silently disappear. Every table cell must use a `Paragraph()`
object, no exceptions.

```python
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()

# WRONG — text will overflow off the page:
data = [['Column A', 'This long sentence will run past the right margin and be cut off']]

# CORRECT — text wraps inside the cell:
data = [
    [Paragraph('Column A', styles['Normal']),
     Paragraph('This long sentence will wrap correctly inside the cell', styles['Normal'])]
]
```

### Rule 2 — Always Set Explicit Column Widths

Never let ReportLab auto-size table columns. Always provide `colWidths` that
sum to the usable page width (468pt for a letter page with 1-inch margins).

```python
from reportlab.lib.pagesizes import letter
PAGE_W, PAGE_H = letter          # 612 x 792 pt
MARGIN = 72                       # 1 inch
USABLE_W = PAGE_W - 2 * MARGIN   # 468 pt

# Example: 3-column table with proportional widths
col_widths = [USABLE_W * 0.25, USABLE_W * 0.50, USABLE_W * 0.25]
table = Table(data, colWidths=col_widths)
```

### Rule 3 — Standard Table Style (use as base for all tables)

```python
from reportlab.lib import colors

table.setStyle(TableStyle([
    # Header row styling
    ('BACKGROUND',     (0, 0), (-1, 0),  colors.HexColor('#1a2540')),
    ('TEXTCOLOR',      (0, 0), (-1, 0),  colors.white),
    ('FONTNAME',       (0, 0), (-1, 0),  'Helvetica-Bold'),
    # All cells
    ('FONTSIZE',       (0, 0), (-1, -1), 9),
    ('ALIGN',          (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN',         (0, 0), (-1, -1), 'TOP'),    # TOP is critical for wrapped text
    ('LEFTPADDING',    (0, 0), (-1, -1), 8),
    ('RIGHTPADDING',   (0, 0), (-1, -1), 8),
    ('TOPPADDING',     (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING',  (0, 0), (-1, -1), 6),
    # Alternating row colors (start from row 1 to skip header)
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
    # Grid lines
    ('GRID',           (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ('LINEBELOW',      (0, 0), (-1, 0),  1.5, colors.HexColor('#0a0f1e')),
]))
```

### Rule 4 — Document Setup with Explicit Margins

```python
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    leftMargin=72,    # 1 inch
    rightMargin=72,   # 1 inch
    topMargin=72,     # 1 inch
    bottomMargin=72,  # 1 inch
)
```

### Rule 5 — Body Text: Use ParagraphStyle with Adequate Leading

```python
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

body_style = ParagraphStyle(
    'BodyText',
    parent=styles['Normal'],
    fontSize=10,
    leading=16,           # Always >= fontSize + 4; never below fontSize + 2
    spaceAfter=8,
    textColor=colors.HexColor('#1e293b'),
)
# Always use Paragraph() for flowing text — never drawString() for body copy
story.append(Paragraph('Your body text here...', body_style))
```

### Rule 6 — Checklist Items: Two-Column Table, Not Manual Positioning

Never try to position a checkbox character next to text using `drawString()`.
Use a two-column table so both elements wrap and align correctly.

```python
from reportlab.lib.styles import ParagraphStyle

item_style = ParagraphStyle('Item', parent=styles['Normal'], fontSize=10, leading=14)
box_style  = ParagraphStyle('Box',  parent=styles['Normal'], fontSize=10, leading=14)

rows = [
    [Paragraph('☐', box_style), Paragraph(item, item_style)]
    for item in checklist_items
]
checklist_tbl = Table(rows, colWidths=[18, USABLE_W - 18])
checklist_tbl.setStyle(TableStyle([
    ('VALIGN',         (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING',    (0, 0), (-1, -1), 0),
    ('RIGHTPADDING',   (0, 0), (-1, -1), 4),
    ('TOPPADDING',     (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING',  (0, 0), (-1, -1), 3),
]))
```

### Pre-flight Checklist Before Saving Any PDF

- [ ] Every table cell uses `Paragraph()` — no plain strings in tables
- [ ] All `colWidths` values sum to ≤ 468pt
- [ ] `VALIGN='TOP'` is set on every table
- [ ] No `drawString()` for body or label text longer than ~20 characters
- [ ] All `leading` values are `>= fontSize + 4`
- [ ] Document margins are set explicitly in `SimpleDocTemplate()`

---

## Cover Image Generation

Every PDF lead magnet (Mini eBook, Full-Length eBook, Worksheet, Swipe File)
should include a polished cover image. There are two scenarios:

### Scenario A — User Uploaded a Cover Image

If the user has attached a book cover, product photo, or branded design image,
**use it** as the cover page of the PDF. Do not generate a new cover.

For Book Funnel ebooks where the user uploads a flat cover:
- Embed the cover image as the first page of the PDF
- Also offer to generate a 3D CSS mockup or Pillow PNG version for use on the
  sales page and in social posts (see the `funnel-builder` Image Assets section
  for the full code)

### Scenario B — No Cover Provided (Generate One)

When no image is provided, generate a cover page using Pillow. This cover gets:
- Embedded as the first page of the PDF via ReportLab's `Image()` element
- Saved as a separate PNG the user can use on opt-in pages and in social posts

**Cover generation approach:**

The full Pillow code is in the `funnel-builder` skill under "Lead Magnet Cover
Image." Call it with the lead magnet title, subtitle, and the user's brand
colors if provided. If no brand colors were given, use a professional default
palette:

| Element | Default color |
|---------|--------------|
| Background | `#1a2744` (deep navy) |
| Accent bars / divider | `#c9a84c` (gold) |
| Title text | `#ffffff` (white) |
| Subtitle text | `#c9a84c` (gold) |

After generating the cover PNG:
1. Embed it as the first page in the PDF: `story.insert(0, Image(cover_path, width=USABLE_W, height=USABLE_W * 1.375))`
2. Note the PNG path in the output so the user can use it for the opt-in page
3. Include in Page Notes: "Use `[lead-magnet-name]-cover.png` as the hero visual on your opt-in page."

### Where Cover Images Get Used

| Asset | How the cover is used |
|-------|----------------------|
| PDF lead magnet | Page 1 of the document |
| Opt-in page | Hero visual (float right on desktop, full-width on mobile below headline) |
| Social posts | Featured visual in the lead magnet announcement post |
| Email delivery | Header image in the delivery email |
| Confirmation page | Visual confirmation of what was just received |

Always save the cover PNG with a clean slug filename: `[lead-magnet-title-slug]-cover.png`


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `funnel-builder-orchestrator` (S3-Funnel-Build) — the lead magnet is the core asset a Lead Magnet / Opt-in funnel build is built around
- `landing-page-generator` — delivers the lead magnet's value proposition and format details needed to write the opt-in page
- `email-sequence-generator` — the lead magnet's promised outcome sets up the delivery and nurture sequence that follows

### Fed By
- `avatar-extraction` (S2-Audience-Positioning) — supplies the target audience's pains and desires the lead magnet topic must match
- `offer-extraction` (S2-Audience-Positioning) — supplies the core offer the lead magnet should logically lead into

### Feedback Loop
If opt-in rate stays low after the page and traffic are ruled out, the fix is usually the lead magnet's promised outcome, not its format — revisit the topic and headline before switching from PDF to checklist to video.

```yaml
chain_metadata:
  skill_slug: "lead-magnet-creator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "funnel-builder-orchestrator"
    - "landing-page-generator"
    - "email-sequence-generator"
```
