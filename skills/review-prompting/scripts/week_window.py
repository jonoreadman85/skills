#!/usr/bin/env python3
"""Return the previous complete Monday-to-Sunday week in a local timezone."""
import argparse
from datetime import datetime, time, timedelta
import json
from zoneinfo import ZoneInfo


def previous_week(now, timezone):
    zone = ZoneInfo(timezone)
    if now.tzinfo is None:
        raise ValueError('The reference time must include an offset.')
    today = now.astimezone(zone).date()
    end_day = today - timedelta(days=today.weekday())
    start_day = end_day - timedelta(days=7)
    return {
        'timezone': timezone,
        'start_inclusive': datetime.combine(start_day, time.min, zone).isoformat(),
        'end_exclusive': datetime.combine(end_day, time.min, zone).isoformat(),
        'report_key': start_day.isoformat(),
        'label': f'{start_day.isoformat()} to {(end_day-timedelta(days=1)).isoformat()}',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timezone', required=True)
    parser.add_argument('--as-of', help='Optional ISO reference time with an offset for reruns')
    args = parser.parse_args()
    now = datetime.fromisoformat(args.as_of.replace('Z', '+00:00')) if args.as_of else datetime.now().astimezone()
    print(json.dumps(previous_week(now, args.timezone)))
