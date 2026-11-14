"""Post-draw checks and disclosure figures of N8's seed draw (N8-protocol-draft.md, section 4; the brief's step 5). Native Python 3.12,
-I -B, NumPy. Run by n8_seed_draw.py. Derived from N7's post_draw_disclosure.py. It reads the corpus manifest, by its exact path, and
nothing else under work/runs/. Outcome-blind: article counts, text and title hashes, and weights from seeds. Writes only
REGISTRY_AND_PARTITION_CHECK.json and DISCLOSURE_FIGURES.md in the registry folder.

Registry: its files against each other; validate() re-derives it from its own bytes under the pins; the claim's approval id, policy,
manifest and source hashes; 98 values clear of every exclusion and of each other, with every N5, N6 and N7 value and the pilot's five
seeds among the exclusions; the census of the study folder read in full.
Partition: re-derived with the sealed matched_data.partition, and with an independent implementation written here from the frozen
policy's words, against the draw's own PARTITION.json. For the independent one, N5's and N6's articles come from their sealed partition
functions, as in N7's check, and N7's from N7's own PARTITION.json. The fresh pool is compared with the owner's count of 13 November and
with the articles N7's draw left unused. Disjointness by the sealed matched_data.disjoint and by separate counts.
Disclosure figures, on the real n01-n24: articles and sequences per draw; identical full text; articles sharing a title with an assigned
article or across draws; tied weights, by the stdlib draw and IEEE cast.

Not measured: exact token sequences and 64-token runs. They would read the corpus's split files, and this step may open only the manifest.
"""
import hashlib, json, math, random, sys, time
sys.dont_write_bytecode = True
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent; STUDY = HERE.parent; SRC = STUDY / 'source'
for p in (str(SRC / 'vendor'), str(SRC)):
    if p not in sys.path: sys.path.insert(0, p)
import fewepoch_plan as fp, fewepoch_data as fd, peak_data, matched_plan as mp, matched_data as md, matched_registry as mr
N7_CHECK = mr.ROOT / mr.N7_DIRECTORY / 'REGISTRY_AND_PARTITION_CHECK.json'      # what N7's own draw left unused
N7_PARTITION = mr.ROOT / mr.N7_DIRECTORY / 'PARTITION.json'
COUNT = STUDY / 'data-count/FRESH_POOL_COUNT.json'
PILOT_LOG = STUDY / 'pilot/PILOT_LOG.json'
sha = lambda b: hashlib.sha256(b).hexdigest()


def draw_weights(seed, n):
    rng = random.Random(1000 + seed); lo, hi = math.log(.01), math.log(10); return np.array([math.exp(rng.uniform(lo, hi)) for _ in range(n)], dtype=np.float32)


def tied(a): return int(a.size - np.unique(a).size)


def run(reg_dir, manifest_path, few_pin=None, peak_pin=None, n7_pin=None, manifest_sha256=None, fixture=False, expected_fresh=None, n7_partition=N7_PARTITION, count=COUNT, pilot_log=PILOT_LOG, study=None, out=print):
    """The keyword arguments other than out are for the native tests; n8_seed_draw.py passes none of them in a real draw."""
    t0 = time.time(); reg_dir = Path(reg_dir); checks = {}; N = md.N_TRAIN; study = Path(study or mr.STUDY)
    few_pin = few_pin or fp.PARTITION_SHA256; peak_pin = peak_pin or md.PEAK_PARTITION_SHA256; n7_pin = n7_pin or md.N7_PARTITION_SHA256; manifest_sha256 = manifest_sha256 or fp.CORPUS_MANIFEST_SHA256
    def check(name, ok, detail=None):
        checks[name] = dict(ok=bool(ok)) if detail is None else dict(ok=bool(ok), detail=detail); out(('PASS ' if ok else 'FAIL ') + name + ('' if detail is None else f' {detail}'))
    if expected_fresh is None and not fixture: expected_fresh = json.loads(N7_CHECK.read_bytes())['left_over_articles']
    files = {n: (reg_dir / n).read_bytes() for n in ('REGISTRY.json', 'EXCLUSIONS.json', 'DRAW.json', 'DRAW_CLAIM.json', 'PARTITION.json', 'SEED_REGISTRY_POLICY.md')}
    reg = json.loads(files['REGISTRY.json']); claim = json.loads(files['DRAW_CLAIM.json']); man_raw = Path(manifest_path).read_bytes(); man = json.loads(man_raw)
    regs_raw = {k: (mr.ROOT / d / 'REGISTRY.json').read_bytes() for k, d in (('few', fp.REGISTRY['directory']), ('peak', mp.PEAK_REGISTRY['directory']), ('n7', mp.N7_REGISTRY['directory']))}
    few, peak, n7 = (json.loads(regs_raw[k]) for k in ('few', 'peak', 'n7'))
    # ---- the registry
    check('no REGISTRY_STOPPED.json', not (reg_dir / 'REGISTRY_STOPPED.json').exists())
    mr.validate(reg, files['EXCLUSIONS.json'], files['DRAW.json'], manifest_sha256, few_pin, peak_pin, n7_pin); check('validate() re-derives the registry from its own bytes, under the pins', True)
    check('registry: FROZEN_DRAWN, the frozen policy, the manifest, and the three earlier registries and partitions',
          reg['status'] == 'FROZEN_DRAWN' and reg['fixture'] is bool(fixture) and reg['policy_sha256'] == mr.POLICY_SHA256 == mp.REGISTRY['policy_sha256'] == sha(files['SEED_REGISTRY_POLICY.md'])
          and reg['corpus_manifest_sha256'] == manifest_sha256 == sha(man_raw) and reg['fewepoch_registry_sha256'] == fp.REGISTRY['registry_sha256'] == sha(regs_raw['few'])
          and reg['peak_registry_sha256'] == mr.PEAK_REGISTRY_SHA256 == sha(regs_raw['peak']) and reg['n7_registry_sha256'] == mr.N7_REGISTRY_SHA256 == sha(regs_raw['n7'])
          and reg['fewepoch_partition_sha256'] == few_pin and reg['peak_partition_sha256'] == peak_pin and reg['n7_partition_sha256'] == n7_pin)
    check('claim: this approval, the same policy and manifest', claim['status'] == 'CLAIMED_BEFORE_DRAW' and claim['fixture'] is bool(fixture) and claim['approval_id'] == reg['approval_id']
          and claim['policy_sha256'] == reg['policy_sha256'] and claim['corpus_manifest_sha256'] == reg['corpus_manifest_sha256'], reg['approval_id'])
    check('every registry-source hash in the claim and the registry equals the source', claim['registry_source_sha256'] == reg['registry_source_sha256'] == mr.source_hashes())
    values = [reg['partition_seed']] + [r[k] for r in reg['groups'] for k in mr.ROLES] + [reg['benchmark']['benchmark_seed']]; ex = json.loads(files['EXCLUSIONS.json']); prov = ex['provenance']
    exs = np.array(sorted(ex['values']), dtype=np.int64); v = np.array(sorted(values), dtype=np.int64); i = np.searchsorted(exs, v)
    near = int(min(min(abs(exs[min(j, len(exs) - 1)] - x), abs(exs[max(j - 1, 0)] - x)) for j, x in zip(i, v)))
    earlier = set(mr.text_registry_values(few)) | set(mr.text_registry_values(peak)) | set(mr.text_registry_values(n7)); pilot_seeds = set(json.loads(Path(pilot_log).read_bytes())['seeds'].values())
    check('98 distinct values, each more than 2,048 from every exclusion and each other; every N5, N6 and N7 value and the five pilot seeds excluded',
          len(values) == len(mr.ROLE_ORDER) == 98 == len(set(values)) and near > mr.NEIGHBORHOOD and int(np.diff(v).min()) > mr.NEIGHBORHOOD and earlier <= set(ex['values']) and len(pilot_seeds) == 5 and pilot_seeds <= set(ex['values']),
          dict(nearest_exclusion=near, nearest_other_role=int(np.diff(v).min()), exclusions=len(ex['values']), unreadable_in_the_closed_record=prov['unreadable_count'], census=prov['census_values']))
    sc = prov.get('study_census', {})
    check("the study folder's census: this folder, read in full", sc.get('root') == str(study) and sc.get('unreadable_count') == 0, dict(root=sc.get('root'), json_files_with_values=sc.get('json_files_with_values'), values=sc.get('values')))
    # ---- the partition, by the sealed rule and independently
    assigned = md.assigned_articles(man, few['partition_seed'], peak['partition_seed'], n7['partition_seed'], few_pin, peak_pin, n7_pin); part = md.partition(man, assigned, reg['partition_seed']); part_raw = md.encoded(part)
    check("the sealed rule re-derives the draw's own PARTITION.json, and the registry records its hash", part_raw == files['PARTITION.json'] and sha(part_raw) == reg['partition_sha256'], sha(part_raw))
    md.disjoint(part, man, assigned); check('matched_data.disjoint passes on the partition', True)
    rows = man['splits']['train']['articles']; by = {a['index']: a for a in rows}; excluded = set(man['exclusions']['articles'])
    few_part = fd.partition(man, few['partition_seed']); few_arts = {a for g in few_part['groups'].values() for a in g['articles']}
    peak_part = peak_data.partition(man, few_arts, peak['partition_seed']); peak_arts = {a for g in peak_part['groups'].values() for a in g['articles']}
    n7_raw = Path(n7_partition).read_bytes(); n7_part = json.loads(n7_raw); n7_arts = {a for g in n7_part['groups'].values() for a in g['articles']}; pilot_arts = set(n7_part['groups']['m01']['articles'])
    used = few_arts | peak_arts | n7_arts; used_text = {by[a]['text_sha256'] for a in used}; used_title = {by[a]['title_sha256'] for a in used}
    step = [a for a in rows if a['index'] not in excluded and a['index'] not in used and a['text_sha256'] not in used_text]; c = Counter(a['text_sha256'] for a in step)
    order = sorted(a['index'] for a in step if c[a['text_sha256']] == 1); fresh_n, fresh_seq, fresh_list = len(order), sum(by[a]['sequences'] for a in order), sha(md.encoded(order))
    random.Random(reg['partition_seed']).shuffle(order); mine, k = {}, 0
    for g in md.GROUPS:
        arts, have = [], 0
        while have < N: a = order[k]; k += 1; arts.append(a); have += by[a]['sequences']
        mine[g] = dict(articles=arts, sequences=[by[a]['first'] + q for a in arts for q in range(by[a]['sequences'])][:N])
    check("an independent implementation from the policy text gives the same draws, with N7's articles from N7's own PARTITION.json",
          sha(n7_raw) == n7_pin and all(mine[g]['articles'] == part['groups'][g]['articles'] and mine[g]['sequences'] == part['groups'][g]['sequences'] for g in md.GROUPS) and part['pool']['fresh_articles'] == fresh_n,
          dict(fresh_articles=fresh_n, n7_partition_sha256=sha(n7_raw)))
    if expected_fresh is not None: check("the fresh pool has the size N7's draw left unused", fresh_n == expected_fresh, dict(expected=expected_fresh, fresh_articles=fresh_n))
    counted = json.loads(Path(count).read_bytes())['n8_fresh_pool']; recorded = reg['fresh_pool']
    check("the fresh pool equals the owner's count of 13 November and the registry's record: articles, sequences and the list's hash",
          counted['fresh_articles'] == fresh_n == recorded['fresh_articles'] and counted['fresh_sequences'] == fresh_seq == recorded['fresh_sequences'] and counted['articles_sha256'] == fresh_list == recorded['articles_sha256'],
          dict(articles=fresh_n, sequences=fresh_seq))
    all_arts = [a for g in md.GROUPS for a in part['groups'][g]['articles']]; all_seq = [q for g in md.GROUPS for q in part['groups'][g]['sequences']]
    per_group = {g: dict(articles=len(part['groups'][g]['articles']), sequences=len(part['groups'][g]['sequences'])) for g in md.GROUPS}
    check('24 draws of exactly N sequences', len(per_group) == 24 and all(x['sequences'] == N for x in per_group.values()), per_group)
    check("no article of N5, N6 or N7 (the pilot's m01 among them), no text of theirs and no excluded article, counted separately",
          not set(all_arts) & used and not {by[a]['text_sha256'] for a in all_arts} & used_text and not set(all_arts) & excluded and not set(all_arts) & pilot_arts,
          dict(assigned_articles=len(used), n5=len(few_arts), n6=len(peak_arts), n7=len(n7_arts), pilot_m01=len(pilot_arts)))
    check('disjoint by article and by sequence, counted separately', len(all_arts) == len(set(all_arts)) and len(all_seq) == len(set(all_seq)), dict(articles=len(all_arts), sequences=len(all_seq)))
    # ---- disclosure
    texts = {g: [by[a]['text_sha256'] for a in part['groups'][g]['articles']] for g in md.GROUPS}; across = Counter(t for g in md.GROUPS for t in set(texts[g]))
    identical = dict(sets_across_fresh_groups=sum(1 for x in across.values() if x > 1), fresh_texts_equal_to_an_assigned_article=len(set(across) & used_text), repeated_inside_a_group=sum(len(t) - len(set(t)) for t in texts.values()))
    titles = {g: [by[a]['title_sha256'] for a in part['groups'][g]['articles']] for g in md.GROUPS}; title_across = Counter(t for g in md.GROUPS for t in set(titles[g]))
    title_figures = dict(sets_across_fresh_groups=sum(1 for x in title_across.values() if x > 1), fresh_articles_sharing_a_title_with_an_assigned_article=sum(by[a]['title_sha256'] in used_title for a in all_arts))
    seeds = {r['group']: r for r in reg['groups']}; ties = {}
    for g in md.GROUPS: w = draw_weights(seeds[g]['weight_seed'], N); ties[g] = dict(before_division=tied(w), after_division_numpy_mean=tied((w / w.mean()).astype(np.float32)))
    limit = N // 1024
    check('the tied values of every draw are within the limit of n / 1,024', all(max(x.values()) <= limit for x in ties.values()), dict(limit=limit, ties={g: x['after_division_numpy_mean'] for g, x in ties.items()}))
    rec = dict(schema=1, purpose='Post-draw checks and disclosure of the N8 seed draw (the brief, step 5). Outcome-blind; from the corpus manifest only.', fixture=bool(fixture), all_pass=all(x['ok'] for x in checks.values()), checks=checks,
               registry_sha256=sha(files['REGISTRY.json']), exclusions_sha256=sha(files['EXCLUSIONS.json']), draw_sha256=sha(files['DRAW.json']), partition_sha256=sha(part_raw), partition_bytes=len(part_raw),
               policy_sha256=sha(files['SEED_REGISTRY_POLICY.md']), corpus_manifest_sha256=sha(man_raw), registry_source_sha256=reg['registry_source_sha256'], approval_id=reg['approval_id'], pool=part['pool'],
               left_over_articles=part['left_over_articles'], per_group=per_group,
               disclosure=dict(N=N, identical_text=identical, titles=title_figures, tied_weights=dict(limit=limit, by_group=ties), token_level='not measured: it would read the corpus split files, and this step may open only the manifest'),
               seconds=round(time.time() - t0, 1))
    (reg_dir / 'REGISTRY_AND_PARTITION_CHECK.json').write_bytes((json.dumps(rec, indent=1) + '\n').encode('utf-8'))
    table = '\n'.join(f"| {g} | {per_group[g]['articles']} | {per_group[g]['sequences']:,} | {ties[g]['before_division']} / {ties[g]['after_division_numpy_mean']} |" for g in md.GROUPS)
    md_text = f"""# Dense-readout replication (N8): disclosure figures on the real draws

**Step:** the owner-run seed draw (the brief, step 5). Outcome-blind: from the corpus manifest and the seeds only. **Measured** on n01–n24 at N = {N:,}. Carried by hand into the results report.

| Draw | Articles | Sequences used | Tied weights, before / after division by numpy's mean (limit {limit}) |
|---|---|---|---|
{table}

## Identical full text

- **Sets across the fresh draws:** {identical['sets_across_fresh_groups']}.
- **Fresh texts equal to an assigned article's:** {identical['fresh_texts_equal_to_an_assigned_article']}.
- **Repeated inside a draw:** {identical['repeated_inside_a_group']}.

The rule removes these, so zero is what it should give.

## Titles, which the rule does not remove

- **Fresh articles sharing a title with an article of N5, N6 or N7, with a different text:** {title_figures['fresh_articles_sharing_a_title_with_an_assigned_article']}.
- **Titles shared across the fresh draws:** {title_figures['sets_across_fresh_groups']}.

## Not measured

**Exact token sequences and 64-token runs.** They would read the corpus's split files, and this step may open only the manifest. So how far token runs recur across n01–n24, N5, N6, N7, the validation set and the pool is not known here. For scale, N6's groups had 64-token runs recurring in another fresh group at a mean of 0.15%. That is N6's figure and not a measurement of these draws.

**Shared by design:** every draw shares the validation set, the pool and the tokenizer with each other and with the earlier natural-text studies.

**Tied weights:** from the stdlib draw and the IEEE cast, without Torch. The weights used are after division, by Torch's mean, so the counts from real Torch can differ by one or so.

**Limit.** Draws are treated as independent in every interval. These figures do not measure how far that is true.
"""
    (reg_dir / 'DISCLOSURE_FIGURES.md').write_bytes(md_text.encode('utf-8'))
    out(('All post-draw checks PASS' if rec['all_pass'] else 'SOME POST-DRAW CHECK FAILED') + f" in {rec['seconds']} s; written: REGISTRY_AND_PARTITION_CHECK.json, DISCLOSURE_FIGURES.md")
    return rec
