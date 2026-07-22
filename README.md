# Code Review Agent

An AI-powered code review agent built with the Gemini API. Instead of reviewing
a diff in isolation, the agent can request additional files from the codebase
when it needs more context, investigating before it judges, similar to how a
human reviewer would.

## How it works

The agent runs in a loop: it's given a code diff and access to two tools
(`list_files` and `read_file`). If it needs to see another file to judge the
change correctly, it requests one; otherwise, it produces its review. It
includes self-correction (recovering from incorrect file-path guesses) and
avoids re-reading files it's already seen.

## Setup

```bash
pip install -U google-genai
export GEMINI_API_KEY="your-key-here"
python3 agent.py
```

## Example

Given a diff that calls an undefined function, the agent requests the file
where it's defined, reads it, and catches a bug that wouldn't be visible from
the diff alone (e.g., a bounds-checking function missing its upper limit).
