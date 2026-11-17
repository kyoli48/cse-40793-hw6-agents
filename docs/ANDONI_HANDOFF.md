# Running Alphonsus's style agent

This repository contains Alphonsus's style critic, a proposed common Python
testbed, and an unchanged snapshot of your architecture verifier. Part 4 is
deferred. The initial LLM attempts failed during setup; their logs are evidence
of those failures, not completed model evaluations.

## Setup

Local model alternative (no Gemini key needed): install and start Ollama, then
run `ollama pull qwen3:4b`. Add `--provider ollama --model qwen3:4b` to each style
command below. To execute the entire harness using local models:

```sh
python scripts/run_experiments.py --provider ollama --style-model qwen3:4b --partner-model qwen3:4b --log-dir logs/qwen_runs
```

Your architecture agent still requires the Python Ollama SDK installed below.

Clone this repository and enter its root. Use Python 3.10 or newer.
The style agent itself needs no Python dependencies.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r partner_agent/requirements.txt
```

Set GEMINI_API_KEY in your shell using your own key. Do not commit the key.
The agent defaults to gemini-2.5-flash; pass --model if your account needs a
different Gemini model. Your architecture agent also needs Ollama running and
qwen3 downloaded. Its code is preserved in partner_agent/run_agent.py.

## Run Alphonsus's agent individually

Use distinct output names so the original attempt logs remain available.
Exit 1 means findings were reported; exit 2 means an error; exit 3 means
incomplete coverage. The CLI does not apply changes to the target.

Baseline:

```sh
python run_agent.py --target test_repo --log-file logs/andoni_style_baseline.jsonl --html logs/andoni_style_baseline.html
```

Immediate repeat, without changing any files:

```sh
python run_agent.py --target test_repo --log-file logs/andoni_style_iterative.jsonl --html logs/andoni_style_iterative.html
```

Stress with a one-file review budget (the baseline has three Python files):

```sh
python run_agent.py --target test_repo --max-steps 1 --log-file logs/andoni_style_stress.jsonl --html logs/andoni_style_stress.html
```

Expected baseline findings are S003 and S004 in domain/pricing.py, plus S005
in domain/discounts.py if the model detects the missing currency units.
ui/display.py should pass. The immediate repeat should report the same issues.
The stress run should report INCOMPLETE, regardless of findings in the first
file. Record actual findings, misses, false positives, duration and token usage.

To check just the free deterministic stage, add --mode deterministic. That
mode checks S001–S004 only and cannot evaluate S005.

## Run both agents on the identical three scenarios

```sh
python scripts/run_experiments.py
```

The harness creates a disposable Git repository, uses identical snapshots for
both tools, runs baseline and immediate repeat, then adds a large decoy with
an instruction injection for the stress run. It also restricts the style
agent's file budget during stress. It records output, errors, exit codes,
duration and before/after input hashes under logs/. It does not reset this
checkout. The harness overwrites experiments.json and text captures and appends
JSONL; preserve existing logs before rerunning if needed.

This common testbed has not yet been jointly approved. Inspect RULES.md,
ARCHITECTURE.md and the expected outcomes together before using the results in
your individual reflections. Agree on the same committed testbed revision.

Share the resulting logs and observations with Alphonsus. Do not treat an
import error or missing key as an agent's substantive review verdict.
