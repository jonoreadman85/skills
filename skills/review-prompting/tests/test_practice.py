import contextlib
from datetime import datetime
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sticky = load('update_sticky')
week = load('week_window')
HABITS = {'habits': [{'title': 'Habit ' + str(i), 'action': 'Try it in a relevant exchange.'} for i in range(3)]}


class WeekWindowTests(unittest.TestCase):
    def test_monday_and_midweek_target_same_complete_week(self):
        monday = week.previous_week(datetime.fromisoformat('2026-11-02T09:00:00+00:00'), 'Europe/London')
        thursday = week.previous_week(datetime.fromisoformat('2026-11-05T09:00:00+00:00'), 'Europe/London')
        self.assertEqual(monday, thursday)
        self.assertEqual(monday['label'], '2026-10-26 to 2026-11-01')

    def test_calendar_week_spans_daylight_saving_change(self):
        result = week.previous_week(datetime.fromisoformat('2026-10-26T09:00:00+00:00'), 'Europe/London')
        self.assertEqual(result['start_inclusive'], '2026-10-19T00:00:00+01:00')
        self.assertEqual(result['end_exclusive'], '2026-10-26T00:00:00+00:00')
        self.assertEqual((datetime.fromisoformat(result['end_exclusive']) - datetime.fromisoformat(result['start_inclusive'])).total_seconds(), 169*3600)

    def test_uses_local_calendar_not_execution_timezone(self):
        result = week.previous_week(datetime.fromisoformat('2026-11-02T00:30:00+00:00'), 'America/Los_Angeles')
        self.assertEqual(result['report_key'], '2026-10-19')

    def test_naive_reference_time_rejected(self):
        with self.assertRaises(ValueError):
            week.previous_week(datetime(2026, 11, 2), 'Europe/London')


class StickyTests(unittest.TestCase):
    def test_input_cannot_inject_extra_lines_or_unsafe_links(self):
        for bad in [dict(HABITS, report_url='javascript:alert(1)'), dict(HABITS, report_url='https:relative'), {'habits': HABITS['habits'][:2]}, {'habits': [{'title': 'a\rb', 'action': 'x'}]*3}]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                sticky.render(bad)

    def run_helper(self, folder, fake, dry=False):
        habits = folder / 'input.json'
        habits.write_text(json.dumps(HABITS))
        state = folder / 'private'
        argv = ['update_sticky', '--habits', str(habits), '--state-dir', str(state)]
        if dry:
            argv.append('--dry-run')
        with patch.object(sys, 'argv', argv), patch.object(sticky.sys, 'platform', 'darwin'), patch.object(sticky.subprocess, 'run', side_effect=fake), contextlib.redirect_stdout(io.StringIO()):
            code = sticky.main()
        return code, state

    def test_dry_run_does_not_touch_desktop_or_write_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            def forbidden(*args, **kwargs):
                self.fail('Dry run attempted desktop automation')
            code, state = self.run_helper(Path(tmp), forbidden, True)
            self.assertEqual(code, 0)
            self.assertFalse(state.exists())

    def test_verified_updates_reuse_existing_state_and_guard_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls = []
            text = sticky.render(HABITS)
            def desktop(command, **kwargs):
                payload = json.loads(command[-1])
                calls.append(payload)
                receipt = {'status': 'found', 'text': text} if payload['checkOnly'] else {'status':'unchanged', 'text':text, 'floating':True}
                return subprocess.CompletedProcess(command, 0, json.dumps(receipt), '')
            introduced_at = None
            for _ in range(2):
                code, state = self.run_helper(Path(tmp), desktop)
                self.assertEqual(code, 0)
                saved = json.loads((state/'sticky-state.json').read_text())
                if introduced_at is None:
                    introduced_at = saved['habits'][0]['introduced_at_utc']
                self.assertEqual(saved['habits'][0]['introduced_at_utc'], introduced_at)
            self.assertEqual(calls[1]['expected'], None)
            self.assertEqual(calls[3]['expected'], text)
            self.assertEqual({p.name for p in state.iterdir()}, {'sticky-state.json', 'practice-state.json'})
            self.assertTrue(json.loads((state/'sticky-state.json').read_text())['setup_complete'])

    def test_new_note_is_sized_and_reverified_before_setup_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            calls = []
            text = sticky.render(HABITS)
            def desktop(command, **kwargs):
                calls.append(command)
                if command[1] == '-':
                    self.assertEqual(command[-1], text)
                    return subprocess.CompletedProcess(command, 0, '', '')
                payload = json.loads(command[-1])
                if payload['checkOnly']:
                    receipt = {'status':'missing'}
                else:
                    receipt = {'status':'created' if len(calls)==2 else 'unchanged', 'text':text, 'floating':True}
                return subprocess.CompletedProcess(command, 0, json.dumps(receipt), '')
            code, state = self.run_helper(Path(tmp), desktop)
            self.assertEqual(code, 0)
            self.assertEqual(len(calls), 4)
            self.assertTrue(json.loads((state/'sticky-state.json').read_text())['setup_complete'])

    def test_concurrent_run_stops_before_desktop_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp)/'private'
            state.mkdir()
            (state/'sticky.lock').write_text('existing run')
            def forbidden(*args, **kwargs):
                self.fail('Locked run attempted desktop automation')
            with self.assertRaisesRegex(RuntimeError, 'Another updater'):
                self.run_helper(Path(tmp), forbidden)
            self.assertEqual((state/'sticky.lock').read_text(), 'existing run')

    def test_permission_failure_does_not_advance_existing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            state = folder/'private'
            state.mkdir()
            original = '{"last_text":"previous note"}'
            (state/'sticky-state.json').write_text(original)
            def denied(command, **kwargs):
                return subprocess.CompletedProcess(command, 1, '', 'Accessibility access denied')
            with self.assertRaisesRegex(RuntimeError, 'Accessibility'):
                self.run_helper(folder, denied)
            self.assertEqual((state/'sticky-state.json').read_text(), original)

    def test_unverified_note_is_not_recorded_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            def desktop(command, **kwargs):
                return subprocess.CompletedProcess(command, 0, json.dumps({'status':'updated','text':'different text','floating':True}), '')
            with self.assertRaisesRegex(RuntimeError, 'not verified'):
                self.run_helper(Path(tmp), desktop)
            self.assertFalse((Path(tmp)/'private'/'sticky-state.json').exists())


if __name__ == '__main__':
    unittest.main()
