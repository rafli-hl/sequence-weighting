"""Tests of PILOT_COMMAND.txt, the owner's command for the pilot (Windows PowerShell 5.1; native Python 3.12, -I -B). No GPU is queried and
nothing runs: the GPU and power checks are replaced by stand-ins, and the WSL call by Write-Output, which prints its arguments.

    python -I -B test_pilot_command.py

- the command's pinned hashes are those of tools/n8_pilot.py and source/SOURCE_SUBJECT.json, and its arguments are the owner's approval id,
  the subject and the five seeds in the pilot's order;
- with an idle GPU on AC power it checks every file and reaches the pilot's command line with those arguments;
- a busy GPU, battery power, or a pilot script that differs from its hash stops it before the pilot.
"""
import hashlib, re, subprocess, sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
PS_EXE = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
COMMAND = (STUDY / 'PILOT_COMMAND.txt').read_text(encoding='utf-8')
SEEDS = dict(init_seed=1188503724, weight_seed=1894175819, pretrain_order_seed=46458185, adapt_order_seed=90809628, benchmark_seed=578352808)
DOT_SOURCE = '. "$src\\gpu_check.ps1"; . "$src\\power_gate.ps1"'
WSL = 'wsl.exe -d Ubuntu --exec '
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
results = []


def check(name, ok, detail=''):
    results.append(bool(ok)); print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f'  [{detail}]' if detail else ''))


def stubbed(verdict='IDLE', power='AC', text=COMMAND):
    stubs = ("function Read-GpuConfig($p) { [pscustomobject]@{nvidia_smi='C:\\Windows\\System32\\cmd.exe'} }; function Invoke-GpuCheck { [pscustomobject]@{verdict='" + verdict + "'} }; "
             "function Format-GpuCheck($c) { 'stand-in check' }; function Get-PowerSample { [pscustomobject]@{power='" + power + "'} }; function Format-PowerSample($s) { 'stand-in power' }; "
             "function Show-PilotCommand { 'PILOT ' + ($args -join ' ') }")
    assert text.count(DOT_SOURCE) == 1 and text.count(WSL) == 1
    r = subprocess.run([PS_EXE, '-NoProfile', '-NonInteractive', '-Command', text.replace(DOT_SOURCE, stubs).replace(WSL, 'Show-PilotCommand ')], capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def main():
    pinned = dict(re.findall(r'"\$(?:study|src)\\([^"]+)" -Algorithm SHA256\)\.Hash\.ToLower\(\) -ne \'([0-9a-f]{64})\'', COMMAND))
    subject = sha(STUDY / 'source' / 'SOURCE_SUBJECT.json')
    check('the command pins the current pilot script and source subject', pinned == {'tools\\n8_pilot.py': sha(STUDY / 'tools' / 'n8_pilot.py'), 'SOURCE_SUBJECT.json': subject}, str({k: v[:16] for k, v in pinned.items()}))
    line = next(ln for ln in COMMAND.splitlines() if WSL in ln)
    args = dict(re.findall(r'--([a-z-]+) (\S+)', line.split('n8_pilot.py', 1)[1]))
    check("the pilot's arguments: the owner's approval id, the subject and the five seeds in the pilot's order",
          args.get('approval-id') == 'pilot-20261113-01' and args.get('expected-subject') == subject and all(args.get(k.replace('_', '-')) == str(v) for k, v in SEEDS.items()) and len(args) == 7, str(args))
    code, out = stubbed()
    shown = next((ln for ln in out.splitlines() if ln.startswith('PILOT ')), '')
    check('idle GPU on AC power: every file checked, and the pilot command line reached with these arguments', code == 0 and 'All files match' in out and 'GPU idle and on AC power' in out
          and shown == 'PILOT ' + line.strip()[len(WSL):], shown[:150])
    for name, kw, text in (('a busy GPU', dict(verdict='BUSY'), 'GPU not idle'), ('battery power', dict(power='BATTERY'), 'Not on AC power'),
                           ('a pilot script that differs from its hash', dict(text=COMMAND.replace(pinned['tools\\n8_pilot.py'], '0' * 64)), 'Hash differs: tools\\n8_pilot.py')):
        code, out = stubbed(**kw)
        check(f'{name} stops the command before the pilot', code != 0 and text in out and '--expected-subject' not in out, next((ln.strip() for ln in out.splitlines() if text.split(':')[0] in ln), '')[:120])
    print(f'{sum(results)} passed, {len(results) - sum(results)} failed')
    return 0 if all(results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
