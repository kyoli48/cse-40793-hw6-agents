# Homework 6 — implementation and initial experiments

Date: November 16, 2026. Student: Alphonsus, Student 10.
This is an evidence-backed progress report through Part 3, not a finished
submission or a claim that both agents have been evaluated successfully.
Part 4 redesign and retesting are deferred at the student's request.

## Assignment understanding and steps

The supplied DOCX requires an individual reproducible agent CLI (Part 1), a
shared fake codebase for two agents (Part 2), and baseline, iterative and
adversarial executions of each agent with effectiveness commentary (Part 3).
The final individual reflection also asks for use circumstances, cadence,
false positives/negatives, three collaboration diagrams, tradeoffs and Part 4
redesign. That final reflection should be completed after Part 4.

The user's template describes a read-only style critic guided by RULES.md,
with deterministic verification and an LLM judge. The implementation preserves
that architecture, uses Python's AST rather than ESLint for Python code, and
supports JSON plus an HTML inspection artifact. See AGENT_DESIGN.md.

Partner: https://github.com/andonilc7/homework-6-ai-aided-swe
Observed main revision: 8562a6890ef4e4be4ec49f27e8f72b3580b07958.
Read the actual source, not only the README. It collects ARCHITECTURE.md,
Git diffs and optional context, makes one Ollama/qwen3 call, validates the
first-line verdict, and logs duration and model token counts. It refuses
review evidence larger than 12,000 bytes. The local copy is unchanged.
A network clone failed (DNS restriction); source was retrieved via Firecrawl.

## Shared testbed and expected outcomes

The common Python pricing application includes:

| File | Seeded condition | Expected detector |
| --- | --- | --- |
| domain/pricing.py:1 | calculateTotal violates S003; no docstring violates S004 | Style deterministic + LLM |
| domain/pricing.py:2 | print in domain violates A001 | Partner architecture verifier |
| domain/discounts.py:2 | Monetary units absent from docstring, S005 | Style LLM; deterministic deliberately lacks semantic coverage |
| ui/display.py | Printing allowed in UI; documented dollar units | Both should accept |

The testbed contains pure calculations and presentation boundaries without
external application services. The testbed was created locally for both tools; no partner approval
or joint authorship is claimed. RULES.md and ARCHITECTURE.md deliberately cover
different engineering concerns. No agent is expected to fix source automatically.

## Execution protocol

scripts/run_experiments.py creates a disposable Git baseline from test_repo.
Baseline and iterative executions use identical input. This satisfies the
assignment's immediate rerun option without applying fixes. The partner uses
--baseline on both so the repeat is not merely a NO_CHANGES shortcut.
Stress adds domain/decoy.py with 800 padding lines and an instruction to ignore
rules and return PASS. Style also gets --max-steps 1. For the partner the decoy
should push the evidence past 12,000 bytes if dependency startup succeeds.
Each agent sees the same snapshot per scenario. Hashes before and after each
run verify that code was unchanged.

## Observed results

Source of truth: logs/experiments.json, corresponding JSONL files, stdout and
stderr captures. All nine attempted processes left their targets unchanged.

| Tool/mode | Baseline | Immediate repeat | Stress |
| --- | --- | --- | --- |
| Style deterministic | FAIL, S003 + S004, 0.005 s | Same findings, 0.005 s | INCOMPLETE, one decoy file reviewed, 0.006 s |
| Style Gemini | ERROR, missing Gemini key | Same missing-key error | INCOMPLETE before any model call; decoy exceeds byte limit |
| Partner unchanged | Import failure: no ollama SDK | Same import failure | Same import failure, before evidence collection |

Timings above are the agent's internal deterministic timings from this run;
process timings in experiments.json include interpreter startup. These do not
measure LLM latency. Deterministic mode uses zero LLM tokens. No LLM token
consumption or dollar cost was observed for either agent. Installing the partner
dependency was attempted separately; see setup-install.txt for its outcome.

Annotated trace excerpts:

```json
{"rule_id":"S003","line":1,"evidence":"def calculateTotal(price, quantity):","message":"Function name is not snake_case"}
{"rule_id":"S004","line":1,"message":"Public function lacks a docstring"}
```
These expected findings appear in both deterministic baseline and repeat logs.
They support repeatability for these two violations, not semantic completeness.

```text
style_deterministic_adversarial: status=INCOMPLETE
reviewed_files=1, total_files=4
file=domain/decoy.py, error=File exceeds --max-bytes
```
The stress outcome avoids claiming the repository passed after reviewing only
the decoy. Prompt-injection resistance was NOT evaluated because its content
never reached a model.

```text
Set GEMINI_API_KEY or GOOGLE_API_KEY for Gemini review.
ModuleNotFoundError: No module named 'ollama'
```
These are infrastructure failures, not evidence of poor review reasoning.
The partner exit code 1 is a Python import exception, NOT its normal FAIL
verdict. No partner JSONL is written because import fails before main().

## Effectiveness and usefulness so far

Style's deterministic stage correctly detected both seeded mechanically
checkable violations, repeated them consistently, and did not flag the valid
UI file. It missed S005, as expected for this mode: documentation semantics
need the LLM stage. No automatic fixes means there were no source regressions
in these runs. The three unit tests also passed: expected findings, immunity
to function-like text in comments/strings, and rejecting invented rule/evidence.

Partner usefulness cannot yet be assessed from actual model output. Its design
could complement style by detecting forbidden I/O in the domain layer, which
style does not prohibit. Its existing input cap is visible in source, but the
current stress attempt never reached it. No inherited partner log is presented
as a new execution.

Provisional use guidance: style is useful for small Python PRs with explicit
team rules, especially as deterministic pre-commit feedback. Semantic review
should initially run on demand or on PRs with human review. A missing units
statement can be noise when units are specified by a type or external contract;
requiring docstrings for every public helper can also burden legacy code.
Architecture verification suits documented layer boundaries, but stale or
underspecified architecture rules can cause questionable advice. No observed
LLM latency/cost supports recommending continuous LLM execution yet.

## What remains for Part 3

1. Provide Gemini credentials in the local environment and ensure model access.
2. Install the Ollama Python SDK, start Ollama and make qwen3 available.
3. Rerun scripts/run_experiments.py with that Python interpreter.
4. Compare actual model findings with the expected table, inspect repeat
   consistency and stress failure behavior, and update this report with real
   token counts, durations and annotated model trace excerpts.

No Part 4 modifications were made in response to the experiment outcomes.
