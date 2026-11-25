#!/usr/bin/env python3
"""Run supplied ethical red-team cases against the local SSH tunnel only."""
import argparse
import csv
import json
import pathlib
import urllib.request
from datetime import datetime, timezone

ENDPOINT = 'http://127.0.0.1:8765/evaluate'
HERE = pathlib.Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description='ICDFA AICS-203 controlled validation suite')
    parser.add_argument('--mode', choices=['baseline', 'hardened'], required=True)
    parser.add_argument('--out', default=None, help='Evidence folder; defaults to evidence/')
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases' / 'cases.json').read_text(encoding='utf8'))
    out = pathlib.Path(args.out) if args.out else HERE / 'evidence'
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for case in cases:
        payload = dict(case['request'], mode=args.mode)
        req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode('utf8'),
                                     headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=8) as response:
            result = json.load(response)
        expected = case['expect_policy_pass_' + args.mode]
        row = {'id': case['id'], 'module': case['module'], 'risk': case['risk'],
               'mode': args.mode, 'expected_policy_pass': expected,
               'actual_policy_pass': result['policy_pass'],
               'matched_expectation': expected == result['policy_pass'],
               'finding': result['finding'], 'result': result['result']}
        records.append(row)
        label = 'MATCH' if row['matched_expectation'] else 'REVIEW'
        print(f"{case['id']}: {label} | policy_pass={result['policy_pass']} | {result['finding']}")
    obj = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
           'target': 'local SSH forwarded simulation only', 'mode': args.mode,
           'results': records}
    (out / f'{args.mode}_results.json').write_text(json.dumps(obj, indent=2), encoding='utf8')
    with (out / f'{args.mode}_results.csv').open('w', newline='', encoding='utf8') as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"\n{sum(r['matched_expectation'] for r in records)}/{len(records)} matched expected simulator behavior")
    print(f"{sum(not r['actual_policy_pass'] for r in records)} responses violated simulated policy")
    print(f'Evidence saved in {out}')

if __name__ == '__main__':
    main()
