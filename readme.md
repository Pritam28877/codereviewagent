# Code Review Agent

An AI-powered code review agent that automatically analyzes pull requests and code diffs, surfaces bugs, security issues, and quality problems, and posts actionable, inline feedback — like a senior engineer reviewing every change.

## Why

Manual code review is slow, inconsistent, and easy to skip under deadline pressure. This agent provides a fast, tireless first pass that catches the obvious problems (and many subtle ones) so human reviewers can focus on architecture and intent rather than nitpicks.

## What It Does

- **Diff-aware review** — reviews only what changed, with surrounding context, instead of dumping the whole file.
- **Bug detection** — flags logic errors, off-by-one mistakes, null/undefined handling, race conditions, and unhandled edge cases.
- **Security scanning** — looks for injection risks, hardcoded secrets, missing authz checks (IDOR), unsafe deserialization, and weak input validation.
- **Quality & style** — highlights dead code, overly complex functions, poor naming, and missed reuse/simplification opportunities.
- **Actionable comments** — every finding includes the file, line, severity, the *why*, and a suggested fix.
- **Configurable strictness** — tune review depth from "high-confidence only" to "broad, exhaustive coverage."

## How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  PR / Diff   │ ──▶ │   Context    │ ──▶ │  LLM Review  │ ──▶ │   Findings   │
│   Source     │     │  Gathering   │     │   Engine     │     │  + Comments  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Ingest** the diff (from a Git provider webhook, CLI, or local working tree).
2. **Gather context** — pull related files, symbols, and project conventions.
3. **Review** — the LLM analyzes each hunk against correctness, security, and quality dimensions.
4. **Report** — findings are deduplicated, ranked by severity, and posted as inline comments or written to a report.

## Tech Stack

> _To be finalized as the project develops._

- **Language:** TBD
- **LLM:** Claude (Anthropic API)
- **Git integration:** GitHub / GitLab APIs
- **Interface:** CLI + optional webhook server

## Getting Started

> _Setup instructions will be added once the initial implementation lands._

```bash
# Clone
git clone <repo-url>
cd codereaviewagent

# Install (placeholder)
# ...

# Run a review on a local diff (placeholder)
# ...
```

## Configuration

The agent reads its configuration from environment variables / a config file:

| Setting             | Description                                  |
| ------------------- | -------------------------------------------- |
| `ANTHROPIC_API_KEY` | API key for the Claude model.                |
| `REVIEW_EFFORT`     | Review depth: `low` \| `medium` \| `high`.   |
| `GIT_PROVIDER`      | `github` \| `gitlab` \| `local`.             |
| `GIT_TOKEN`         | Access token for posting review comments.    |

> Secrets are loaded from the environment only — never commit keys.

## Roadmap

- [ ] Core diff parsing and context gathering
- [ ] LLM review engine with configurable dimensions
- [ ] GitHub PR integration (inline comments)
- [ ] GitLab MR integration
- [ ] CLI for local pre-commit review
- [ ] Webhook server for automated CI review
- [ ] Per-repo convention learning

## License

TBD
