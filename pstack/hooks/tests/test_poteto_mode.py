import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PotetoModeTest(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="lstack-mode-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.data = self.root / "data"
        self.env = {**os.environ, "PLUGIN_ROOT": str(ROOT), "PLUGIN_DATA": str(self.data)}

    def hook(self, prompt="", session="chat-a", event="UserPromptSubmit", source=None, env=None):
        payload = {"hook_event_name": event, "session_id": session, "prompt": prompt}
        if source:
            payload["source"] = source
        manifest = json.loads((ROOT / "hooks/hooks.json").read_text())
        command = manifest["hooks"][event][0]["hooks"][0]["command"]
        result = subprocess.run(command, shell=True, input=json.dumps(payload), text=True, capture_output=True, env=env or self.env, check=True)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout) if result.stdout else None

    def context(self, result):
        return result["hookSpecificOutput"]["additionalContext"]

    def test_new_conversation_is_off_and_does_not_create_state(self):
        self.assertIsNone(self.hook("관련 코드를 조사해줘"))
        self.assertFalse(self.data.exists())

    def test_enable_persists_for_followup_without_repeating_the_command(self):
        self.assertIn("켜짐", self.hook("poteto 모드 켜줘")["systemMessage"])
        result = self.hook("이제 구현해줘")
        self.assertIn("is ON", self.context(result))
        self.assertIn(str(ROOT / "skills/poteto-mode/SKILL.md"), self.context(result))
        self.assertNotIn("systemMessage", result)
        self.assertNotIn("mode-control request", self.context(result))

    def test_off_stops_followup_routing(self):
        self.hook("poteto mode on")
        self.assertIn("is OFF", self.context(self.hook("poteto 모드 꺼줘")))
        self.assertIsNone(self.hook("다음 작업을 해줘"))

    def test_sessions_are_independent(self):
        self.hook("포테토 모드 켜줘", session="chat-a")
        self.assertIsNone(self.hook("구현해줘", session="chat-b"))
        self.hook("poteto mode on", session="chat-b")
        self.hook("poteto mode off", session="chat-a")
        self.assertIn("is ON", self.context(self.hook("구현해줘", session="chat-b")))

    def test_resume_and_compaction_restore_the_same_conversation(self):
        self.hook("poteto mode on")
        for source in ("resume", "compact"):
            with self.subTest(source=source):
                result = self.hook(event="SessionStart", source=source)
                self.assertEqual(result["hookSpecificOutput"]["hookEventName"], "SessionStart")
                self.assertIn("is ON", self.context(result))

    def test_new_fork_is_off_and_parent_stays_on(self):
        self.hook("poteto mode on", session="parent")
        self.assertIn("is OFF", self.context(self.hook(session="child", event="SessionStart", source="fork")))
        self.assertIsNone(self.hook("작업해줘", session="child"))
        self.assertIn("is ON", self.context(self.hook("작업해줘", session="parent")))

    def test_clear_resets_the_conversation(self):
        self.hook("poteto mode on")
        self.assertIn("is OFF", self.context(self.hook(event="SessionStart", source="clear")))
        self.assertIsNone(self.hook("구현해줘"))

    def test_disabled_resume_and_compaction_override_earlier_mode_context(self):
        self.hook("poteto mode on")
        self.hook("poteto mode off")
        for source in ("resume", "compact"):
            with self.subTest(source=source):
                self.assertIn("is OFF", self.context(self.hook(event="SessionStart", source=source)))

    def test_repeated_on_and_off_are_idempotent(self):
        for _ in range(2):
            self.assertIn("켜짐", self.hook("poteto mode on")["systemMessage"])
        self.assertEqual(len(list(self.data.rglob("*.enabled"))), 1)
        for _ in range(2):
            self.assertIn("꺼짐", self.hook("poteto mode off")["systemMessage"])
        self.assertIsNone(self.hook("작업해줘"))

    def test_status_observes_without_enabling(self):
        self.assertIn("꺼짐", self.hook("poteto 모드 상태")["systemMessage"])
        self.assertFalse(self.data.exists())
        self.hook("poteto mode on")
        self.assertIn("켜짐", self.hook("$pstack:poteto-mode status")["systemMessage"])
        self.assertIn("is ON", self.context(self.hook("작업해줘")))

    def test_command_only_acknowledges_but_command_with_task_runs_the_task(self):
        self.assertIn("mode-control request", self.context(self.hook("poteto mode on")))
        self.assertNotIn("mode-control request", self.context(self.hook("poteto mode on\n\n버그를 수정해줘")))

    def test_mentions_quotes_and_one_shot_invocation_do_not_enable_persistence(self):
        for prompt in ('"poteto mode on"', "```text\npoteto mode on\n```", "poteto 모드 켜줘라는 문구를 설명해줘", "$pstack:poteto-mode 버그를 수정해줘"):
            with self.subTest(prompt=prompt):
                self.assertIsNone(self.hook(prompt))
                self.assertIsNone(self.hook("다음 작업"))

    def test_missing_identity_or_data_reports_current_turn_only(self):
        self.assertIn("current-turn-only", self.context(self.hook("poteto mode on", session=None)))
        env = dict(self.env)
        env.pop("PLUGIN_DATA")
        self.assertIn("current-turn-only", self.context(self.hook("poteto mode on", env=env)))
        self.assertFalse(self.data.exists())

    def test_unwritable_state_does_not_claim_the_mode_was_saved(self):
        self.data.write_text("not a directory")
        result = self.hook("poteto mode on")
        self.assertIn("current-turn-only", self.context(result))
        self.assertNotIn("켜짐", result["systemMessage"])

    def test_hook_command_supports_plugin_paths_with_spaces(self):
        plugin = self.root / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", plugin / "hooks")
        env = {**self.env, "PLUGIN_ROOT": str(plugin)}
        self.assertIn(str(plugin / "skills/poteto-mode/SKILL.md"), self.context(self.hook("poteto mode on", env=env)))

    def test_malformed_input_does_not_mutate_state(self):
        for payload in ("{", "[]", '{"hook_event_name":"SessionStart","session_id":[]}'):
            result = subprocess.run(["python3", str(ROOT / "hooks/poteto_mode.py")], input=payload, text=True, capture_output=True, env=self.env)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
        self.assertFalse(self.data.exists())

    def test_large_prompts_only_receive_a_short_skill_reference(self):
        self.hook("poteto mode on")
        self.assertLess(len(self.context(self.hook("작업 " * 10000))), 1000)


if __name__ == "__main__":
    unittest.main()
