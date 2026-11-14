"""Write CHANGES.md: the full diff of N8's source against N7's sealed source, with one line of justification per hunk.

    python -I -B make_changes.py <N7_SEALED_SOURCE>      -> CHANGES.md in the study folder

Hunks are difflib unified hunks with one line of context. It refuses unless there is exactly one note per hunk, so a change to the
source without a note, or a note without a change, stops it. Byte copies, the new byte copy, the dropped files and the regenerated
SOURCE_SUBJECT.json are listed by hash, not diffed.
"""
import difflib, hashlib, sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]; SRC = STUDY / 'source'
CHANGED = ('matched_plan.py', 'matched_data.py', 'matched_registry.py', 'matched_worker.py', 'MATCHED_OWNER_RUN.ps1', 'AUTHORIZATION.json', 'README.md')
DROPPED = {'matched_analysis.py': "N7's analysis; N8's is `analysis/n8_analysis.py` (§6).", 'PROTOCOL.md': "N7's protocol; N8's is `N8-protocol-draft.md`."}
NOTES = {
    'matched_plan.py': [
        'Describes N8\'s plan: 24 draws at 1e-4 with dense readouts, kept E0 states and saved orders (§3), retry runs (§8); N7\'s fixed sequence is gone (§6).',
        'Paths in the study folder (brief, item "paths"); modes R1–R8 and retries X1–X8 (§8); N8\'s own registry: the frozen seed policy, pinned before the draw, and the registry and partition of the owner\'s draw of 14 Nov 2026, pinned after it (§4, §10.4).',
        'N7\'s registry and partition pinned as a third source of excluded articles (§4).',
        'Eight runs of three draws in registry order, and their retries (§8); N7\'s analysis minimum and M1→M2 rule removed (replaced by §6 and §8); one rate, 1e-4 (§3).',
        'One arm per width at 1e-4 (§3); E0 states kept (§3); readouts every 64 updates from update 2,048 to 3,584 (§3).',
        'Match path: all 25 readouts from E2 to E3.5 (§5, §6); N7\'s statistics, labels and power removed, as N8\'s are in `analysis/n8_analysis.py` (§6, §7); the order file named (§3).'],
    'matched_data.py': [
        'Describes N8\'s partition: 24 groups, with N7\'s m01–m06 among the excluded articles (§4).',
        'Draws n01–n24 (§3); N7\'s partition is re-derived with N7\'s own sealed function, so it is imported (§4).',
        '24 draws named n01–n24 (§3); N7\'s partition pinned (§4).',
        'The assigned articles now include N7\'s m01–m06, re-derived and checked against N7\'s pin (§4).',
        'Wording follows the 24 draws (§3).',
        'Message follows the 24 draws (§3).',
        'Wording follows the 24 draws (§3).'],
    'matched_registry.py': [
        'Describes the registry tool\'s changes for N8 (§4).',
        'The study folder comes from matched_plan.STUDY_ROOT, so the registry imports the plan (§4; Gate 2 review).',
        'The study folder, by OS from matched_plan.STUDY_ROOT as the worker\'s, joins the seed census, so that no seed saved there (the pilot\'s among them) can be drawn (§4: every seed recorded in a JSON file in the N8 study folder is excluded); N7\'s registry as an exclusion source (§4); the frozen N8 seed policy pinned (§4; `registry/n8-seed-registry/SEED_REGISTRY_POLICY.md`).',
        'The registry records the hash of N7\'s data function, which the draw now runs (§4).',
        'study_census: the study folder must exist and be read in full, or the draw refuses before its claim (§4; Gate 2 review).',
        'The census of the study folder (§4).',
        'The census of the study folder: the one made before the claim (§4).',
        'The draw takes N7\'s partition pin and the study folder (§4).',
        'A real draw binds N7\'s pin from the plan only, as it does the other pins (§4); the study census runs before the claim, so a missing or unreadable study folder claims nothing (§4; Gate 2 review).',
        'Before the claim, N7\'s registry must equal its pin and N7\'s partition must re-derive to its pin (§4).',
        'The exclusions use the study census made before the claim (§4).',
        'The registry records N7\'s registry and partition pins (§4); its kind names N8.',
        'Admission takes N7\'s partition pin (§4).',
        'Admission refuses a registry not bound to N7\'s registry and partition (§4).'],
    'matched_worker.py': [
        'Describes N8\'s worker: runs and retries (§8), readouts (§3), kept E0 states and saved orders (§3).',
        'Needed to choose the study folder\'s path on Linux or Windows (brief, item "paths").',
        'Activations and runs in the study folder, with the corpus still read from the closed record (brief, item "paths"); N7\'s registry pins (§4); a retry binds its first attempt\'s terminal (§8).',
        'Modes R1–R8 and X1–X8 (§8).',
        'Replaces N7\'s M2-on-M1 admission with §8\'s retry: X<k>, admitted on R<k>\'s terminal, repeats once the draws R<k> did not finish.',
        'Modes R1–R8 and X1–X8 (§8); admission covers N7\'s registry (§4).',
        'N7\'s partition pin (§4).',
        'The activation binds N7\'s registry, and N7\'s articles are excluded when the partition is re-derived (§4).',
        'A retry is admitted only on its first attempt\'s terminal, for the draws that run did not complete, and the activation must list exactly those draws (§8).',
        'The saved orders add one file and 512 KiB per draw (§3); the time cap counts a run\'s own draws, since a retry may repeat fewer than three (§8).',
        'The cap includes writing the orders (§3).',
        'The cap counts a run\'s own draws (§8).',
        'E0 states, with any partial state writes as N7\'s remove_states finds them, are listed and kept, not deleted (§3; Gate 2 review); each epoch\'s order is serialised as little-endian int64 (§3).',
        'Each epoch\'s batch order is saved, with its SHA-256 recorded in the draw\'s INPUTS.json (§3).',
        'E0 states kept (§3) and the orders re-checked at the end of the draw (§3); a retry compares its E0 losses with its first attempt\'s (§8).',
        'The run\'s draws come from admission (§8); the one-use message no longer says "no retry" (§8).',
        'The terminal names N8 and lists the run\'s draws (§8); N7\'s fixed stage list removed (§8).',
        'The cap counts the run\'s own draws (§8).',
        'The receipt reports the kept states (§3) and a retry\'s E0 comparison (§8).',
        'On failure only the benchmark\'s states are deleted; the active draw\'s E0 states are kept (§3).'],
    'MATCHED_OWNER_RUN.ps1': [
        'Describes N8\'s runs and retries (§8).',
        'Activations and runs in the study folder (brief, item "paths"); R1–R8 of three draws and X1–X8 (§8); the hours from the pilot, about 2.3 h wall time (2.1 h on the worker clock) (§7; the owner\'s decision of 14 Nov 2026, after the draw).',
        'Names N8.',
        'A retry\'s draws come from its activation and must be among R<k>\'s; a first run must list exactly its three (§8). The worker re-derives them.',
        'The activation binds N7\'s registry (§4).',
        'R1 starts only with at least 8 GB free on D:, room for the kept E0 states of all 24 draws; every run still needs 3 GiB (§3). Tested at 7.9 GB (refused) and 8 GB (admitted).',
        'The start message gives the hours on both clocks, and the 6-hour limit as the worker\'s (§7; the owner\'s decision of 14 Nov 2026, after the draw).',
        'The worker runs from the study folder (brief, item "paths").',
        'The owner\'s receipt marks a retry run (§8).',
        'The end-of-run messages state §8\'s retry rule in place of N7\'s no-retry rule.'],
    'AUTHORIZATION.json': ['Names N8; still disabled.'],
    'README.md': [
        'Describes N8\'s source, records the pilot (run on subject 9743b179… and discarded, §10.3), and points to the protocol, the analysis and this file.',
        'Lists N8\'s changed, new, dropped and byte-copied files.',
        'Status: the seed policy is frozen, and the registry and partition of the owner\'s draw are pinned (§10.4).'],
}
sha = lambda b: hashlib.sha256(b).hexdigest()


def hunks(a, b):
    out, cur = [], None
    for line in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='', n=1):
        if line.startswith(('---', '+++')): continue
        if line.startswith('@@'): cur = [line]; out.append(cur)
        else: cur.append(line)
    return out


def main(n7):
    subject = SRC / 'SOURCE_SUBJECT.json'; n7_subject = sha((n7 / 'SOURCE_SUBJECT.json').read_bytes())
    parts = ['# N8 source: every change from N7\'s sealed source', '',
             f'N8\'s source (`source/`, subject `{sha(subject.read_bytes())}`) against N7\'s sealed source (subject `{n7_subject}`). Section numbers (§) refer to '
             '`N8-protocol-draft.md`; "brief" is the owner\'s task brief for N8. Hunks have one line of context. Generated by `tools/make_changes.py`, which refuses '
             'unless every hunk has one note.', '',
             '## Unchanged', '', 'Byte copies of N7\'s sealed source, checked by `tools/build_n8_subject.py` and `source-tests/test_n8_source.py`: the model, '
             'optimiser, loss, clipping, weights, evaluation and environment gate are in these files and are unchanged.', '']
    copies = sorted(p.relative_to(SRC).as_posix() for p in SRC.rglob('*') if p.is_file() and p.relative_to(SRC).as_posix() not in CHANGED + ('SOURCE_SUBJECT.json', 'n7_matched_data.py'))
    for f in copies:
        if (SRC / f).read_bytes() != (n7 / f).read_bytes(): raise SystemExit('Not a byte copy, and no note: ' + f)
        parts.append(f'- `{f}` `{sha((SRC / f).read_bytes())[:16]}…`')
    parts += ['', '## Added, dropped and regenerated', '',
              f'- **Added** `n7_matched_data.py` `{sha((SRC / "n7_matched_data.py").read_bytes())[:16]}…`: a byte copy of N7\'s `matched_data.py`, so that N7\'s m01–m06 are re-derived with N7\'s own sealed function (§4).']
    if (SRC / 'n7_matched_data.py').read_bytes() != (n7 / 'matched_data.py').read_bytes(): raise SystemExit('n7_matched_data.py is not a byte copy')
    for f, why in DROPPED.items():
        if (SRC / f).exists(): raise SystemExit('Listed as dropped but present: ' + f)
        parts.append(f'- **Dropped** `{f}` `{sha((n7 / f).read_bytes())[:16]}…`: {why}')
    parts += [f'- **Regenerated** `SOURCE_SUBJECT.json` by `tools/build_n8_subject.py`: every file of N8\'s source with its hash, the bound records, the frozen policy, and the drawn registry and partition (DRAWN), accepted only as the post-draw revision of the pending seal kept in `seal/pre-pin/`.', '']
    total = 0
    for f in CHANGED:
        hs = hunks((n7 / f).read_text(encoding='utf-8'), (SRC / f).read_text(encoding='utf-8')); notes = NOTES[f]
        if len(hs) != len(notes): raise SystemExit(f'{f}: {len(hs)} hunks but {len(notes)} notes')
        parts += [f'## `{f}`', '']
        for k, (h, note) in enumerate(zip(hs, notes), 1):
            total += 1; parts += [f'**{total}.** {note}', '', '```diff', *h, '```', '']
    (STUDY / 'CHANGES.md').write_bytes(('\n'.join(parts)).encode('utf-8'))
    print(f'CHANGES.md: {total} hunks in {len(CHANGED)} files, {len(copies)} byte copies, 1 added, {len(DROPPED)} dropped')


if __name__ == '__main__':
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    main(Path(sys.argv[1]))
