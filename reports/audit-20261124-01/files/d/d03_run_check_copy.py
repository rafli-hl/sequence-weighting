"""POST HOC audit script (area D). Makes a scratch copy of the published check_run.py whose ONLY change is the STUDY constant (pointed
at the dummy study in the auditor's scratch folder), then runs that copy on the three dummy runs and reports:
 - the number of checks it performs for a complete run of three draws, a run failed in its third draw, and a one-draw retry
   (to compare with the counts in OPERATIONAL_NOTES.md: 54+1, 46+1, 31+1);
 - whether the sentinel "loss" value planted in every loss field and array (6.283185) appears anywhere in its output;
 - the same on a corrupted copy of the dummy study (failure paths).
The published check_run.py is never run: only the copy, and only on the dummy folders.

usage: python -I -B d03_run_check_copy.py <clone> <scratch>
"""
import difflib, hashlib, re, shutil, subprocess, sys
from pathlib import Path

CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
SRC = CLONE / 'preregistration' / 'natural-text-dense-replication-20261114' / 'check_run.py'
STUDY = SCRATCH / 'dummy-study'
COPY = SCRATCH / 'check_run_copy.py'
PY = sys.executable

text = SRC.read_bytes().decode('utf-8')
old = "STUDY = r'D:\\sequence-weighting-n8'"
assert text.count(old) == 1, text.count(old)
assert "'" not in str(STUDY)
new = text.replace(old, "STUDY = r'" + str(STUDY) + "'")
COPY.write_bytes(new.encode('utf-8'))
print('published check_run.py sha256:', hashlib.sha256(SRC.read_bytes()).hexdigest())
print('diff published -> scratch copy:')
for line in difflib.unified_diff(text.splitlines(), new.splitlines(), 'check_run.py', 'check_run_copy.py', lineterm='', n=0): print('   ', line)
print('other mentions of drive D: left in the copy (comments and messages only):', [ln.strip()[:80] for ln in new.splitlines() if re.search(r"D:\\\\", ln)])


def run(mode, study=STUDY, extra=()):
    p = subprocess.run([PY, '-I', '-B', str(COPY), mode, '--study', str(study), '--n-train', '1024', *extra], capture_output=True, text=True, encoding='utf-8')
    out = p.stdout + p.stderr
    passes, fails = len(re.findall(r'^PASS  ', out, re.M)), len(re.findall(r'^FAIL  ', out, re.M))
    return p.returncode, out, passes, fails


for mode in ('R1', 'R2', 'X2'):
    rc, out, passes, fails = run(mode)
    (SCRATCH / f'd03_check_{mode}.out').write_text(out, encoding='utf-8')
    summary = [ln for ln in out.splitlines() if re.search(r'passed, .* failed|inventory failure|did not complete', ln)]
    print(f'== {mode}: exit {rc}; PASS lines {passes}, FAIL lines {fails}, total checks {passes + fails}')
    for ln in summary: print('    ' + ln[:230])
    print('    failed checks:', [ln[6:90] for ln in out.splitlines() if ln.startswith('FAIL  ')])
    print('    sentinel 6.28 in output:', '6.28' in out, '| any float with 4+ decimals printed:', sorted(set(re.findall(r'\b\d+\.\d{4,}\b', out)))[:8])

# Failure paths: a corrupted copy of the dummy study (truncated arrays, a missing key, a non-finite mean, an unreadable record).
BAD = SCRATCH / 'dummy-study-corrupt'
if BAD.exists(): shutil.rmtree(BAD)
shutil.copytree(STUDY, BAD)
import json
r1 = BAD / 'runs' / 'n8-r1'
a = r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32'; a.write_bytes(a.read_bytes()[:-3])
p = r1 / 'n01' / 'PRETRAINED.json'; j = json.loads(p.read_bytes()); del j['512']['E0_validation_loss']; p.write_bytes(json.dumps(j).encode())
p = r1 / 'n02' / 'w512' / 'lr1e-04' / 'record.json'; j = json.loads(p.read_bytes()); j['readouts'][3]['train_loss'] = float('nan'); p.write_bytes(json.dumps(j).encode())
p = r1 / 'n03' / 'w768' / 'lr1e-04' / 'record.json'; p.write_bytes(p.read_bytes()[:200])
p = r1 / 'n03' / 'w512' / 'E0.f32'; p.write_bytes(b'\x00' * 7)
rc, out, passes, fails = run('R1', BAD)
(SCRATCH / 'd03_check_R1_corrupt.out').write_text(out, encoding='utf-8')
print(f'== R1 on the corrupted dummy: exit {rc}; PASS {passes}, FAIL {fails}, total {passes + fails}')
print('    sentinel 6.28 in output:', '6.28' in out, '| "nan" in output:', 'nan' in out.lower(), '| floats with 4+ decimals:', sorted(set(re.findall(r'\b\d+\.\d{4,}\b', out)))[:8])
for ln in out.splitlines():
    if ln.startswith('FAIL  '): print('    ' + ln[:60] + ' ... ' + (ln[ln.rfind('['):][:150] if '[' in ln else ''))
