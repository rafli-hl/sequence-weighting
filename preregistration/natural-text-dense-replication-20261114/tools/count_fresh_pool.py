"""Count N8's fresh articles and sequences (the brief's step 3; native Python 3.12, -I -B; stdlib only). Run by the owner, because it reads
the sealed corpus manifest, which lies in the closed record's work/runs/; it opens nothing else there.

  python -I -B count_fresh_pool.py <CORPUS_MANIFEST.json> <NEW_OUT_DIR>       -> <NEW_OUT_DIR>/FRESH_POOL_COUNT.json, and a summary on stdout

The manifest must equal its pin (fewepoch_plan.CORPUS_MANIFEST_SHA256), be the approved acquisition's, and pass the sealed checks
(wt103_corpus.validate_manifest). N5's, N6's and N7's partitions are re-derived with their sealed functions from their registries'
partition seeds (the registries under the closed record's reports/), each against its pin. Then:
- N7's own fresh pool is recounted and compared with the counts N7's registry recorded: a check that the manifest and the code are those
  N7 used;
- N8's fresh pool (matched_data.fresh_pool, less the N5, N6 and N7 articles and their text copies) is counted: articles, sequences, and
  what each rule removed;
- feasibility without a partition: whatever the shuffle, 24 draws of 16,384 fit if the pool holds at least 24 x 16,384 + 24 x (its
  largest article - 1) sequences, because a group passes N by less than one article.
No seed of N8 is drawn or used, and no partition of N8 is made: that needs the registry (step 5).
"""
import hashlib, json, sys
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDY / 'source'))
import fewepoch_plan as fp, matched_data as md, matched_plan as mp, matched_registry as mr, n7_matched_data, wt103_corpus as wc

sha = lambda b: hashlib.sha256(b).hexdigest()
POOL_KEYS = ('eligible_articles', 'assigned_articles', 'unused_articles', 'removed_text_duplicates_of_assigned', 'removed_repeats_inside_the_pool', 'sets_of_repeats_inside_the_pool', 'fresh_articles', 'fresh_sequences')


def pool_record(pool):
    return dict({k: pool[k] for k in POOL_KEYS}, articles_sha256=sha(md.encoded(pool['articles'])))


def count(manifest, seeds, pins, n7_recorded):
    """seeds: the partition seeds of N5, N6 and N7 (few, peak, n7); pins: their partitions' pins; n7_recorded: N7's registry's fresh_pool."""
    earlier = n7_matched_data.assigned_articles(manifest, seeds['few'], seeds['peak'], pins['few'], pins['peak'])
    n7_pool = n7_matched_data.fresh_pool(manifest, earlier)
    assigned = md.assigned_articles(manifest, seeds['few'], seeds['peak'], seeds['n7'], pins['few'], pins['peak'], pins['n7'])
    n7_articles = assigned - earlier; pool = md.fresh_pool(manifest, assigned)
    rows = {a['index']: a for a in manifest['splits']['train']['articles']}; lengths = [rows[i]['sequences'] for i in pool['articles']]
    largest = max(lengths) if lengths else 0; need = len(md.GROUPS) * md.N_TRAIN; bound = need + len(md.GROUPS) * max(largest - 1, 0)
    n7_recount = pool_record(n7_pool)
    return dict(n8_fresh_pool=pool_record(pool), draws=len(md.GROUPS), n_train=md.N_TRAIN, sequences_needed=need, largest_fresh_article_sequences=largest,
                mean_sequences_per_fresh_article=pool['fresh_sequences'] / len(lengths) if lengths else None, sequences_needed_whatever_the_shuffle=bound,
                fits_whatever_the_shuffle=pool['fresh_sequences'] >= bound, assigned_articles=dict(n5_and_n6=len(earlier), n7=len(n7_articles), all=len(assigned)),
                n7_pool_recount=n7_recount, n7_pool_matches_its_registry=n7_recount == n7_recorded,
                n8_pool_is_n7_pool_less_n7_articles=set(pool['articles']) == set(n7_pool['articles']) - n7_articles)


def main(manifest_path, out_dir):
    out = Path(out_dir)
    if out.exists(): raise SystemExit('The output folder exists; nothing was counted')
    raw = Path(manifest_path).read_bytes()
    if sha(raw) != fp.CORPUS_MANIFEST_SHA256: raise SystemExit('The corpus manifest differs from its pin; nothing was counted')
    manifest = json.loads(raw)
    if manifest.get('source_subject_sha256') != fp.ACQUISITION_SUBJECT or manifest.get('fixture') is not False: raise SystemExit('Not the approved acquisition\'s manifest; nothing was counted')
    wc.validate_manifest(manifest, {f: sha((STUDY / 'source' / f).read_bytes()) for f in wc.CODE_FILES})
    regs = {}
    for key, d, pin in (('few', fp.REGISTRY['directory'], fp.REGISTRY['registry_sha256']), ('peak', mp.PEAK_REGISTRY['directory'], mp.PEAK_REGISTRY['registry_sha256']), ('n7', mp.N7_REGISTRY['directory'], mp.N7_REGISTRY['registry_sha256'])):
        r = (mr.ROOT / d / 'REGISTRY.json').read_bytes()
        if sha(r) != pin: raise SystemExit(f'The {key} registry differs from its pin; nothing was counted')
        regs[key] = json.loads(r)
    seeds = {k: v['partition_seed'] for k, v in regs.items()}; pins = dict(few=fp.PARTITION_SHA256, peak=md.PEAK_PARTITION_SHA256, n7=md.N7_PARTITION_SHA256)
    result = dict(schema=1, kind='N8 fresh-pool count (step 3)', corpus_manifest_sha256=sha(raw), registries_sha256={k: sha((mr.ROOT / d / 'REGISTRY.json').read_bytes()) for k, d in
                  (('few', fp.REGISTRY['directory']), ('peak', mp.PEAK_REGISTRY['directory']), ('n7', mp.N7_REGISTRY['directory']))}, partition_pins=pins,
                  source_sha256={f: sha((STUDY / 'source' / f).read_bytes()) for f in ('matched_data.py', 'n7_matched_data.py', 'peak_data.py', 'fewepoch_data.py', 'text_data.py', 'wt103_corpus.py')},
                  tool_sha256=sha(Path(__file__).read_bytes()), **count(manifest, seeds, pins, regs['n7']['fresh_pool']))
    out.mkdir(parents=False); raw_out = (json.dumps(result, sort_keys=True, indent=1) + '\n').encode('utf-8'); (out / 'FRESH_POOL_COUNT.json').write_bytes(raw_out)
    p = result['n8_fresh_pool']
    print(f"N8 fresh pool: {p['fresh_articles']:,} articles, {p['fresh_sequences']:,} sequences (assigned {p['assigned_articles']:,}; removed {p['removed_text_duplicates_of_assigned']} text copies of assigned articles "
          f"and {p['removed_repeats_inside_the_pool']} repeats inside the pool)")
    print(f"Needed: {result['sequences_needed']:,}; whatever the shuffle: {result['sequences_needed_whatever_the_shuffle']:,} (largest fresh article {result['largest_fresh_article_sequences']} sequences). "
          f"Fits: {result['fits_whatever_the_shuffle']}")
    print(f"N7's pool recounted and equal to its registry: {result['n7_pool_matches_its_registry']}; N8's pool is N7's less N7's articles: {result['n8_pool_is_n7_pool_less_n7_articles']}")
    print(f"Written {out / 'FRESH_POOL_COUNT.json'} sha256 {sha(raw_out)}")
    return 0 if result['fits_whatever_the_shuffle'] and result['n7_pool_matches_its_registry'] else 1


if __name__ == '__main__':
    if len(sys.argv) != 3: raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
