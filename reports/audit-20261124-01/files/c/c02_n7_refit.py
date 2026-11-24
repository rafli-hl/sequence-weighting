"""POST HOC audit script (area C). Refit N7's 240 p* from the public loss-array bundle with n8_analysis.points and cache them.
Reads only the clone and the bundle; writes c02_per.pkl in the scratch folder.
Usage: python -I -B c02_n7_refit.py <REPO> <BUNDLE> <SCRATCH>"""
import sys, json, pickle, time, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
repo, bundle, scratch = (Path(x) for x in sys.argv[1:4])
sys.path.insert(0, str(repo / 'preregistration/natural-text-dense-replication-20261114/analysis'))
import numpy as np
import n8_analysis as na
man = json.loads((bundle / 'MANIFEST.json').read_bytes()); data = {}; bad = 0
for d, entry in man['draws'].items():
    wb = (bundle / entry['weights']['path']).read_bytes(); bad += hashlib.sha256(wb).hexdigest() != entry['weights']['sha256']
    arms = {}
    for wd, we in entry['widths'].items():
        e0 = (bundle / we['E0']['path']).read_bytes(); bad += hashlib.sha256(e0).hexdigest() != we['E0']['sha256']
        for tag, arm in we['arms'].items():
            arr = (bundle / arm['arrays']['path']).read_bytes(); bad += hashlib.sha256(arr).hexdigest() != arm['arrays']['sha256']
            arms[(int(wd), tag)] = dict(e0=e0, arrays=arr, record=json.loads((bundle / arm['record']['path']).read_bytes()))
    data[d] = dict(weights=np.frombuffer(wb, dtype='<f4').tolist(), arms=arms)
print('bundle files with a SHA-256 different from MANIFEST.json:', bad)
t0 = time.perf_counter()
per = na.points(data, sorted(data), progress=lambda d: print(f'fitted {d}, {time.perf_counter() - t0:.0f} s', flush=True))
pickle.dump(per, open(scratch / 'c02_per.pkl', 'wb'))
print('fits:', sum(len(pe) for pd in per.values() for pe in pd.values()), 'environment', na.environment())
