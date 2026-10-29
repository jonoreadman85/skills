#!/usr/bin/env python3
"""Create/update one prompting reminder; keep user state outside the skill package."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse

from practice_store import state_lock, update_current, validate_habits

TITLE = 'BEFORE I PROMPT'
CUE = 'Open chat. Pause. Choose one habit.'

# Arguments are data, never interpolated into executable AppleScript/JavaScript.
AUTOMATION = r'''
function run(argv) {
    const cfg = JSON.parse(argv[0]);
    const app = Application('Stickies');
    const wasRunning = app.running();
    if (!wasRunning && cfg.checkOnly) return JSON.stringify({status:'not_running'});
    app.activate();
    delay(0.3);
    const p = Application('System Events').processes.byName('Stickies');
    function area(w) { return w.scrollAreas[0].textAreas[0]; }
    let matches = [];
    for (const w of p.windows()) {
        if (!w.name().startsWith(cfg.title)) continue;
        try {
            const text = area(w).value();
            if (text.split('\n')[0] === cfg.title) matches.push({w,text});
        } catch (_) {}
    }
    if (matches.length > 1) throw Error('Multiple reminder notes found; resolve duplicates manually.');
    if (cfg.checkOnly) return JSON.stringify({status:matches.length?'found':'missing', text:matches.length?matches[0].text:null});
    let status = 'updated', w;
    if (matches.length) {
        w = matches[0].w;
        const old = matches[0].text;
        if (cfg.expected !== null && old !== cfg.expected && old !== cfg.text)
            throw Error('Reminder was edited outside this workflow; keep it and reconcile the edits first.');
        if (cfg.expected === null && old.indexOf(cfg.cue) < 0)
            throw Error('An unrecognised note has the same title; do not overwrite it.');
        status = old === cfg.text ? 'unchanged' : (cfg.expected === null ? 'adopted_and_updated' : 'updated');
        w.actions.byName('AXRaise').perform();
    } else {
        p.menuBars[0].menuBarItems.byName('File').menus[0].menuItems.byName('New Note').click();
        delay(0.3);
        w = p.windows[0];
        if (area(w).value()) throw Error('New note is not empty; refusing to overwrite it.');
        status = 'created';
    }
    const current = area(w).value();
    if (current !== cfg.text && current !== (matches.length ? matches[0].text : ''))
        throw Error('Note changed during setup; refusing to overwrite it.');
    area(w).attributes.byName('AXValue').value = cfg.text;
    delay(0.3);
    if (area(w).value() !== cfg.text) throw Error('Note text could not be verified.');
    // Re-raise the owned note before touching a menu that acts on the key window.
    w.actions.byName('AXRaise').perform();
    delay(0.2);
    const front = p.windows[0];
    if (area(front).value() !== cfg.text) throw Error('Reminder is not the selected note.');
    const item = p.menuBars[0].menuBarItems.byName('Window').menus[0].menuItems.byName('Float on Top');
    if (!item.attributes.byName('AXMenuItemMarkChar').value()) item.click();
    delay(0.2);
    return JSON.stringify({status, text:area(front).value(), floating:!!item.attributes.byName('AXMenuItemMarkChar').value()});
}
'''

LAYOUT = '''on run argv
tell application "System Events"
tell process "Stickies"
if value of text area 1 of scroll area 1 of window 1 is not item 1 of argv then error "Reminder is not selected"
set size of window 1 to {370, 440}
set position of window 1 to {40, 80}
end tell
end tell
end run
'''


def render(data):
    if not isinstance(data, dict):
        raise ValueError('Habits JSON must be an object.')
    habits = data.get('habits')
    validate_habits(habits)
    lines = [TITLE, '']
    for i, habit in enumerate(habits, 1):
        title, action = habit.get('title'), habit.get('action')
        lines.extend([f'{i}. {title.strip()}', action.strip(), ''])
    lines.append(CUE)
    link = data.get('report_url')
    if link:
        if not isinstance(link, str) or any(c in link for c in '\r\n') or urlparse(link).scheme not in {'https', 'file'}:
            raise ValueError('Use an HTTPS report link or an absolute file URI.')
        if urlparse(link).scheme == 'https' and not urlparse(link).netloc:
            raise ValueError('The report link needs a hostname.')
        if urlparse(link).scheme == 'file' and not urlparse(link).path.startswith('/'):
            raise ValueError('The file URI must be absolute.')
        lines.extend(['', 'Full list and report:', link])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--habits', required=True, type=Path, help='JSON with three habits and optional report_url')
    parser.add_argument('--state-dir', required=True, type=Path, help='Private persistent directory outside the skill checkout')
    parser.add_argument('--dry-run', action='store_true', help='Validate and print text; do not touch the desktop or state')
    args = parser.parse_args()
    data = json.loads(args.habits.read_text())
    text = render(data)
    state_dir = args.state_dir.expanduser().resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    if state_dir == skill_dir or skill_dir in state_dir.parents:
        raise ValueError('State must be outside the reusable skill package.')
    state_file = state_dir / 'sticky-state.json'
    previous = json.loads(state_file.read_text()) if state_file.exists() else {}
    if args.dry_run:
        print(json.dumps({'status':'dry_run', 'text':text, 'has_state':bool(previous)}))
        return 0
    if sys.platform != 'darwin':
        print(json.dumps({'status':'unsupported_platform', 'text':text}))
        return 2
    with state_lock(state_dir, 'sticky.lock'):
        previous = json.loads(state_file.read_text()) if state_file.exists() else {}
        # Practice identity persists independently of whether desktop access succeeds.
        data = dict(data, habits=update_current(state_dir, data['habits']))
        payload = {'title':TITLE, 'cue':CUE, 'text':text, 'expected':previous.get('last_text'), 'checkOnly':False}
        # Inspect once before writing. A missing permission or duplicate note stops this run.
        check = dict(payload, checkOnly=True)
        for request in [check, payload]:
            result = subprocess.run(['/usr/bin/osascript','-l','JavaScript','-',json.dumps(request)],
                                    input=AUTOMATION, text=True, capture_output=True, timeout=20)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or 'Stickies automation failed.')
            receipt = json.loads(result.stdout)
        status = receipt['status']
        if status == 'created':
            layout = subprocess.run(['/usr/bin/osascript', '-', text], input=LAYOUT,
                                    text=True, capture_output=True, timeout=20)
            if layout.returncode:
                raise RuntimeError(layout.stderr.strip() or 'New reminder could not be sized.')
            verify = subprocess.run(['/usr/bin/osascript','-l','JavaScript','-',json.dumps(payload)],
                                    input=AUTOMATION, text=True, capture_output=True, timeout=20)
            if verify.returncode:
                raise RuntimeError(verify.stderr.strip() or 'Resized reminder could not be verified.')
            receipt = json.loads(verify.stdout)
        if receipt.get('text') != text:
            raise RuntimeError('The saved note text was not verified; state was not advanced.')
        updated_at = datetime.now(timezone.utc).isoformat()
        habits = data['habits']
        state = {'schema_version':1, 'setup_complete':bool(receipt.get('floating')),
                 'last_text':text, 'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                 'last_updated_utc':updated_at,
                 'habits':habits, 'report_url':data.get('report_url'),
                 'floating_verified':bool(receipt.get('floating'))}
        temp = state_file.with_suffix('.tmp')
        temp.write_text(json.dumps(state, indent=2)+'\n')
        temp.replace(state_file)
        print(json.dumps({'status':status, 'floating':state['floating_verified'], 'state_file':str(state_file)}))
        return 0 if state['setup_complete'] else 2


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status':'blocked', 'error':str(exc)}), file=sys.stderr)
        sys.exit(1)
