#!/usr/bin/env python3
"""PreToolUse guard for the AI Engineer Wiki.

Enforces the two irreversible hard rules from CLAUDE.md at the tool level, so they
hold regardless of what the model decides:

  1. transcripts/ is immutable source material — block all Edit/Write.
  2. The `## Notes` section of a wiki/ page is user-owned — block any Edit/Write
     that modifies it.

Reads the hook JSON on stdin. Exit 2 = deny (stderr is shown to Claude). Exit 0 =
allow. Any parsing/IO problem fails open (exit 0) rather than blocking legitimate
work.
"""
import json
import os
import sys

NOTES_HEADING = "## Notes"


def deny(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def notes_section(text):
    """Return the text from the first `## Notes` heading to end, or None."""
    idx = text.find(NOTES_HEADING)
    return None if idx == -1 else text[idx:]


def notes_region_touched(current, old_string):
    """True if any occurrence of old_string reaches at/into the Notes region."""
    idx = current.find(NOTES_HEADING)
    if idx == -1 or not old_string:
        return False
    start = 0
    while True:
        pos = current.find(old_string, start)
        if pos == -1:
            return False
        if pos + len(old_string) > idx:
            return True
        start = pos + 1


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if data.get("tool_name") not in ("Edit", "Write"):
        sys.exit(0)

    tool = data["tool_name"]
    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    if not file_path:
        sys.exit(0)

    cwd = data.get("cwd") or os.getcwd()
    project = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR") or cwd)
    abs_fp = file_path if os.path.isabs(file_path) else os.path.normpath(os.path.join(cwd, file_path))

    try:
        rel = os.path.relpath(abs_fp, project).replace(os.sep, "/")
    except ValueError:
        sys.exit(0)

    # 1. transcripts/ is immutable
    if rel == "transcripts" or rel.startswith("transcripts/"):
        deny("Blocked: transcripts/ is immutable source material (CLAUDE.md hard rule — read-only).")

    # 2. wiki/ `## Notes` is user-owned
    if rel.startswith("wiki/"):
        if not os.path.exists(abs_fp):
            sys.exit(0)  # new page — its empty Notes section is fine to create
        try:
            with open(abs_fp, encoding="utf-8") as fh:
                current = fh.read()
        except OSError:
            sys.exit(0)
        if NOTES_HEADING not in current:
            sys.exit(0)
        if tool == "Edit":
            if notes_region_touched(current, tool_input.get("old_string", "")):
                deny("Blocked: this edit modifies the user-owned `## Notes` section (CLAUDE.md hard rule 2).")
        else:  # Write
            if notes_section(current) != notes_section(tool_input.get("content", "")):
                deny("Blocked: this Write changes the user-owned `## Notes` section (CLAUDE.md hard rule 2). Preserve it verbatim.")

    sys.exit(0)


if __name__ == "__main__":
    main()
