import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from collect_agent_metrics import collect


class MetricsTests(unittest.TestCase):
    def test_unrelated_cli_source_string(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "session.jsonl"
            p.write_text(json.dumps(dict(type="session_meta", payload=dict(source="cli"))) + "\n")
            self.assertEqual(collect(p, "parent", "/root/ab_"), [])

    def test_filter_and_turn_deltas(self):
        events = [dict(type="session_meta", payload=dict(parent_thread_id="parent", agent_path="/root/ab_x"))]
        for turn, tokens in [("one", 100), ("two", 170)]:
            events.extend([
                dict(type="event_msg", payload=dict(type="task_started", turn_id=turn)),
                dict(type="turn_context", payload=dict(model="test-model", effort="medium")),
                dict(type="event_msg", payload=dict(type="token_count", info=dict(total_token_usage=dict(input_tokens=tokens, cached_input_tokens=20, output_tokens=10)))),
                dict(type="event_msg", payload=dict(type="task_complete", duration_ms=1234)),
            ])
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "session.jsonl"
            p.write_text("\n".join(json.dumps(x) for x in events))
            self.assertEqual(collect(p, "another-parent", "/root/ab_"), [])
            rows = collect(p, "parent", "/root/ab_")
            self.assertEqual([r["usage"]["input_tokens"] for r in rows], [100, 70])
            self.assertEqual(rows[1]["usage"]["output_tokens"], 0)
            self.assertEqual(rows[0]["duration_ms"], 1234)
            self.assertNotIn("messages", rows[0])


if __name__ == "__main__":
    unittest.main()
