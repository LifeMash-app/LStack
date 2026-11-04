import hashlib
import json
import os
from pathlib import Path
import re
import sys


COMMAND = re.compile(
    r"(?:poteto\s*(?:mode|모드)|포테토\s*모드|\$pstack:poteto-mode)"
    r"\s+(on|off|status|켜줘|꺼줘|상태)[.!]?",
    re.IGNORECASE,
)
ACTIONS = {"on": "on", "켜줘": "on", "off": "off", "꺼줘": "off", "status": "status", "상태": "status"}


def emit(event_name, context, status=None):
    output = {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}
    if status:
        output["systemMessage"] = status
    print(json.dumps(output, ensure_ascii=False))


def handle(event):
    event_name = event.get("hook_event_name")
    if event_name not in ("SessionStart", "UserPromptSubmit"):
        return
    prompt = event.get("prompt", "")
    if not isinstance(prompt, str):
        return
    lines = prompt.strip().splitlines()
    match = COMMAND.fullmatch(lines[0].strip()) if lines and event_name == "UserPromptSubmit" else None
    action = ACTIONS[match.group(1).lower()] if match else None
    session_id = event.get("session_id")
    data_dir = os.environ.get("PLUGIN_DATA")
    if not isinstance(session_id, str) or not session_id.strip() or not data_dir:
        if action:
            emit(event_name, "LStack session persistence is unavailable. Do not claim the mode is saved; use current-turn-only behavior.", "Poteto 모드 상태를 저장할 수 없습니다.")
        return
    key = hashlib.sha256(session_id.encode()).hexdigest()
    marker = Path(data_dir) / "poteto-mode" / f"{key}.enabled"
    try:
        if event_name == "SessionStart" and event.get("source") in ("clear", "fork"):
            marker.unlink(missing_ok=True)
        if action == "on":
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.touch(mode=0o600)
        elif action == "off":
            marker.unlink(missing_ok=True)
        enabled = marker.is_file()
    except OSError:
        emit(event_name, "LStack could not access its session state. Do not claim persistence; use current-turn-only behavior.", "Poteto 모드 상태를 확인하거나 저장하지 못했습니다.")
        return
    restoring = event_name == "SessionStart" and event.get("source") in ("resume", "compact", "clear", "fork")
    if not enabled and action is None and not restoring:
        return
    if enabled:
        skill = Path(__file__).resolve().parent.parent / "skills" / "poteto-mode" / "SKILL.md"
        context = f"LStack Poteto Mode is ON for this conversation. Follow {skill} for this request. Reuse it if already loaded; read it again after compaction. This does not change permissions or model settings."
    else:
        context = "LStack Poteto Mode is OFF for this conversation. Do not continue persistent Poteto routing. Explicit skill invocations still apply to their request."
    if action and not any(line.strip() for line in lines[1:]):
        context += " This is only a mode-control request; acknowledge the state without starting a work playbook."
    status = f"Poteto 모드 {'켜짐' if enabled else '꺼짐'}" if action else None
    emit(event_name, context, status)


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError):
        return
    if isinstance(event, dict):
        handle(event)


if __name__ == "__main__":
    main()
