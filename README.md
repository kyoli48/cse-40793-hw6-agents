# Homework 6 — Alphonsus (Student 10)

Andoni: start with [the partner handoff guide](docs/ANDONI_HANDOFF.md) for setup
and baseline, repeat, and stress commands for Alphonsus's agent.

Scope: Parts 1–3. Part 4 is intentionally deferred. Part 1 implementation and
Part 2 shared testbed are ready; Part 3 deterministic runs are complete, but
both agents' actual LLM reviews remain blocked by model/dependency access.
See docs/PARTS_1_TO_3.md for the evidence and exact limitations.

## Style CLI

Python 3.10+, no Python packages required for this agent.

```sh
python3 run_agent.py --target ./test_repo --mode deterministic --log-file logs/manual.jsonl --html logs/manual.html
export GEMINI_API_KEY='your-key-set-locally'
python3 run_agent.py --target ./test_repo --model gemini-2.5-flash --log-file logs/gemini.jsonl --html logs/gemini.html
```

Default mode is `llm`: deterministic checks plus Gemini review per file, with a
second Gemini judge call when semantic findings are proposed. Four worker
threads by default. `--max-steps` bounds files, `--max-bytes` bounds each file,
`--max-tokens` bounds output per call. These are practical implementation
budgets; the template's million-token figure is not an output budget.
Gemini receives source code and RULES.md; use a testbed or code you may send.
Set `--model` to a Gemini model available to your account. No live Gemini call
has been verified in this environment.

Exit codes: 0 PASS, 1 violations, 2 error, 3 incomplete coverage. Deterministic
PASS covers only S001–S004, not semantic rule S005. JSON includes findings,
source evidence, suggestions, origin, annotated source, hashes, duration and
usage metadata if returned by Gemini. HTML is a standalone escaped JSON viewer.
The agent never applies fixes. Its file reads are not an OS-level sandbox.
Supported code language: Python; ESLint is inappropriate for this Python shared
testbed, so AST/line checks implement the free verification stage instead.

## Partner CLI

Unmodified source and provenance: partner_agent/SOURCE.md.
Uses Git plus the Python Ollama SDK and an Ollama service with qwen3 installed.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r partner_agent/requirements.txt
ollama serve
# In another terminal, if not installed:
ollama pull qwen3
```

## Reproduce scenarios

Run with a Python interpreter containing the Ollama SDK. Set the Gemini key
first and start Ollama to obtain meaningful LLM reviews.

```sh
.venv/bin/python scripts/run_experiments.py
python3 -m unittest discover -s tests -v
```

The harness copies test_repo into a temporary directory, initializes and
commits it in Git, then performs baseline, immediate repeat, and adversarial
runs for deterministic style, Gemini style, and the partner agent. Logs stay
outside the target. It preserves stdout, stderr, exit codes, elapsed time,
input hashes, and checks that each agent left source files unchanged.
The partner's repeat uses `--baseline` again so it receives identical evidence
rather than skipping the review with NO_CHANGES. The stress scenario adds an
oversized decoy containing an instruction injection; style also has a one-file
budget. Logs append JSONL on reruns; experiments.json and stdout/stderr/HTML
represent the latest harness execution. Copy logs before rerunning if you want
to preserve this initial attempt.

The included test_repo is the common proving ground for both agents, extending
the partner's pricing-domain concept. It was created locally; partner review
and acceptance of this shared testbed have not been recorded.
