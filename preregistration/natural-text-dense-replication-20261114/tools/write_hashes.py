"""HASHES.json of N8's registration (the brief, step 6), in the manner of N7's. Native Python 3.12, -I -B; stdlib only.

  python -I -B write_hashes.py            -> HASHES.json in the study folder (refuses unless the seal is DRAWN)
  python -I -B write_hashes.py --check    -> compares every hash in HASHES.json with its file; exit 1 on any difference

Every hash is computed from the file it names, never typed. It binds: the protocol and CHANGES.md; the sealed source subject, the pending
seal it was revised from (with the copies kept in seal/pre-pin/) and the subject the pilot ran on; the seed policy and every file of the
owner-run draw; the owner's fresh-pool count; the pilot's log; both owner commands; the analysis, the tools and the tests; and N7's
released inputs, which the analysis tests read and which are not published here.
"""
import hashlib, json, sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
REG = 'registry/n8-seed-registry'
FILES = dict(protocol='N8-protocol-draft.md', changes='CHANGES.md', sealed_source_subject='source/SOURCE_SUBJECT.json', pending_seal_before_the_draw='seal/pre-pin/SOURCE_SUBJECT.json',
             pilot_source_subject='seal/pilot/SOURCE_SUBJECT.json', seed_policy=f'{REG}/SEED_REGISTRY_POLICY.md', seed_registry=f'{REG}/REGISTRY.json', exclusions=f'{REG}/EXCLUSIONS.json',
             draw=f'{REG}/DRAW.json', draw_claim=f'{REG}/DRAW_CLAIM.json', partition=f'{REG}/PARTITION.json', registry_and_partition_check=f'{REG}/REGISTRY_AND_PARTITION_CHECK.json',
             disclosure_figures=f'{REG}/DISCLOSURE_FIGURES.md', seed_draw_receipt=f'{REG}/SEED_DRAW_RECEIPT.json', fresh_pool_count='data-count/FRESH_POOL_COUNT.json', pilot_log='pilot/PILOT_LOG.json',
             pilot_command='PILOT_COMMAND.txt', draw_command='DRAW_COMMAND.txt')
GROUPS = dict(pre_pin_copies='seal/pre-pin', analysis='analysis', tools='tools', source_tests='source-tests', tools_tests='tools-tests', retired_tests='tests-retired',
              analysis_inputs_not_published='inputs')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def group(folder):
    return {p.relative_to(STUDY).as_posix(): sha(p) for p in sorted((STUDY / folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name != 'SOURCE_SUBJECT.json'}


def hashes():
    subject = json.loads((STUDY / 'source/SOURCE_SUBJECT.json').read_bytes()); reg = json.loads((STUDY / REG / 'REGISTRY.json').read_bytes())
    if subject['seed_registry_and_partition'].get('status') != 'DRAWN': raise SystemExit('The seal is not DRAWN: run apply_pins.py and build_n8_subject.py first')
    out = dict(schema=1, published='before any activation or training run of this study', sealed_source_folder='source/ (SOURCE_SUBJECT.json lists every file with its sha256)')
    out.update({f'{k}_sha256': sha(STUDY / p) for k, p in FILES.items()})
    out.update(corpus_manifest_sha256=reg['corpus_manifest_sha256'], approval_id=reg['approval_id'], n7_partition_sha256=reg['n7_partition_sha256'])
    out.update({k: group(p) for k, p in GROUPS.items()})
    out['activation_builder_note'] = ('tools/build_n8_activation.py records the public registration (PUBLIC_REGISTRATION and EXPECTED_SUBJECT) in one revision after the merge, '
                                      'so its hash then differs from the one listed here')
    out['not_included'] = ('the corpus, run outputs (none exist), model states, and inputs/ (N7\'s released loss arrays and regenerated orders, named here by hash; '
                           'the arrays are in the release of the closed record)')
    return out


def check():
    want = json.loads((STUDY / 'HASHES.json').read_bytes()); got = hashes(); bad = sorted(k for k in set(want) | set(got) if want.get(k) != got.get(k))
    for k in bad: print('DIFFERS', k)
    print('HASHES.json matches every file' if not bad else f'{len(bad)} entries differ')
    return 0 if not bad else 1


def write():
    raw = (json.dumps(hashes(), sort_keys=False, indent=2) + '\n').encode('utf-8'); (STUDY / 'HASHES.json').write_bytes(raw)
    print('Written HASHES.json sha256', hashlib.sha256(raw).hexdigest()); return 0


if __name__ == '__main__':
    if sys.argv[1:] not in ([], ['--check']): raise SystemExit(__doc__)
    raise SystemExit(check() if sys.argv[1:] == ['--check'] else write())
