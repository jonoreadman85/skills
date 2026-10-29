#!/usr/bin/env python3
"""Persist habit identity and immutable weekly baselines independently of Stickies."""
import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

from week_window import previous_week


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def private_dir(directory):
    directory = Path(directory).expanduser().resolve()
    package = Path(__file__).resolve().parents[1]
    if directory == package or package in directory.parents:
        raise ValueError('Practice state must be outside the skill package.')
    return directory


@contextmanager
def state_lock(directory, name='practice.lock'):
    directory = private_dir(directory)
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = directory/name
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise RuntimeError('Another updater is running or left a lock; inspect it before retrying.')
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def atomic_json(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2)+'\n')
    temp.replace(path)


def validate_habits(habits):
    if not isinstance(habits, list) or len(habits) != 3:
        raise ValueError('Provide exactly three habits.')
    for h in habits:
        if not isinstance(h, dict):
            raise ValueError('Each habit must be an object.')
        for field, limit in [('title', 60), ('action', 140)]:
            value = h.get(field)
            if not isinstance(value, str) or not value.strip() or len(value) > limit or any(c in value for c in '\r\n'):
                raise ValueError('Habit titles and actions must be short, nonempty single-line strings.')
        if 'id' in h and (not isinstance(h['id'], str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', h['id'])):
            raise ValueError('Habit IDs must contain 1-80 letters, numbers, underscores or hyphens.')


def resolve_habits(incoming, catalog, now):
    validate_habits(incoming)
    result = []
    for source in incoming:
        h = {'title': source['title'], 'action': source['action']}
        identity = source.get('id')
        if not identity:
            matches = [x['id'] for x in catalog.values() if x['title'] == h['title'] and x['action'] == h['action']]
            if len(matches) > 1:
                raise ValueError('Habit wording matches several identities; supply its ID.')
            identity = matches[0] if matches else 'habit_'+uuid.uuid4().hex
        old = catalog.get(identity)
        h.update(id=identity, introduced_at_utc=old['introduced_at_utc'] if old else now)
        result.append(h)
    if len({h['id'] for h in result}) != len(result):
        raise ValueError('The three habits must have distinct IDs.')
    return result


def load_state(directory):
    path = directory/'practice-state.json'
    if path.exists():
        state = json.loads(path.read_text())
        if state.get('schema_version') != 1:
            raise ValueError('Unsupported practice-state version; leave it unchanged.')
        return state
    state = {'schema_version':1, 'current_habits':[], 'habit_catalog':{}, 'weeks':{}, 'current_from_week':None}
    legacy = directory/'sticky-state.json'
    if legacy.exists():
        for old in json.loads(legacy.read_text()).get('habits', []):
            identity = old.get('id') or 'habit_'+uuid.uuid5(uuid.NAMESPACE_URL, 'review-prompting:'+old['title']+'\n'+old['action']).hex
            h = dict(old, id=identity, introduced_at_utc=old.get('introduced_at_utc') or utc_now())
            state['current_habits'].append(h)
            state['habit_catalog'][identity] = deepcopy(h)
    return state


def update_current(directory, incoming, now=None):
    directory = private_dir(directory)
    with state_lock(directory):
        state = load_state(directory)
        habits = resolve_habits(incoming, state['habit_catalog'], now or utc_now())
        state['current_habits'] = habits
        state['habit_catalog'].update({h['id']:deepcopy(h) for h in habits})
        atomic_json(directory/'practice-state.json', state)
        return deepcopy(habits)


def begin_review(directory, zone, reference):
    directory = private_dir(directory)
    window = previous_week(reference, zone)
    key = window['report_key']
    with state_lock(directory):
        state = load_state(directory)
        if key not in state['weeks']:
            baseline = state['current_habits']
            if state.get('current_from_week') and state['current_from_week'] >= key:
                earlier = [k for k, r in state['weeks'].items() if k < key and r.get('next_habits')]
                baseline = state['weeks'][max(earlier)]['next_habits'] if earlier else []
            state['weeks'][key] = {'window':window, 'baseline_habits':deepcopy(baseline),
                                   'baseline_captured_at_utc':utc_now(), 'report':None,
                                   'revisions':[], 'next_habits':None, 'desktop':{'status':'not_attempted'}}
        record = state['weeks'][key]
        if record['window'] != window:
            raise ValueError('This week was captured in a different timezone; reconcile before continuing.')
        atomic_json(directory/'practice-state.json', state)
        return deepcopy(record)


def publish_review(directory, key, markdown, next_habits, report_url=None, now=None):
    directory = private_dir(directory)
    if date.fromisoformat(key).weekday() != 0:
        raise ValueError('The report key must be a Monday date.')
    if not isinstance(markdown, str) or not markdown.strip():
        raise ValueError('The report must not be empty.')
    with state_lock(directory):
        state = load_state(directory)
        if key not in state['weeks']:
            raise ValueError('Begin the review before publishing, so its baseline is captured.')
        record = state['weeks'][key]
        habits = resolve_habits(next_habits, state['habit_catalog'], now or utc_now())
        path = directory/'reports'/(key+'.md')
        path.parent.mkdir(exist_ok=True)
        checksum = hashlib.sha256(markdown.encode()).hexdigest()
        if record['report'] and record['report']['sha256'] != checksum:
            record['revisions'].append(deepcopy(record['report']))
            # Preserve the exact superseded text, not just its hash.
            revision = path.with_name(key+'-revision-'+str(len(record['revisions']))+'.md')
            revision.write_text(record['report']['markdown'])
        temp = path.with_suffix('.tmp')
        temp.write_text(markdown)
        temp.replace(path)
        url = report_url or (record['report']['url'] if record['report'] else path.as_uri())
        record['report'] = {'path':str(path), 'url':url, 'sha256':checksum, 'markdown':markdown}
        record['next_habits'] = habits
        current = state.get('current_from_week')
        historical = current is not None and key < current
        if not historical:
            state['habit_catalog'].update({h['id']:deepcopy(h) for h in habits})
            state['current_habits'] = habits
            state['current_from_week'] = key
        atomic_json(directory/'practice-state.json', state)
        return {'report':deepcopy(record['report']), 'baseline_habits':deepcopy(record['baseline_habits']),
                'next_habits':deepcopy(habits), 'historical':historical}


def record_desktop(directory, key, status, detail=''):
    if status not in {'updated', 'blocked', 'skipped'}:
        raise ValueError('Desktop status must be updated, blocked or skipped.')
    directory = private_dir(directory)
    with state_lock(directory):
        state = load_state(directory)
        if not state['weeks'][key]['report']:
            raise ValueError('Publish the report before recording the desktop result.')
        state['weeks'][key]['desktop'] = {'status':status, 'detail':detail}
        atomic_json(directory/'practice-state.json', state)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', required=True, type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    begin = commands.add_parser('begin')
    begin.add_argument('--timezone', required=True)
    begin.add_argument('--as-of', help='ISO reference time including an offset')
    publish = commands.add_parser('publish')
    publish.add_argument('--week', required=True)
    publish.add_argument('--report', required=True, type=Path)
    publish.add_argument('--habits', required=True, type=Path)
    publish.add_argument('--report-url')
    desktop = commands.add_parser('desktop')
    desktop.add_argument('--week', required=True)
    desktop.add_argument('--status', required=True, choices=['updated','blocked','skipped'])
    desktop.add_argument('--detail', default='')
    args = parser.parse_args()
    if args.command == 'begin':
        reference = datetime.fromisoformat(args.as_of.replace('Z','+00:00')) if args.as_of else datetime.now(timezone.utc)
        result = begin_review(args.state_dir, args.timezone, reference)
    elif args.command == 'publish':
        result = publish_review(args.state_dir, args.week, args.report.read_text(), json.loads(args.habits.read_text())['habits'], args.report_url)
    else:
        record_desktop(args.state_dir, args.week, args.status, args.detail)
        result = {'status':args.status}
    print(json.dumps(result))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, RuntimeError) as exc:
        parser_error = {'status':'blocked', 'error':str(exc)}
        print(json.dumps(parser_error))
        raise SystemExit(1)
