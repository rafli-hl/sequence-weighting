"""Frozen plan of the dense-readout replication, N8 (N8-protocol-draft.md). Pure constants. Derived from N7's matched_plan.py.

Twenty-four fresh WikiText-103 draws n01-n24 in eight runs R1-R8 of three draws, with the few-epoch recipe at 1e-4 only, 3.5 epochs
and readouts at E0.25, E0.5, E1, then every 64 updates from update 2,048 to 3,584. A run that does not complete is repeated once, from
scratch with the same seeds, by its retry run X1-X8: the draws it did not complete (protocol section 8). Per draw, each width's E0
state is kept, and each epoch's batch order is saved with its SHA-256 (protocol section 3). The analysis is analysis/n8_analysis.py
(protocol section 6); nothing here labels anything.
No rate is chosen: 1e-4 is 768's lowest validation NLL on t00, by validation NLL only. The shared recipe and limits come from
fewepoch_plan.py, a byte copy.
The seed policy is pinned before the owner-run seed draw. The registry and partition pins are None until a pin-only revision sets them
after that draw; the worker and the builder refuse real mode while any is None. Importing this module cannot read data, import a
framework or launch anything.
"""
import fewepoch_plan as fp
import matched_data as md

EXECUTION_ENABLED = False

# Paths. The corpus is relative to the closed record's root (text_worker.ROOT) and only read; the rest is relative to this study's root.
STUDY_ROOT = dict(posix='/mnt/d/sequence-weighting-n8', nt=r'D:\sequence-weighting-n8')
SOURCE = 'source'
CORPUS = fp.CORPUS
RUN_MODES = tuple(f'R{k}' for k in range(1, 9))
RETRY_MODES = tuple(f'X{k}' for k in range(1, 9))
MODES = RUN_MODES + RETRY_MODES
ACTIVATIONS = {m: f'activations/n8-{m.lower()}' for m in MODES}
RUNS = {m: f'runs/n8-{m.lower()}' for m in MODES}

# The frozen seed policy, and the owner-run seed draw and its partition (None until they exist).
REGISTRY = dict(directory='registry/n8-seed-registry',
                policy_sha256='6dde3e233abaa644df4a04df364542f42e67e57a97418faea17dc2e4d6209943',
                registry_sha256='7628c80950fe14e130336909d3fb995fa35dcad3f836d2fd90ddd8071c96fd3e',
                exclusions_sha256='232e3e60235e82e302905ece260c19148c0f7e44f2f58cd9cf7a951d58ad4555',
                draw_sha256='58489c76bbcd9989527cc0377aa154aaac2a6733b2de623f278576e7784bdcda',
                approval_id='OWNER-20261114-N8-SEEDS-01')
PARTITION_SHA256 = '15c1d59876fa0c09b5e34c62f1d0ed278db37c69c878667142da1b297183f42a'


def pins_set():
    return all(v is not None for v in (REGISTRY['registry_sha256'], REGISTRY['exclusions_sha256'], REGISTRY['draw_sha256'], REGISTRY['approval_id'], PARTITION_SHA256))


# The three earlier registries whose articles are out (their pins; the registries live in the closed record's reports/).
PEAK_REGISTRY = dict(directory='reports/natural-text-peak-seed-registry-20261103-01', registry_sha256='0e8b05285a6ad98a32a2041f0907e423c9c8d85fa6408e6a90be9acfb8c326dd')
PEAK_PARTITION_SHA256 = md.PEAK_PARTITION_SHA256
N7_REGISTRY = dict(directory='reports/natural-text-matched-seed-registry-20261104-01', registry_sha256='bee578826fbdb5e66fbb36d577e45929af756e05b12b62d6cd141b4b5da7ea64')
N7_PARTITION_SHA256 = md.N7_PARTITION_SHA256

# Groups and runs.
GROUPS = md.GROUPS
RUN_STAGES = {m: GROUPS[3 * i:3 * i + 3] for i, m in enumerate(RUN_MODES)}
RETRY_OF = dict(zip(RETRY_MODES, RUN_MODES))  # X<k> repeats, once, the draws of R<k> that its terminal does not record as complete
N_TRAIN = md.N_TRAIN

# The rate and the arms. The two widths share each draw's tokens, weights and batch orders.
RATE = 1e-4
RATE_SOURCE = dict(file='reports/natural-text-peak-analysis-approval-20261103-01/pinned-records/LR_SELECTION.json', sha256='fa760ba0d693518ba1b98a40f366899ebec3a013ff03863284a3ac2c32b5ad01')
WIDTHS = (512, 768)
BENCH_WIDTHS = WIDTHS                         # the start-up benchmark, 768 last
ARMS = {768: (RATE,), 512: (RATE,)}           # per draw: widest first; each width's E0 state is kept
TAG = fp.rate_tag(RATE)

# Readouts, in epochs; a readout follows update round(e x N / 16). E0 is each width's pre-trained state.
READOUTS = (0.25, 0.5, 1) + tuple(2 + k / 16 for k in range(25))     # then 2, 2.0625, ..., 3.5: every 64 updates from 2,048 to 3,584
LAST_READOUT = 3.5
ORDER_EPOCHS = 4                              # batch orders are drawn per epoch; the fourth is used up to E3.5
FINAL, PREVIOUS = fp.FINAL, fp.PREVIOUS       # E3 and E2
MATCH_PATH = tuple(e for e in READOUTS if e >= 2)                    # 25 readouts, E2 to E3.5
ORDER_FILE = 'ORDERS.i64'                     # per draw: the ORDER_EPOCHS orders, one row each, as little-endian int64 sequence indices
