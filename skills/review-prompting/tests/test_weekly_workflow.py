"""Controlled weekly lifecycle tests; desktop failure is simulated, not a live scheduled run."""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0, str(SCRIPTS))
import practice_store as store

NOW = '2026-10-28T09:00:00+00:00'
MONDAY = datetime.fromisoformat('2026-11-02T09:00:00+00:00')
HABITS = [
    {'id':'give-direction', 'title':'Give direction', 'action':'Explain the mismatch and give a positive example.'},
    {'id':'replace-constraint', 'title':'Replace the whole constraint', 'action':'State the full replacement and what to recalculate.'},
    {'id':'verify-first', 'title':'Verify before correcting', 'action':'Ask for the evidence or calculation first.'},
]
REPORT = '''# Weekly prompting review: 26 October to 1 November 2026

## What you achieved

- Produced a revised service configuration with a recorded passing test run. Deployment is not established. [config-chat, event 3]
- Reached a focused naming shortlist. No final selection is recorded. [naming-chat, events 1-2]
- A separate deployment was described as complete by the assistant, with no supporting tool result. Treat it as claimed completion. [deployment-chat, event 1]

## How you applied the three habits

- Give direction — Applied: explained that names were too whimsical and supplied Apollo as a reference. [naming-chat, event 1]
- Replace the whole constraint — Applied: supplied the complete new request-rate limit and requested recalculation. [config-chat, event 1]
- Verify before correcting — Applied: requested a calculation without asserting an error. [conversion-chat, event 1]

These observations follow the lessons introduced on 28 October. The 27 October exchange cannot establish application of a lesson introduced later.

## Your next three habits

Retain all three. Reword the first for clarity, preserving its identity. Practise one diagnostic follow-up in a real task and retain its source reference.

## Coverage and limits

Synthetic pilot only. Reviewed four independent conversations inside the target week. Excluded an earlier event, a subagent record and duplicated fork ancestry. No claim of mastery or causal improvement.
'''


class HabitIdentityTests(unittest.TestCase):
    def test_rewording_with_same_id_preserves_introduction_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = store.update_current(tmp, HABITS, NOW)
            changed = deepcopy(HABITS)
            changed[0]['title'] = 'Make feedback diagnostic'
            changed[0]['action'] = 'Explain why it misses and provide a positive reference.'
            result = store.update_current(tmp, changed, '2026-11-02T09:00:00+00:00')
            self.assertEqual(result[0]['id'], original[0]['id'])
            self.assertEqual(result[0]['introduced_at_utc'], NOW)
            self.assertNotEqual(result[0]['title'], original[0]['title'])

    def test_new_identity_gets_new_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            store.update_current(tmp, HABITS, NOW)
            changed = deepcopy(HABITS)
            changed[0] = {'id':'define-success', 'title':'Define success', 'action':'State how completion can be checked.'}
            result = store.update_current(tmp, changed, '2026-11-02T09:00:00+00:00')
            self.assertEqual(result[0]['introduced_at_utc'], '2026-11-02T09:00:00+00:00')
            self.assertEqual(result[1]['introduced_at_utc'], NOW)

    def test_legacy_migration_preserves_dates_and_reuses_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = [dict(title=h['title'], action=h['action'], introduced_at_utc=NOW) for h in HABITS]
            (Path(tmp)/'sticky-state.json').write_text(json.dumps({'habits':old}))
            first = store.update_current(tmp, old)
            second = store.update_current(tmp, old)
            self.assertEqual(first, second)
            self.assertTrue(all(h['introduced_at_utc']==NOW for h in first))
            self.assertEqual(len({h['id'] for h in first}), 3)

    def test_duplicate_ids_are_rejected_without_advancing_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            store.update_current(tmp, HABITS, NOW)
            path = Path(tmp)/'practice-state.json'
            previous = path.read_bytes()
            bad = deepcopy(HABITS)
            bad[1]['id'] = bad[0]['id']
            with self.assertRaises(ValueError):
                store.update_current(tmp, bad)
            self.assertEqual(path.read_bytes(), previous)


class WeeklyLifecycleTests(unittest.TestCase):
    def test_same_week_rerun_keeps_baseline_and_reuses_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = store.update_current(tmp, HABITS, NOW)
            initial = store.begin_review(tmp, 'Europe/London', MONDAY)
            changed = deepcopy(original)
            changed[0]['title'] = 'Make feedback diagnostic'
            first = store.publish_review(tmp, '2026-10-26', REPORT, changed, 'https://example.org/private/pilot', '2026-11-02T09:00:00+00:00')
            rerun = store.begin_review(tmp, 'Europe/London', MONDAY)
            self.assertEqual(initial['baseline_habits'], rerun['baseline_habits'])
            self.assertEqual(rerun['baseline_habits'], original)
            self.assertNotEqual(rerun['baseline_habits'], rerun['next_habits'])
            second = store.publish_review(tmp, '2026-10-26', REPORT, changed)
            self.assertEqual(first['report']['path'], second['report']['path'])
            self.assertEqual(first['report']['url'], second['report']['url'])
            self.assertEqual(len(list((Path(tmp)/'reports').glob('*.md'))), 1)
            self.assertEqual(store.load_state(Path(tmp))['weeks']['2026-10-26']['revisions'], [])

    def test_report_survives_unavailable_desktop_and_next_week_has_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            store.update_current(tmp, HABITS, NOW)
            store.begin_review(tmp, 'Europe/London', MONDAY)
            changed = deepcopy(HABITS)
            changed[0]['title'] = 'Make feedback diagnostic'
            published = store.publish_review(tmp, '2026-10-26', REPORT, changed)
            store.record_desktop(tmp, '2026-10-26', 'blocked', 'Simulated unavailable GUI session')
            state = store.load_state(Path(tmp))
            self.assertEqual(Path(published['report']['path']).read_text(), REPORT)
            self.assertEqual(state['weeks']['2026-10-26']['desktop']['status'], 'blocked')
            next_week = store.begin_review(tmp, 'Europe/London', datetime.fromisoformat('2026-11-09T09:00:00+00:00'))
            self.assertEqual(next_week['baseline_habits'], state['weeks']['2026-10-26']['next_habits'])
            self.assertEqual(next_week['baseline_habits'][0]['introduced_at_utc'], NOW)

    def test_changed_report_preserves_exact_superseded_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            store.update_current(tmp, HABITS, NOW)
            store.begin_review(tmp, 'Europe/London', MONDAY)
            store.publish_review(tmp, '2026-10-26', REPORT, HABITS)
            revised = REPORT+'\nRevision: a later source verified the deployment.\n'
            result = store.publish_review(tmp, '2026-10-26', revised, HABITS)
            self.assertEqual(Path(result['report']['path']).read_text(), revised)
            self.assertEqual((Path(tmp)/'reports/2026-10-26-revision-1.md').read_text(), REPORT)
            self.assertEqual(store.begin_review(tmp, 'Europe/London', MONDAY)['baseline_habits'][0]['introduced_at_utc'], NOW)

    def test_historical_rerun_does_not_replace_current_habits(self):
        with tempfile.TemporaryDirectory() as tmp:
            store.update_current(tmp, HABITS, NOW)
            store.begin_review(tmp, 'Europe/London', MONDAY)
            store.publish_review(tmp, '2026-10-26', REPORT, HABITS)
            store.begin_review(tmp, 'Europe/London', datetime.fromisoformat('2026-11-09T09:00:00+00:00'))
            current = deepcopy(HABITS)
            current[0] = {'id':'define-success', 'title':'Define success', 'action':'State how completion can be checked.'}
            store.publish_review(tmp, '2026-11-02', 'New weekly report', current)
            before = store.load_state(Path(tmp))['current_habits']
            result = store.publish_review(tmp, '2026-10-26', REPORT, HABITS)
            self.assertTrue(result['historical'])
            self.assertEqual(store.load_state(Path(tmp))['current_habits'], before)

    def test_publish_requires_captured_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'Begin'):
                store.publish_review(tmp, '2026-10-26', REPORT, HABITS)
            self.assertFalse((Path(tmp)/'reports').exists())


if __name__ == '__main__':
    unittest.main()
