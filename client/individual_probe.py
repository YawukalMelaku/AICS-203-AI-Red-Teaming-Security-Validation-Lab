#!/usr/bin/env python3
"""Submit one bounded, lab-only test case through an SSH tunnel."""
import argparse
import json
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--scenario', required=True, choices=['retrieval','disclosure','tool','output'])
parser.add_argument('--mode', default='baseline', choices=['baseline','hardened'])
parser.add_argument('--text', default='')
parser.add_argument('--document', default='')
parser.add_argument('--operation', default='read_record')
parser.add_argument('--lab-token', default='student-demo', choices=['student-demo','instructor-demo'])
a = parser.parse_args()
payload = {'scenario': a.scenario, 'mode': a.mode, 'text': a.text,
           'document': a.document, 'operation': a.operation, 'lab_token': a.lab_token}
request = urllib.request.Request('http://127.0.0.1:8765/evaluate', data=json.dumps(payload).encode(),
                                 headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(request, timeout=8) as response:
    print(json.dumps(json.load(response), indent=2))
