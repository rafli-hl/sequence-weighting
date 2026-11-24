"""Assembles FINDINGS.md from the hand-written parts and the scripts and outputs in this scratch folder (post hoc audit helper)."""
import sys
from pathlib import Path
S = Path(sys.argv[1])
PY = '"C:\\Users\\rafli\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" -I -B'
CL, SC = 'C:\\Users\\rafli\\AppData\\Local\\Temp\\swa21\\d\\repo', 'C:\\Users\\rafli\\AppData\\Local\\Temp\\swa21\\d\\scratch'


def text(name, enc='utf-8'):
    b = (S / name).read_bytes()
    if b[:2] in (b'\xff\xfe', b'\xfe\xff'): enc = 'utf-16'
    return b.decode(enc).replace('\r\n', '\n').lstrip('\ufeff').rstrip('\n')


def block(body, lang=''): return f'```{lang}\n{body}\n```\n'


out = [text('_body_1.md').replace('`PILOT_LOG.json:30–31, 141`', '`PILOT_LOG.json:30–31, 156`'), '']
out.append('## 4. Scripts I wrote (all post hoc), with their commands and output\n')
out.append('All are in `' + SC + '`. They read only my clone and dummy folders they create in the scratch folder. The published `check_run.py` and `RUN_COMMAND.ps1` were never run: d03, d04 and d06 run a scratch copy of the check whose one changed line is `STUDY`, and d05 executes eleven and three lines taken unchanged from `RUN_COMMAND.ps1` with `$study` set to a dummy folder.\n')
items = [
    ('d01_hash_checks.py', 'pinned hashes, the sealed source, the three subjects, the pilot seeds, the terminal hashes', f'{PY} d01_hash_checks.py "{CL}"', 'python', ['d01_hash_checks.out']),
    ('d02_dummy_study.py', 'a dummy study with invented contents (every "loss" is the sentinel 6.283185)', f'{PY} d02_dummy_study.py "{CL}" "{SC}"\n{PY} d02_dummy_study.py "{CL}" "{SC}" dummy-study-refused refused', 'python', ['d02_dummy_study.out', 'd02_dummy_study_refused.out']),
    ('d03_run_check_copy.py', 'a scratch copy of check_run.py on the dummy runs: number of checks, and whether a loss value is printed', f'{PY} d03_run_check_copy.py "{CL}" "{SC}"', 'python', ['d03_run_check_copy.out']),
    ('d04_hook_test.py', 'the audit hook of check_run.py, through the scratch copy, on the dummy study', f'{PY} d04_hook_test.py "{SC}" X2\n{PY} d04_hook_test.py "{SC}" R1   (below: the X2 output in full, then the R1 lines that differ in kind)', 'python', ['d04_hook_test_X2.out']),
    ('d05_run_order_test.ps1', 'the run-order rule and the approval checks of RUN_COMMAND.ps1, on dummy folders (Windows PowerShell 5.1)', f"& '{SC}\\d05_run_order_test.ps1' -Clone '{CL}' -Scratch '{SC}'", 'powershell', ['d05_run_order_test.out']),
]
for i, (name, what, cmd, lang, outs) in enumerate(items, 1):
    out.append(f'### 4.{i} `{name}`: {what}\n')
    out.append('Command:\n\n' + block(cmd))
    out.append('Script:\n\n' + block(text(name), lang))
    for o in outs: out.append('Output:\n\n' + block(text(o)))
    if name == 'd04_hook_test.py':
        r1 = [ln for ln in text('d04_hook_test_R1.out').split('\n') if any(k in ln for k in ('roots for', 'dummy-study\\', 'R2 TERMINAL', 'R2 n06/INPUTS', 'R1 TERMINAL', 'outside the study'))]
        out.append('Output for R1 (selected lines):\n\n' + block('\n'.join(r1)))
    if name == 'd03_run_check_copy.py':
        out.append('The full output of each dummy check is in `d03_check_R1.out`, `d03_check_R2.out`, `d03_check_X2.out` and `d03_check_R1_corrupt.out` in the scratch folder.\n')
out.append('### 4.6 d06: the scratch copy of the check on a dummy R1 with one refused start (no new script)\n')
out.append('Command:\n\n' + block(f'{PY} check_run_copy.py R1 --study "{SC}\\dummy-study-refused" --n-train 1024 > d06_check_R1_refused.out 2>&1; echo "exit $?"\ngrep -E "^FAIL|passed, .* failed|other failure|inventory failure" d06_check_R1_refused.out | cut -c1-330'))
ref = [ln[:330] for ln in text('d06_check_R1_refused.out').split('\n') if ln.startswith('FAIL') or 'passed, ' in ln or 'other failure' in ln or 'inventory failure' in ln]
out.append('Output:\n\n' + block('exit 1\n' + '\n'.join(ref)))
out.append(text('_body_5.md'))
final = '\n'.join(out).rstrip('\n') + '\n'
(S / 'FINDINGS.md').write_bytes(final.encode('utf-8'))
print('FINDINGS.md', len(final.encode('utf-8')), 'bytes,', final.count('\n'), 'lines')
