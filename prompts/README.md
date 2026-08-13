# Iterating on the brief

The brief's quality lives almost entirely in `system.md`. Everything else in this repo is
plumbing that either works or doesn't. This is the part worth returning to.

## The loop

```bash
python -m src.capture          # snapshot today's real data (once, or when you want fresh input)
$EDITOR prompts/system.md      # change the prose
python -m src.tune             # replay the same snapshot through the new prompt
```

Capture freezes the input. That matters more than it sounds: if you iterate against live
Graph calls, the inbox shifts under you and you cannot tell whether the output changed
because of your edit or because new mail arrived. With a fixture, your edit is the only
variable.

Nothing in this loop sends email.

## Trying an alternative without losing the current one

Copy `system.md` to a new name, edit it, and compare on identical input:

```bash
cp prompts/system.md prompts/tighter.md
$EDITOR prompts/tighter.md
python -m src.tune --compare system,tighter
```

Both run against the same fixture, so the difference you see is the prompt. When a variant
wins, move it over `system.md` and log why in `CHANGELOG.md`.

```bash
python -m src.tune --list      # what variants exist
python -m src.tune --save      # keep the output in runs/ to diff later
```

## Frontmatter

```yaml
---
version: 2
model: claude-sonnet-5
max_tokens: 2000
temperature: 1.0
status: live
notes: What changed and why
---
```

`model` is per-prompt, so you can A/B a cheaper or stronger model against the same prose:
copy the file, change one line, `--compare`. Sonnet is the default and the right tier for
daily triage. If you find yourself reaching for Opus, first check whether the prompt is
underspecified - vague instructions are usually the problem, not model capability.

## Placeholders

`{{tz_label}}` is substituted at runtime. Double braces so literal single braces in prose
are never mangled. `tune` warns about unrecognized placeholders before spending tokens, so
a typo surfaces immediately instead of silently producing a prompt with `{{tz_labl}}` in it.

## What to actually tune, in rough priority order

1. **The ACTION REQUIRED / NEEDS A REPLY / FYI split.** This is the whole value of the
   brief. If the wrong things land in ACTION REQUIRED, the brief is noise.
2. **Demotion rules.** Vendor outreach and automated digests should compress to one line.
   If they are taking individual entries, tighten the rule.
3. **The "say what they need" instruction.** The difference between "Abbe replied about
   Summits" and "Abbe needs attendee contacts before she can schedule" is the difference
   between a list and a brief.
4. **Length.** 400 words is a guess. Adjust once you know whether you read the whole thing.

Do not tune against a single day. One quiet inbox tells you nothing. Capture a few fixtures
across different days - label them, `python -m src.capture --label busy-monday` - and check
a prompt change against several before adopting it.

## Deliberately no automated eval

There is no scoring harness or LLM judge here. What makes a good brief for you is not a
metric anyone can specify in advance, and a judge would optimize toward its own idea of
"executive summary." Read the output. You are the evaluator.
