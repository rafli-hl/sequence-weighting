"""POST HOC audit script (area D). Tests the audit hook of the published check_run.py (read_only + roots) on the DUMMY study in the
auditor's scratch folder, through the scratch copy check_run_copy.py (one line changed: STUDY). It installs the hook exactly as main()
does for mode X2, then tries reads, listings, writes, processes and network use inside and outside the allowed roots, and prints what
was allowed or refused. Nothing on drive D: is touched: every path is inside the scratch folder.

usage: python -I -B d04_hook_test.py <scratch> <mode>
"""
import importlib.util, os, sys
from pathlib import Path

SCRATCH, MODE = Path(sys.argv[1]), sys.argv[2]
STUDY = SCRATCH / 'dummy-study'
spec = importlib.util.spec_from_file_location('check_run_copy', SCRATCH / 'check_run_copy.py'); cr = importlib.util.module_from_spec(spec); spec.loader.exec_module(cr)
assert os.path.normcase(cr.STUDY) == os.path.normcase(str(STUDY))

# An outside file, a sibling folder whose name starts like an allowed root, both inside the scratch folder (made before the hook).
outside = SCRATCH / 'outside-root'; outside.mkdir(exist_ok=True); (outside / 'secret.f32').write_bytes(b'\x00' * 16)
sibling = STUDY / 'runs' / f'n8-{MODE.lower()}-other'; sibling.mkdir(exist_ok=True); (sibling / 'x.json').write_bytes(b'{}')

roots = cr.roots(str(STUDY), MODE)
print('roots for', MODE + ':'); [print('   ', os.path.relpath(r, SCRATCH)) for r in roots]
cr.read_only(roots)                                     # irreversible for this process, as in check_run.main()
import glob, json, shutil, socket, subprocess
import numpy as np                                      # imported after the hook, as check_run.py does
print('numpy imported under the hook:', np.__version__)

run, act = STUDY / 'runs' / f'n8-{MODE.lower()}', STUDY / 'activations' / f'n8-{MODE.lower()}'
r2, r1 = STUDY / 'runs' / 'n8-r2', STUDY / 'runs' / 'n8-r1'


def attempt(label, fn):
    try: fn(); print(f'  ALLOWED  {label}')
    except PermissionError as e: print(f'  REFUSED  {label}   [{str(e)[:70]}]')
    except Exception as e: print(f'  ERROR    {label}   [{type(e).__name__}: {str(e)[:70]}]')


print('-- reads inside the allowed roots')
attempt('open run TERMINAL.json', lambda: open(run / 'TERMINAL.json', 'rb').close())
attempt('open activation AUTHORIZATION.json', lambda: open(act / 'AUTHORIZATION.json', 'rb').close())
attempt('open source matched_plan.py', lambda: open(STUDY / 'source' / 'matched_plan.py', 'rb').close())
attempt('same path in upper case', lambda: open(str(run / 'TERMINAL.json').upper(), 'rb').close())
attempt('list the run folder (os.listdir)', lambda: os.listdir(run))
attempt('rglob the run folder', lambda: list(run.rglob('*')))
attempt('np.frombuffer of a run array via read_bytes', lambda: np.frombuffer(next(run.rglob('arrays.f32')).read_bytes(), dtype='<f4'))
print('-- the first attempt R2 (allowed only for X2: its terminal and the folders of the draws X2 repeats)')
attempt('open R2 TERMINAL.json', lambda: open(r2 / 'TERMINAL.json', 'rb').close())
attempt('open R2 n06/INPUTS.json (the draw X2 repeats)', lambda: open(r2 / 'n06' / 'INPUTS.json', 'rb').close())
attempt('open R2 n06/w768/E0.f32', lambda: open(r2 / 'n06' / 'w768' / 'E0.f32', 'rb').close())
attempt('open R2 n04/INPUTS.json (a draw X2 does not repeat)', lambda: open(r2 / 'n04' / 'INPUTS.json', 'rb').close())
attempt('open R2 n04/w768/lr1e-04/arrays.f32', lambda: open(r2 / 'n04' / 'w768' / 'lr1e-04' / 'arrays.f32', 'rb').close())
attempt('open R2 BENCHMARK.json', lambda: open(r2 / 'BENCHMARK.json', 'rb').close())
attempt('open R2 n04-RECEIPT.json', lambda: open(r2 / 'n04-RECEIPT.json', 'rb').close())
attempt('list R2 run folder', lambda: os.listdir(r2))
attempt('open activations/n8-r2/OWNER_EXIT_RECEIPT.json', lambda: open(STUDY / 'activations' / 'n8-r2' / 'OWNER_EXIT_RECEIPT.json', 'rb').close())
print('-- other runs and anything else')
attempt('open R1 TERMINAL.json', lambda: open(r1 / 'TERMINAL.json', 'rb').close())
attempt('open R1 array via np.fromfile', lambda: np.fromfile(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32', dtype='<f4'))
attempt('np.memmap of an R1 array', lambda: np.memmap(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32', dtype='<f4', mode='r'))
attempt('os.open(O_RDONLY) of an R1 array', lambda: os.close(os.open(r1 / 'n01' / 'w768' / 'E0.f32', os.O_RDONLY)))
attempt('open through ..\\ from the run folder', lambda: open(str(run) + '\\..\\n8-r1\\TERMINAL.json', 'rb').close())
attempt('open a file in a sibling folder n8-<run>-other', lambda: open(sibling / 'x.json', 'rb').close())
attempt('open a file outside the study', lambda: open(outside / 'secret.f32', 'rb').close())
attempt('list runs\\', lambda: os.listdir(STUDY / 'runs'))
attempt('os.scandir of the study folder', lambda: list(os.scandir(STUDY)))
attempt('os.walk of R1 (first step)', lambda: next(os.walk(r1, onerror=lambda e: (_ for _ in ()).throw(e))))
attempt('glob R1 arrays', lambda: glob.glob(str(r1 / '*' / '*' / '*' / 'arrays.f32')))
print('-- writes, processes, network')
attempt('open a run file for append', lambda: open(run / 'TERMINAL.json', 'ab').close())
attempt('create a file in the run folder', lambda: open(run / 'new.txt', 'w').close())
attempt('Path.write_bytes in the activation', lambda: (act / 'new.bin').write_bytes(b'x'))
attempt('os.remove a run file', lambda: os.remove(run / 'BENCHMARK.json'))
attempt('os.rename a run file', lambda: os.rename(run / 'BENCHMARK.json', run / 'B.json'))
attempt('os.mkdir in the run folder', lambda: os.mkdir(run / 'newdir'))
attempt('shutil.copyfile out of the run folder', lambda: shutil.copyfile(run / 'BENCHMARK.json', outside / 'copy.json'))
attempt('subprocess.run', lambda: subprocess.run(['cmd', '/c', 'echo', 'x'], capture_output=True))
attempt('os.system', lambda: os.system('echo x'))
attempt('socket.socket()', lambda: socket.socket().close())
print('-- not covered by the hook (no audit event carries a path that it checks): metadata only')
attempt('os.stat of an R1 array (size, times)', lambda: os.stat(r1 / 'n01' / 'w768' / 'lr1e-04' / 'arrays.f32'))
attempt('Path.exists / is_file outside the roots', lambda: (outside / 'secret.f32').is_file())
attempt('shutil.disk_usage of the drive', lambda: shutil.disk_usage(STUDY.anchor))
print('files in the run folder unchanged:', sorted(p.name for p in run.iterdir()))
