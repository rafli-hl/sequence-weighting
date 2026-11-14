"""The post-draw revision of N8's source after the owner-run seed draw (the brief, step 5). Native Python 3.12, -I -B.

  python -I -B apply_pins.py        -> source/matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1 revised in place; prints the diff

It refuses unless the registry folder holds the drawn registry, its exclusions, draw and partition, and a post-draw check record that
passed and names the same registry and partition, and unless the plan's registry and partition pins are all still None. It then sets the
five pins in matched_plan.py (the registry, exclusions and draw hashes, the approval id and the partition hash), replaces the README's
two status lines (build_n8_subject.README_PENDING by README_DRAWN), and replaces the owner script's hours line and start message
(OWNER_PENDING by OWNER_DRAWN; the owner's decision of 14 Nov 2026). Nothing else changes, and nothing is written unless every
replacement applies. build_n8_subject.py then seals the revision, and accepts nothing more against the pending seal kept in seal/pre-pin/.
"""
import difflib, hashlib, json, re, sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent; STUDY = HERE.parent
sys.path.insert(0, str(HERE))
import build_n8_subject as bs
sha = lambda b: hashlib.sha256(b).hexdigest()


def revise(src=STUDY / 'source', reg_dir=STUDY / bs.REGISTRY_DIR, out=print):
    plan_path, readme_path, owner_path = src / 'matched_plan.py', src / 'README.md', src / 'MATCHED_OWNER_RUN.ps1'
    plan, readme, owner = (p.read_bytes().decode('utf-8') for p in (plan_path, readme_path, owner_path))
    names = ('REGISTRY.json', 'EXCLUSIONS.json', 'DRAW.json', 'PARTITION.json', 'REGISTRY_AND_PARTITION_CHECK.json')
    missing = [n for n in names if not (reg_dir / n).is_file()]
    if missing: raise SystemExit(f'The drawn registry is not complete: {missing}; nothing changed')
    raw = {n: (reg_dir / n).read_bytes() for n in names}; reg, checked = json.loads(raw['REGISTRY.json']), json.loads(raw['REGISTRY_AND_PARTITION_CHECK.json'])
    if checked.get('all_pass') is not True: raise SystemExit('The post-draw checks did not all pass; nothing changed')
    pins = dict(registry_sha256=sha(raw['REGISTRY.json']), exclusions_sha256=sha(raw['EXCLUSIONS.json']), draw_sha256=sha(raw['DRAW.json']), approval_id=reg.get('approval_id'), partition_sha256=sha(raw['PARTITION.json']))
    if (reg.get('partition_sha256'), checked.get('registry_sha256'), checked.get('partition_sha256')) != (pins['partition_sha256'], pins['registry_sha256'], pins['partition_sha256']):
        raise SystemExit('The registry, its partition and the check record do not name each other; nothing changed')
    if Path(src).resolve() == (STUDY / 'source').resolve() and (reg.get('fixture') is not False or str(pins['approval_id']).upper().startswith('FIXTURE')):
        raise SystemExit('The study source takes only a real registry; nothing changed')
    if not re.fullmatch('[A-Z0-9-]+', str(pins['approval_id'])): raise SystemExit('The approval id cannot be written as a pin; nothing changed')
    if bs.unpinned(plan) != plan: raise SystemExit('The plan already pins a registry; nothing changed')
    new_plan = plan
    for key in ('registry_sha256', 'exclusions_sha256', 'draw_sha256', 'approval_id'):
        new_plan, n = re.subn(rf'(?m)^( {{16}}{key}=)None', lambda m: m.group(1) + repr(pins[key]), new_plan)
        if n != 1: raise SystemExit(f'The plan does not hold one {key}=None; nothing changed')
    new_plan, n = re.subn(r'(?m)^(PARTITION_SHA256 = )None', lambda m: m.group(1) + repr(pins['partition_sha256']), new_plan)
    if n != 1: raise SystemExit('The plan does not hold one PARTITION_SHA256 = None; nothing changed')
    new_readme = bs.revised(readme, bs.README_PENDING, bs.README_DRAWN, 'README')
    new_owner = bs.revised(owner, bs.OWNER_PENDING, bs.OWNER_DRAWN, 'owner script')
    diff = ''.join(line for a, b, name in ((plan, new_plan, 'matched_plan.py'), (readme, new_readme, 'README.md'), (owner, new_owner, 'MATCHED_OWNER_RUN.ps1'))
                   for line in difflib.unified_diff(a.splitlines(True), b.splitlines(True), f'a/source/{name}', f'b/source/{name}'))
    for p, t in ((plan_path, new_plan), (readme_path, new_readme), (owner_path, new_owner)): p.write_bytes(t.encode('utf-8'))
    out(diff)
    return pins, diff


if __name__ == '__main__':
    if len(sys.argv) != 1: raise SystemExit(__doc__)
    revise()
