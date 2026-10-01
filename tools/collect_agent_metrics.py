#!/usr/bin/env python3
"""Extract per-turn time and provider token counters for a specified parent only.

No messages, prompts, environment contents or credentials are exported.
"""
import argparse
import json
from pathlib import Path


def collect(path, parent_thread, prefix):
    with path.open() as stream:
        first = json.loads(stream.readline())
        meta = first.get("payload", {})
        source = meta.get("source", {})
        spawn = source.get("subagent", {}) if isinstance(source, dict) else {}
        spawn = spawn.get("thread_spawn", {}) if isinstance(spawn, dict) else {}
        parent = meta.get("parent_thread_id") or spawn.get("parent_thread_id")
        agent = meta.get("agent_path") or spawn.get("agent_path", "")
        if parent != parent_thread or not agent.startswith(prefix):
            return []
        rows, totals, prior, active = [], {}, {}, None
        model, effort = None, None
        tool_calls, model_calls, exit_statuses = 0, 0, []
        for line in stream:
            event = json.loads(line)
            value = event.get("payload", {})
            if event.get("type") == "turn_context":
                model, effort = value.get("model"), value.get("effort")
            if event.get("type") == "token_usage_record":
                model_calls += 1
            if event.get("type") == "response_item" and value.get("type") in {"custom_tool_call", "function_call"}:
                tool_calls += 1
            if event.get("type") == "response_item" and value.get("type") == "custom_tool_call_output":
                for item in value.get("output", []):
                    if not isinstance(item, dict):
                        continue
                    try:
                        tool_result = json.loads(item.get("text", ""))
                    except (ValueError, TypeError):
                        continue
                    if isinstance(tool_result, dict) and "exit_code" in tool_result:
                        exit_statuses.append(tool_result["exit_code"])
            if event.get("type") != "event_msg":
                continue
            kind = value.get("type")
            if kind == "task_started":
                active = value.get("turn_id")
                prior = totals.copy()
                tool_calls, model_calls, exit_statuses = 0, 0, []
            elif kind == "token_count":
                info = value.get("info") or {}
                totals = info.get("total_token_usage", totals)
            elif kind == "task_complete":
                usage = {key: number - prior.get(key, 0) for key, number in totals.items()}
                if any(x < 0 for x in usage.values()):
                    raise ValueError("token counters decreased; cannot infer per-turn usage")
                rows.append(dict(agent=agent, turn_id=active, model=model, effort=effort,
                                 duration_ms=value.get("duration_ms"), started_at=value.get("started_at"),
                                 completed_at=value.get("completed_at"), usage=usage or None,
                                 tool_calls=tool_calls, model_calls=model_calls, command_exit_statuses=exit_statuses))
        return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions", type=Path, required=True)
    parser.add_argument("--parent-thread", required=True)
    parser.add_argument("--agent-prefix", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for path in sorted(args.sessions.rglob("*.jsonl")):
        rows.extend(collect(path, args.parent_thread, args.agent_prefix))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    print(f"Collected {len(rows)} completed turns; no prompt or message text exported")


if __name__ == "__main__":
    main()
