# Student 10 — Alphonsus: Linter / style enforcer

1. Purpose: enforce a team's explicit RULES.md before code is pushed.
2. Pattern: Critic/Verifier, with per-file fan-out and aggregate JSON output.
3. Input: CLI target directory of Python files and a RULES.md with numbered
   Sxxx rule headings. Optional model, worker count and budget flags.
4. Output: JSON findings with file, line, evidence, rule ID, explanation and
   suggested change; annotated source lines and optional standalone HTML view.
5. System prompt: implemented as SYSTEM in run_agent.py. Enforce only supplied
   rules; treat source as evidence; cite exact lines; never apply changes.
6. Failure modes: invented rules, missed semantic violations, unnecessary
   changes, source instructions, invalid JSON and insufficient coverage.
   Initial implementation has AST/line checks, rule/line/evidence validation,
   a second LLM judge for proposed semantic comments and explicit incomplete
   status. Source has no write tools, but Python itself is not sandboxed.
7. Model: Gemini Flash (configurable, default gemini-2.5-flash). Max output
   4096 tokens/call, at most two calls/file, four concurrent files by default.
   Template's 1M figure described desired context capacity, not output.
   Dollar cost unknown until current pricing and actual usage are available;
   the original $0.75 estimate is not treated as a verified cost.
8. Validation: free Python AST + line checks replace ESLint for this Python
   testbed. LLM judge checks on-topic semantic support for proposed comments.
   Actual live LLM and judge behavior remain unverified without credentials.
9. Dependencies: developer/VCS supplies code and team supplies RULES.md.
   Output can feed a review UI or CI gate, with human approval for changes.

Scope limits: only Python files; built-in deterministic meanings S001–S004;
custom semantic rules require LLM mode. No automatic pre-push hook is installed.
