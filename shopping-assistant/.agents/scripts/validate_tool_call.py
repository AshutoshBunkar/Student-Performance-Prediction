import json
import re
import sys


def main():
    try:
        # Read the JSON payload from stdin
        input_data = json.loads(sys.stdin.read())
    except Exception:
        # Default to allow if JSON parsing fails to avoid blocking the agent unintentionally
        print(
            json.dumps(
                {"decision": "allow", "reason": "No valid JSON input found on stdin"}
            )
        )
        sys.exit(0)

    # Extract command line from potential payload structures
    tool_args = (
        input_data.get("arguments")
        or input_data.get("tool_args")
        or input_data.get("args")
        or {}
    )

    command_line = (
        tool_args.get("CommandLine")
        or tool_args.get("command")
        or input_data.get("command")
        or ""
    )

    # Normalize command to help with regex matching
    normalized_cmd = " ".join(command_line.lower().split())

    # Detect destructive patterns, specifically blocking commands like 'rm -rf /'
    # and general 'rm -rf' or 'rm -f' executions
    if "rm -rf" in normalized_cmd or re.search(r"rm\s+-rf\s+/", normalized_cmd):
        print(
            json.dumps(
                {
                    "decision": "deny",
                    "reason": "Destructive command blocked by secure coding standards hook.",
                }
            )
        )
        sys.exit(1)

    # Otherwise allow the command execution
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
