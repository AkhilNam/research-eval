# Research Eval

A Claude plugin and portable skill that reviews a paper draft for a conference, workshop, or journal. It returns an overall recommendation, evidence-based reviewer comments, confidence, author questions, and prioritized revisions.

The skill aims to reduce bias through explicit venue criteria, identity-independent judgment, and manuscript-grounded comments. It cannot guarantee an unbiased result or predict a real acceptance decision.

## Use in Claude Code

From this repository, launch:

```sh
claude --plugin-dir .
```

Then invoke the skill inside Claude Code:

```text
/research-eval:review-paper Review ./draft.pdf for <venue, year, and track>. Use the official reviewer guide at <URL>.
```

Replace the angle-bracket fields with the actual target. The review guide is optional; the skill looks for public official guidance when browsing is available. You can also supply a local call for papers or review form.

```text
/research-eval:review-paper Review ./paper.tex for the attached workshop call. The appendix and bibliography are in the same folder. Focus on the current draft's readiness for submission.
```

For a downloaded plugin archive, extract `dist/research-eval-plugin.zip` and launch `claude --plugin-dir /path/to/research-eval`. The path must point to the extracted directory containing `.claude-plugin/` and `skills/`.

For a standalone personal skill instead, copy `skills/review-paper/` into `~/.claude/skills/review-paper/` and invoke `/review-paper`. Choose one installation method to avoid duplicate skill discovery. These paths and invocation conventions follow [Claude Code's skills documentation](https://code.claude.com/docs/en/skills) and [plugin creation documentation](https://code.claude.com/docs/en/plugins/create).

## Use in Claude chat

Upload [dist/review-paper.zip](dist/review-paper.zip) through **Customize → Skills → + → Create skill → Upload a skill**, enable it, then attach the draft and name the target venue. See [Anthropic's skill upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude) for availability and setup requirements. Example request:

```text
Review the attached draft for <journal and article type>. Give a candid recommendation, reviewer comments, and the changes that would most affect the decision. The journal's scope and review criteria are attached.
```

The same source skill works in both formats. It requires no API keys, hooks, MCP servers, or custom executable runtime. Reading PDFs and looking up public guidance use the tools available in your Claude environment; if those capabilities are unavailable, it reports the limitations.

## What a review contains

- A verified venue-native recommendation when available. Otherwise: **Strong accept, Accept, Weak accept, Weak reject, Reject, or Strong reject** using the included fallback definitions.
- For journal workflows, an editorial recommendation such as major revision kept separate from the simulated accept/reject judgment.
- A neutral summary, applicable quality dimensions, specific strengths and weaknesses, and questions for the authors.
- Evidence locations, concern severity, confidence, and an ordered revision plan.
- A coverage note and sources for venue criteria. An abstract-only or materially unreadable draft gets **Insufficient information**, with a partial assessment instead of a fabricated paper-level verdict.

The reviewer does not use author prestige as evidence, force positive/negative comment quotas, invent citations or numerical acceptance probabilities, or send draft content to public search engines. Novelty judgments remain qualified unless the relevant literature was actually checked. It reviews the draft as submitted and does not modify it.

## Build and validate

Python 3.9+ builds the two ZIP files with the standard library:

```sh
python3 scripts/package.py
claude plugin validate . --strict
```

The packager includes only explicitly listed release files, so unrelated manuscripts, evaluation outputs, credentials, and Git history stay out of the archives. Rebuild after changing the skill, references, manifest, or this README. The plugin archive contains the README for usage; its references to the repository's `dist/` and development scripts apply to the full source checkout.

[evals/behavioral-cases.md](evals/behavioral-cases.md) provides manual behavioral checks, including a strong paper, an invalid evaluation, venue-dependent scope, incomplete inputs, journal decisions, reputation bias, and manuscript prompt injection. Manifest/archive validation checks packaging, not review quality. Behavioral cases require actual model runs and human assessment; they are not claimed to pass merely because the plugin validates.

## Source layout

```text
.claude-plugin/plugin.json          Claude Code plugin manifest
skills/review-paper/SKILL.md        Shared workflow
skills/review-paper/references/     Rating rubric and report format
scripts/package.py                 Build both distribution archives
evals/behavioral-cases.md           Behavioral evaluation cases
dist/review-paper.zip               Uploadable standalone Claude skill
dist/research-eval-plugin.zip       Extractable Claude Code plugin
```
