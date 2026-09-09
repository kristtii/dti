#!/bin/sh
# PostToolUse hook (Edit|Write): non-blocking reminders after relevant edits.

payload=$(cat)

file_path=$(printf '%s' "$payload" | python3 -c 'import sys, json
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
    sys.exit(0)
print(data.get("tool_input", {}).get("file_path", ""))')

case "$file_path" in
    */blog/models.py)
        echo "Reminder: models.py changed -> run 'python manage.py makemigrations' then 'migrate'." >&2
        ;;
    */static/css/*)
        echo "Reminder: CSS source changed -> run 'python manage.py collectstatic' before deploy." >&2
        ;;
esac

exit 0
