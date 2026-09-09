#!/bin/sh
# PreToolUse hook (Edit|Write): hard-block edits to .env and db files.
# Reads tool call JSON on stdin, emits a deny decision when the target is protected.

payload=$(cat)

file_path=$(printf '%s' "$payload" | python3 -c 'import sys, json
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    sys.exit(0)
print(data.get("tool_input", {}).get("file_path", ""))')

deny() {
    reason="$1"
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$reason"
    exit 0
}

case "$file_path" in
    *.env|*/.env)
        deny "STRICT USE: never edit .env directly. Instruct the user to edit .env themselves."
        ;;
    *.sqlite3|*db.sqlite3)
        deny "STRICT USE: never modify db files directly. Use Django migrations instead."
        ;;
esac

exit 0
