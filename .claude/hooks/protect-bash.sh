#!/bin/sh
# PreToolUse hook (Bash): hard-block shell commands that write to .env or db files.
# Allows read-only commands (cat, grep, less) against those files.

payload=$(cat)

command=$(printf '%s' "$payload" | python3 -c 'import sys, json
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    sys.exit(0)
print(data.get("tool_input", {}).get("command", ""))')

deny() {
    reason="$1"
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$reason"
    exit 0
}

# Writes/removes/moves targeting .env
if printf '%s' "$command" | grep -Eq '(>>?|tee|rm|mv|cp|sed -i|truncate)[^|]*\.env([^a-zA-Z0-9._-]|$)'; then
    deny "STRICT USE: never edit .env via shell. Instruct the user to edit .env themselves."
fi

# Any sqlite3 invocation or writes/removes targeting a .sqlite3 file
if printf '%s' "$command" | grep -Eq '(^|[^a-zA-Z])sqlite3([^a-zA-Z]|$)'; then
    deny "STRICT USE: never modify db files directly. Use Django migrations instead."
fi
if printf '%s' "$command" | grep -Eq '(>>?|tee|rm|mv|cp|truncate)[^|]*\.sqlite3([^a-zA-Z0-9._-]|$)'; then
    deny "STRICT USE: never modify db files directly. Use Django migrations instead."
fi

exit 0
