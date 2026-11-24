"""POST HOC audit script (auditor B). Reads only published files of the clone at v2.1; imports nothing from the repository.
Internal consistency of N8's HASHES.json, seed registry, partition, pilot log, seals and pins, re-derived with my own code.
"""
import hashlib, json, re, sys
from pathlib import Path
REPO = Path(sys.argv[1]); N8 = REPO / 'preregistration/natural-text-dense-replication-20261114'
N7 = REPO / 'preregistration/natural-text-matched-confirmation-20261104'; N6 = REPO / 'preregistration/natural-text-peak-confirmation-20261103'
REG = N8 / 'registry/n8-seed-registry'
sha = lambda b: hashlib.sha256(b).hexdigest()
J = lambda p: json.loads(Path(p).read_bytes())
ok_all = []
def check(name, ok, detail=''):
    ok_all.append(bool(ok)); print(('PASS  ' if ok else 'FAIL  ') + name + (f'  [{detail}]' if detail != '' else ''))

# ---------------------------------------------------------------- 1. HASHES.json against the files
h = J(N8 / 'HASHES.json')
single = dict(protocol_sha256='N8-protocol-draft.md', changes_sha256='CHANGES.md', sealed_source_subject_sha256='source/SOURCE_SUBJECT.json', pending_seal_before_the_draw_sha256='seal/pre-pin/SOURCE_SUBJECT.json',
              pilot_source_subject_sha256='seal/pilot/SOURCE_SUBJECT.json', seed_policy_sha256='registry/n8-seed-registry/SEED_REGISTRY_POLICY.md', seed_registry_sha256='registry/n8-seed-registry/REGISTRY.json',
              exclusions_sha256='registry/n8-seed-registry/EXCLUSIONS.json', draw_sha256='registry/n8-seed-registry/DRAW.json', draw_claim_sha256='registry/n8-seed-registry/DRAW_CLAIM.json',
              partition_sha256='registry/n8-seed-registry/PARTITION.json', registry_and_partition_check_sha256='registry/n8-seed-registry/REGISTRY_AND_PARTITION_CHECK.json',
              disclosure_figures_sha256='registry/n8-seed-registry/DISCLOSURE_FIGURES.md', seed_draw_receipt_sha256='registry/n8-seed-registry/SEED_DRAW_RECEIPT.json',
              fresh_pool_count_sha256='data-count/FRESH_POOL_COUNT.json', pilot_log_sha256='pilot/PILOT_LOG.json', pilot_command_sha256='PILOT_COMMAND.txt')
bad = [k for k, p in single.items() if sha((N8 / p).read_bytes()) != h[k]]
check('HASHES.json: 17 single-file hashes equal the published files', not bad, bad)
groups = ('pre_pin_copies', 'analysis', 'tools', 'source_tests', 'tools_tests', 'retired_tests')
diff, absent = [], []
for g in groups:
    for p, v in h[g].items():
        f = N8 / p
        if not f.is_file(): absent.append(p)
        elif sha(f.read_bytes()) != v: diff.append((p, sha(f.read_bytes())[:8]))
check('HASHES.json: grouped file hashes equal the published files, except those listed', diff == [('tools/build_n8_activation.py', 'c31fd4aa')] and absent == ['tests-retired/test_draw_command.py'], f'differ: {diff}; named but not published: {absent}')
unpub = [k for k in h if k.endswith('_sha256') and k not in single]
print('      HASHES.json keys ending _sha256 with no published file checked above:', unpub)
tracked = sorted(p.relative_to(N8).as_posix() for p in N8.rglob('*') if p.is_file())
named = set(single.values()) | {p for g in groups for p in h[g]}
subject_files = {'source/' + f['path'] for f in J(N8 / 'source/SOURCE_SUBJECT.json')['files']}
unbound = [p for p in tracked if p not in named and p not in subject_files]
print('      published files bound neither by HASHES.json nor by SOURCE_SUBJECT.json:', unbound)

# ---------------------------------------------------------------- 2. the seed draw, re-derived from the policy text
draw = J(REG / 'DRAW.json'); raw = bytes.fromhex(draw['entropy_hex']); ex = J(REG / 'EXCLUSIONS.json'); reg = J(REG / 'REGISTRY.json')
check('DRAW.json: 1,024 bytes of entropy', len(raw) == 1024 == draw['bytes'])
cands = [int.from_bytes(raw[4 * i:4 * i + 4], 'little') for i in range(256)]
excluded = sorted(set(ex['values'])); accepted = []
for c in cands:
    if len(accepted) == 98: break
    if all(abs(c - e) > 2048 for e in excluded) and all(abs(c - a) > 2048 for a in accepted): accepted.append(c)
roles = [('partition', 'partition_seed')] + [(f'n{i:02d}', r) for i in range(1, 25) for r in ('init_seed', 'weight_seed', 'pretrain_order_seed', 'adapt_order_seed')] + [('benchmark', 'benchmark_seed')]
mine = {}
for (slot, role), v in zip(roles, accepted): mine.setdefault(slot, {})[role] = v
theirs = {'partition': {'partition_seed': reg['partition_seed']}, 'benchmark': {'benchmark_seed': reg['benchmark']['benchmark_seed']}}
for row in reg['groups']: theirs[row['group']] = {k: v for k, v in row.items() if k != 'group'}
check('my re-derivation of the 98 role values from DRAW.json and EXCLUSIONS.json equals REGISTRY.json', len(accepted) == 98 and mine == theirs, f'candidates used up to index {cands.index(accepted[-1])}; rejected before that: {cands.index(accepted[-1]) + 1 - 98}')
vals = [v for s in theirs.values() for v in s.values()]
near_ex = min(min(abs(v - e) for e in excluded) for v in vals); near_other = min(abs(a - b) for i, a in enumerate(vals) for b in vals[i + 1:])
check('98 distinct values, each more than 2,048 from every exclusion and from each other', len(set(vals)) == 98 and near_ex > 2048 and near_other > 2048, f'nearest exclusion {near_ex}, nearest other role {near_other}; the check record says 37913 and 112876')
check('registry decisions list equals my accept/reject sequence', [d['value'] for d in reg['decisions'] if d['accepted']] == accepted and len(reg['decisions']) == 256)
check('registry binds its own draw, exclusions, policy and partition', (reg['draw_sha256'], reg['exclusions_sha256'], reg['policy_sha256'], reg['partition_sha256']) == (sha((REG / 'DRAW.json').read_bytes()), sha((REG / 'EXCLUSIONS.json').read_bytes()), sha((REG / 'SEED_REGISTRY_POLICY.md').read_bytes()), sha((REG / 'PARTITION.json').read_bytes())))
check('exclusions: 4,370 values, sorted, unique; provenance union_values agrees', len(ex['values']) == 4370 == ex['provenance']['union_values'] and ex['values'] == excluded)
pilot = J(N8 / 'pilot/PILOT_LOG.json')
check("the pilot's five seeds are all in EXCLUSIONS.json", all(v in set(excluded) for v in pilot['seeds'].values()) and len(pilot['seeds']) == 5, pilot['seeds'])
def text_values(r): return {r['partition_seed'], r['benchmark']['benchmark_seed']} | {v for row in r['groups'] for k, v in row.items() if k != 'group'}
def collect(value, under, out):
    # every integer 0..2^32-1 under a key whose name contains seed, stream, schedule or corpus (the policy's census rule)
    if isinstance(value, dict):
        for k, v in value.items(): collect(v, under or any(x in str(k).lower() for x in ('seed', 'stream', 'schedule', 'corpus')), out)
    elif isinstance(value, list):
        for v in value: collect(v, under, out)
    elif under and type(value) is int and 0 <= value < 2 ** 32: out.add(value)
exset = set(excluded)
for name, folder in (('N7', N7 / 'seed-registry'), ('N6', N6 / 'seed-registry')) + tuple((d.name, d) for d in sorted((REPO / 'reports').glob('*seed-registry*')) if (d / 'REGISTRY.json').is_file()):
    r = J(folder / 'REGISTRY.json'); tv = text_values(r) if 'groups' in r and 'partition_seed' in r else set(); cv = set(); collect(r, False, cv)
    e = set(J(folder / 'EXCLUSIONS.json')['values']) if (folder / 'EXCLUSIONS.json').is_file() else None
    check(f"{name}: every role value ({len(tv)}), every census-rule value of its REGISTRY.json ({len(cv)}) and its exclusion list ({'not published' if e is None else len(e)}) are in N8's exclusions",
          tv <= exset and cv <= exset and (e is None or e <= exset), 'registry sha ' + sha((folder / 'REGISTRY.json').read_bytes())[:8] + f'; nearest N8 role value to one of its values: {min(abs(a - b) for a in vals for b in (cv | tv))}')
check("N8's registry pins N7's registry and partition as published", reg['n7_registry_sha256'] == sha((N7 / 'seed-registry/REGISTRY.json').read_bytes()) and reg['n7_partition_sha256'] == sha((N7 / 'seed-registry/PARTITION.json').read_bytes()))
claim = J(REG / 'DRAW_CLAIM.json'); src = {f['path']: f['sha256'] for f in J(N8 / 'source/SOURCE_SUBJECT.json')['files']}
check('claim and registry: registry-source hashes equal the sealed source files (13 files)', claim['registry_source_sha256'] == reg['registry_source_sha256'] and all(src[k] == v for k, v in claim['registry_source_sha256'].items()) and len(claim['registry_source_sha256']) == 13)
rec = J(REG / 'SEED_DRAW_RECEIPT.json')
check('receipt: registry, partition, draw script and disclosure script hashes', (rec['registry_sha256'], rec['partition_sha256'], rec['draw_script_sha256'], rec['disclosure_script_sha256']) == (h['seed_registry_sha256'], h['partition_sha256'], h['tools']['tools/n8_seed_draw.py'], h['tools']['tools/n8_post_draw.py']))
check('receipt: the draw ran on the pending seal kept in seal/pre-pin', rec['source_subject_sha256'] == h['pending_seal_before_the_draw_sha256'] == sha((N8 / 'seal/pre-pin/SOURCE_SUBJECT.json').read_bytes()), rec['finished_local'])
chk = J(REG / 'REGISTRY_AND_PARTITION_CHECK.json')
check('post-draw check record: 16 checks, all ok', len(chk['checks']) == 16 and all(c['ok'] for c in chk['checks'].values()) and chk['all_pass'] is True)

# ---------------------------------------------------------------- 3. the partition
part = J(REG / 'PARTITION.json'); g = part['groups']
check('partition: 24 groups n01-n24 in order, n = 16,384', list(g) == [f'n{i:02d}' for i in range(1, 25)] and part['n'] == 16384)
check('each group: exactly 16,384 distinct sequences', all(len(v['sequences']) == 16384 == len(set(v['sequences'])) for v in g.values()))
allseq = [s for v in g.values() for s in v['sequences']]; allart = [a for v in g.values() for a in v['articles']]
check('groups are disjoint by sequence (393,216 distinct) and by article', len(set(allseq)) == 393216 == len(allseq) and len(set(allart)) == len(allart), f'{len(allart)} articles in all; left over {part["left_over_articles"]}; sum {len(allart) + part["left_over_articles"]}')
print('      partition pool record:', part['pool'])
check('articles used + left over = 14,039 fresh articles', len(allart) + part['left_over_articles'] == 14039 == reg['fresh_pool']['fresh_articles'] == part['pool'].get('fresh_articles', 14039))
for name, folder in (('N7', N7), ('N6', N6)):
    pf = folder / 'seed-registry/PARTITION.json'
    if not pf.is_file(): print(f'      {name}: no PARTITION.json published; not checked'); continue
    p7 = J(pf); a7 = {a for v in p7['groups'].values() for a in v['articles']}; s7 = {s for v in p7['groups'].values() for s in v['sequences']}
    check(f"no N8 article or sequence is in {name}'s published partition", not (set(allart) & a7) and not (set(allseq) & s7), f'{name}: {len(a7)} articles, {len(s7)} sequences, left over {p7.get("left_over_articles")}')
p7 = J(N7 / 'seed-registry/PARTITION.json')
check("N7's left-over articles (14,039) equal N8's fresh pool size", p7['left_over_articles'] == 14039)
fig = (REG / 'DISCLOSURE_FIGURES.md').read_text(encoding='utf-8'); rows = re.findall(r'^\| (n\d\d) \| (\d+) \| ([\d,]+) \|', fig, flags=re.M)
check('DISCLOSURE_FIGURES.md: articles and sequences per draw equal the partition', len(rows) == 24 and all(len(g[d]['articles']) == int(a) and len(g[d]['sequences']) == int(s.replace(',', '')) for d, a, s in rows))
det = chk['checks']['24 draws of exactly N sequences']['detail']
check('check record: articles and sequences per draw equal the partition', all(det[d] == dict(articles=len(g[d]['articles']), sequences=len(g[d]['sequences'])) for d in g))
# sequences are consecutive runs inside articles: the last article of a group may be cut
cut = {d: len(v['sequences']) for d, v in g.items()}
runs = {}
for d, v in g.items():
    s = v['sequences']; breaks = 1 + sum(1 for a, b in zip(s, s[1:]) if b != a + 1); runs[d] = breaks
check('each group\'s sequences form at most as many consecutive runs as it has articles', all(runs[d] <= len(g[d]['articles']) for d in g), f'runs {min(runs.values())}-{max(runs.values())}')

# ---------------------------------------------------------------- 4. the fresh-pool count and the protocol's numbers
fc = J(N8 / 'data-count/FRESH_POOL_COUNT.json')
check('fresh pool: count file = registry record = 14,039 articles and 582,603 sequences', fc['n8_fresh_pool'] == reg['fresh_pool'] and fc['n8_fresh_pool']['fresh_articles'] == 14039 and fc['n8_fresh_pool']['fresh_sequences'] == 582603)
check('24 x 16,384 = 393,216; + 24 x (328 - 1) = 401,064 <= 582,603', 24 * 16384 == 393216 == fc['sequences_needed'] and 393216 + 24 * (fc['largest_fresh_article_sequences'] - 1) == 401064 == fc['sequences_needed_whatever_the_shuffle'] and fc['largest_fresh_article_sequences'] == 328 and 401064 <= 582603)
check('count: assigned 13,511 = 11,099 (N5, N6) + 2,412 (N7); N7 pool 16,451 - 2,412 = 14,039', fc['assigned_articles'] == dict(all=13511, n5_and_n6=11099, n7=2412) and 11099 + 2412 == 13511 and fc['n7_pool_recount']['fresh_articles'] - 2412 == 14039)
a7 = {a for v in p7['groups'].values() for a in v['articles']}
check("N7's published partition holds 2,412 articles in m01-m06", len(a7) == 2412, len(a7))
check('count tool hash and source hashes agree with HASHES.json and the sealed source', fc['tool_sha256'] == h['tools']['tools/count_fresh_pool.py'] and all(src[k] == v for k, v in fc['source_sha256'].items()))

# ---------------------------------------------------------------- 5. pins in the sealed source, the builder and the prose
plan = (N8 / 'source/matched_plan.py').read_text(encoding='utf-8'); regpy = (N8 / 'source/matched_registry.py').read_text(encoding='utf-8'); datapy = (N8 / 'source/matched_data.py').read_text(encoding='utf-8')
pin = lambda text, key: re.search(key + r"\s*=\s*'([0-9a-f]{64})'", text).group(1)
check('matched_plan.py pins: policy, registry, exclusions, draw, partition', (pin(plan, 'policy_sha256'), pin(plan, 'registry_sha256'), pin(plan, 'exclusions_sha256'), pin(plan, 'draw_sha256'), pin(plan, 'PARTITION_SHA256')) == (h['seed_policy_sha256'], h['seed_registry_sha256'], h['exclusions_sha256'], h['draw_sha256'], h['partition_sha256']))
check('matched_registry.py POLICY_SHA256 and N7_REGISTRY_SHA256; matched_data.py N7_PARTITION_SHA256', pin(regpy, 'POLICY_SHA256') == h['seed_policy_sha256'] and pin(regpy, 'N7_REGISTRY_SHA256') == sha((N7 / 'seed-registry/REGISTRY.json').read_bytes()) and pin(datapy, 'N7_PARTITION_SHA256') == h['n7_partition_sha256'] == sha((N7 / 'seed-registry/PARTITION.json').read_bytes()))
b = (N8 / 'tools/build_n8_activation.py').read_text(encoding='utf-8')
check('builder (v2.1): EXPECTED_SUBJECT, and PUBLIC_REGISTRATION subject and pilot-log hash', "EXPECTED_SUBJECT = '" + h['sealed_source_subject_sha256'] in b and "'source_subject_sha256': '" + h['sealed_source_subject_sha256'] in b and "'pilot_log_sha256': '" + h['pilot_log_sha256'] in b)
prose = {'N8-protocol-draft.md': (N8 / 'N8-protocol-draft.md').read_text(encoding='utf-8'), 'README.md': (N8 / 'README.md').read_text(encoding='utf-8'), 'source/README.md': (N8 / 'source/README.md').read_text(encoding='utf-8'), 'CHANGES.md': (N8 / 'CHANGES.md').read_text(encoding='utf-8')}
known = {v for v in h.values() if isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v)} | {v for g_ in groups for v in h[g_].values()} | set(src.values()) | {sha((N8 / 'tools/build_n8_activation.py').read_bytes()), sha((N7 / 'sealed-source/SOURCE_SUBJECT.json').read_bytes()), 'c6f98b26669f5d29f30c576b6d800c1fc82c98eb'}
known |= {f['sha256'] for f in J(N7 / 'sealed-source/SOURCE_SUBJECT.json')['files']}
for name, text in prose.items():
    if name == 'CHANGES.md': text = '\n'.join(l for l in text.split('\n') if not l.startswith(('+', '-', ' ')))
    pref = set(re.findall(r'`([0-9a-f]{8,64})(?:…)?`', text))
    unmatched = sorted(p for p in pref if not any(k.startswith(p) for k in known))
    print(f'      {name}: {len(pref)} hash prefixes quoted; not matching any hash I can compute from published files: {unmatched}')

# ---------------------------------------------------------------- 6. the seals: pilot subject -> pending seal -> sealed subject
def files(p): return {f['path']: f['sha256'] for f in J(p)['files']}
s_pilot, s_pre, s_final = files(N8 / 'seal/pilot/SOURCE_SUBJECT.json'), files(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json'), files(N8 / 'source/SOURCE_SUBJECT.json')
d1 = sorted(k for k in set(s_pilot) | set(s_pre) if s_pilot.get(k) != s_pre.get(k)); d2 = sorted(k for k in set(s_pre) | set(s_final) if s_pre.get(k) != s_final.get(k)); d3 = sorted(k for k in set(s_pilot) | set(s_final) if s_pilot.get(k) != s_final.get(k))
print('      files whose hash differs, pilot subject -> pending seal :', d1)
print('      files whose hash differs, pending seal -> sealed subject:', d2)
print('      files whose hash differs, pilot subject -> sealed subject:', d3)
check('pending seal -> sealed: exactly matched_plan.py, README.md and MATCHED_OWNER_RUN.ps1', d2 == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py'])
check('pilot subject -> sealed: exactly matched_plan.py, matched_registry.py, MATCHED_OWNER_RUN.ps1 and README.md (as the README says)', d3 == ['MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py', 'matched_registry.py'])
check('the pre-pin copies are the files the pending seal lists', all(sha((N8 / 'seal/pre-pin' / k).read_bytes()) == s_pre[k] for k in ('MATCHED_OWNER_RUN.ps1', 'README.md', 'matched_plan.py')))
check("the pilot log names the pilot subject and the pilot tool", pilot['source_subject_sha256'] == h['pilot_source_subject_sha256'] and pilot['pilot_sha256'] == h['tools']['tools/n8_pilot.py'])
import difflib
for k in ('matched_plan.py', 'README.md', 'MATCHED_OWNER_RUN.ps1'):
    a = (N8 / 'seal/pre-pin' / k).read_text(encoding='utf-8').splitlines(); c = (N8 / 'source' / k).read_text(encoding='utf-8').splitlines()
    print(f'      --- pre-pin -> sealed: {k}')
    for l in difflib.unified_diff(a, c, n=0, lineterm=''):
        if l.startswith(('+', '-')) and not l.startswith(('+++', '---')): print('        ' + l[:230])
for key in ('pins_pending', 'status', 'has_run', 'runtime_authorized'):
    print(f'      SOURCE_SUBJECT {key}: pilot {J(N8 / "seal/pilot/SOURCE_SUBJECT.json").get(key)!r}, pre-pin {J(N8 / "seal/pre-pin/SOURCE_SUBJECT.json").get(key)!r}, sealed {J(N8 / "source/SOURCE_SUBJECT.json").get(key)!r}')
print('      seed_registry_and_partition: pilot', J(N8 / 'seal/pilot/SOURCE_SUBJECT.json').get('seed_registry_and_partition'), '| pre-pin', J(N8 / 'seal/pre-pin/SOURCE_SUBJECT.json').get('seed_registry_and_partition'))

# ---------------------------------------------------------------- 7. the pilot log against the protocol's section 7
t = pilot['stage']['timing']; r3 = pilot['run_of_three_draws']; bm = pilot['benchmark']['architectures']
w512 = t['w512/lr1e-04']['total_seconds'] + t['w512/pretraining and E0']['total_seconds']; w768 = t['w768/lr1e-04']['total_seconds'] + t['w768/pretraining and E0']['total_seconds']
ev = sum(x['evaluation_seconds'] for x in t.values())
facts = [('benchmark 43.6 s (22.0 + 21.6)', round(r3['benchmark_seconds'], 1) == 43.6 and round(bm['512']['seconds'], 1) == 22.0 and round(bm['768']['seconds'], 1) == 21.6),
         ('per draw 2,528 s = 42.1 min, cap 3,097 s', round(r3['measured_stage_seconds']) == 2528 and round(r3['measured_stage_seconds'] / 60, 1) == 42.1 and r3['stage_cap_seconds'] == 3097),
         ('width 512: 867 s; 55 / 242 / 570', (round(w512), round(t['w512/pretraining and E0']['total_seconds']), round(t['w512/lr1e-04']['training_seconds']), round(t['w512/lr1e-04']['evaluation_seconds'])) == (867, 55, 242, 570)),
         ('width 768: 1,660 s; 101 / 462 / 1,097', (round(w768), round(t['w768/pretraining and E0']['total_seconds']), round(t['w768/lr1e-04']['training_seconds']), round(t['w768/lr1e-04']['evaluation_seconds'])) == (1660, 101, 462, 1097)),
         ('evaluation about two thirds', 0.62 < ev / pilot['stage']['seconds'] < 0.72),
         ('run of three: 7,629 s measured, 7,186 s projected; both under 21,600 s', round(r3['measured_run_seconds']) == 7629 and round(r3['projected_run_seconds']) == 7186 and abs(r3['measured_run_seconds'] - (r3['benchmark_seconds'] + 3 * r3['measured_stage_seconds'])) < 1e-6),
         ('PyTorch reserved at most 1.42 GiB', round(pilot['stage']['guard_peaks']['cuda_reserved'] / 2 ** 30, 2) == 1.42),
         ('eight runs: about 17 h on the worker clock', round(8 * r3['measured_run_seconds'] / 3600) == 17),
         ('28 readouts per record; 12 files; orders 524,288 bytes = 4 epochs x 16,384 x 8', pilot['stage']['checks']['records_have_28_readouts'] == {'w512': True, 'w768': True} and pilot['stage']['checks']['files']['ORDERS.i64'] == 4 * 16384 * 8),
         ('status PASS, real, no loss read, no p* fitted, run folder deleted', pilot['status'] == 'PASS' and pilot['fixture'] is False and pilot['loss_read'] is False and pilot['p_star_fitted'] is False and pilot['run_folder_deleted'] is True),
         ("the pilot's draw is N7's m01, none of it in N8's fresh pool", pilot['data']['draw'] == "N7's m01" and pilot['data']['articles_in_n8_fresh_pool'] == 0 and pilot['data']['sequences_in_n8_fresh_pool'] == 0 and pilot['data']['articles'] == len(p7['groups']['m01']['articles']))]
for name, ok in facts: check('pilot log vs protocol section 7: ' + name, ok)
print(f'      evaluation share {ev / pilot["stage"]["seconds"]:.3f}; device-wide GPU memory sampled by the guard, peak {pilot["stage"]["guard_peaks"]["device_used_sampled"]:,} bytes = {pilot["stage"]["guard_peaks"]["device_used_sampled"] / 2 ** 30:.3f} GiB; guard limit 2.5 GiB = {int(2.5 * 2 ** 30):,}; headroom {(int(2.5 * 2 ** 30) - pilot["stage"]["guard_peaks"]["device_used_sampled"]) / 2 ** 20:.0f} MiB')
print(f'      kept E0 states: (67,497,092 + 138,986,628) x 24 = {(67497092 + 138986628) * 24:,} bytes = {(67497092 + 138986628) * 24 / 2 ** 30:.2f} GiB (protocol: about 4.6 GiB)')
print(f'\n{sum(ok_all)} of {len(ok_all)} checks passed')
