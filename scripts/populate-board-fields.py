#!/usr/bin/env python3
"""Fill Sprint / Role / Estimate on a Delegate project board from the ticket markdown.

Reads docs/backlog/sprint-0*-tickets.md, matches each board item by its S<n>-<nn>
ticket id, and writes the three custom fields. Safe to re-run — writes are idempotent.

Usage: populate-board-fields.py <project-number> <owner>
"""
import json, re, subprocess, sys

num, owner = sys.argv[1], sys.argv[2]


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def tickets():
    out = {}
    for sprint in ('1', '2'):
        text = open(f'docs/backlog/sprint-0{sprint}-tickets.md').read()
        for part in re.split(r'\n### ', text)[1:]:
            head, _, rest = part.partition('\n')
            m = re.match(r'(S\d-\d\d)\s+—', head.strip())
            if not m:
                continue
            meta = rest.strip().split('\n')[0]
            roles = re.findall(r'`(be|mob|ops)`', meta)
            est = re.search(r'\*\*Est:\*\* ([\d.]+)d', meta)
            out[m.group(1)] = {
                'sprint': 'S' + sprint,
                # ops-only tickets are external blockers; otherwise backend leads
                'role': 'ops' if roles == ['ops'] else ('be' if 'be' in roles else roles[0]),
                'est': est.group(1) if est else None,
            }
    return out


proj = json.loads(gh('project', 'view', num, '--owner', owner, '--format', 'json'))['id']
fields = {f['name']: f for f in json.loads(
    gh('project', 'field-list', num, '--owner', owner, '--format', 'json'))['fields']}
opt = lambda name, value: next(
    o['id'] for o in fields[name].get('options', []) if o['name'] == value)

T = tickets()
items = json.loads(gh('project', 'item-list', num, '--owner', owner,
                      '--format', 'json', '--limit', '100'))['items']
done = 0
for it in items:
    tid = it['content']['title'].split(' —')[0]
    t = T.get(tid)
    if not t:
        print('no ticket for', tid, file=sys.stderr)
        continue
    base = ['project', 'item-edit', '--project-id', proj, '--id', it['id']]
    gh(*base, '--field-id', fields['Sprint']['id'],
       '--single-select-option-id', opt('Sprint', t['sprint']))
    gh(*base, '--field-id', fields['Role']['id'],
       '--single-select-option-id', opt('Role', t['role']))
    if t['est']:
        gh(*base, '--field-id', fields['Estimate (days)']['id'], '--number', t['est'])
    done += 1
print(f'{done} items populated')
