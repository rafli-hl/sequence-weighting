"""Frozen fresh-draw partition of the dense-readout replication, N8 (N8-protocol-draft.md, section 4). Stdlib only; no framework, no
losses, no outcomes. Sealed with matched_registry.py and the seed policy before any seed of this study exists. Derived from N7's
matched_data.py, a byte copy here as n7_matched_data.py.

The 24 fresh groups n01-n24 come from the eligible WikiText-103 training articles (those the corpus manifest does not exclude), less:
- every article the few-epoch partition (N5: t00, d01-d10), the peak partition (N6: c01-c06) or the matched partition (N7: m01-m06)
  assigned to a group, each re-derived with its sealed function from its own registry's partition_seed and required to equal its pin;
- every remaining article whose full text equals that of an assigned article;
- every copy of any text that occurs more than once among what remains.
The articles of N1, N3 and N4, and of the first attempts of N1 and N3, are WikiText-2 articles, and the corpus manifest excludes every
article equal by title or text to a WikiText-2 article, so they cannot enter. S is synthetic and has no articles.
The fresh indices are sorted, shuffled with random.Random(partition_seed) (this registry's seed) and assigned whole, in that order, to
n01, ..., n24, each group until it holds at least N sequences (text_data._fill); each group uses its first N sequences in assignment
order. Depends only on per-article sequence counts, text hashes and the four partition seeds (outcome-blind).
"""
import hashlib, random
import n7_matched_data
import peak_data
import text_data

GROUPS = tuple(f'n{i:02d}' for i in range(1, 25))
N_TRAIN = 16384
PEAK_PARTITION_SHA256 = '3ba24bff0c38612d7d1751505edf8c5e02e9a98e46ff24165195c1199571ab85'   # the encoded c01-c06 partition (N6)
N7_PARTITION_SHA256 = 'b7eb3d3ba200b86046c6d731d2f0200ff657b6c2aaeebd43423cd4aec530e33b'     # the encoded m01-m06 partition (N7)
encoded = peak_data.encoded
fresh_pool = peak_data.fresh_pool                                                             # the same three rules, on the larger assigned set


def assigned_articles(manifest, fewepoch_partition_seed, peak_partition_seed, n7_partition_seed, fewepoch_pin=None, peak_pin=None, n7_pin=None):
    """The articles of N5's, N6's and N7's partitions, re-derived with the sealed functions (N7's: n7_matched_data, a byte copy).
    Raises ValueError if any differs from its pin."""
    earlier = n7_matched_data.assigned_articles(manifest, fewepoch_partition_seed, peak_partition_seed, fewepoch_pin, peak_pin)
    n7 = n7_matched_data.partition(manifest, earlier, n7_partition_seed)
    if hashlib.sha256(n7_matched_data.encoded(n7)).hexdigest() != (n7_pin or N7_PARTITION_SHA256): raise ValueError('The N7 partition differs from its pin')
    return earlier | {a for g in n7['groups'].values() for a in g['articles']}


def partition(manifest, assigned, partition_seed):
    """n01-n24 from the fresh articles. Raises ValueError if they cannot fill every group at N."""
    pool = fresh_pool(manifest, assigned); rows = {a['index']: a for a in manifest['splits']['train']['articles']}
    counts = {i: rows[i]['sequences'] for i in pool['articles']}; first = {i: rows[i]['first'] for i in pool['articles']}
    order = list(pool['articles']); random.Random(partition_seed).shuffle(order)
    filled = text_data._fill(order, counts, N_TRAIN, len(GROUPS))
    if filled is None: raise ValueError(f'The fresh articles cannot fill {len(GROUPS)} groups at N')
    groups = {name: dict(articles=arts_in, sequences=[first[a] + k for a in arts_in for k in range(counts[a])][:N_TRAIN]) for name, arts_in in zip(GROUPS, filled)}
    return dict(n=N_TRAIN, groups=groups, pool={k: v for k, v in pool.items() if k != 'articles'}, left_over_articles=len(order) - sum(len(g['articles']) for g in groups.values()))


def disjoint(part, manifest, assigned):
    """By article and by full text: the groups are disjoint, hold exactly N distinct sequences inside their own articles, and
    touch no excluded article, no assigned article and no text of an assigned article. Raises PermissionError."""
    if sorted(part['groups']) != sorted(GROUPS) or part['n'] != N_TRAIN: raise PermissionError('Partition groups or size differ from the plan')
    rows = {a['index']: a for a in manifest['splits']['train']['articles']}; arts = [a for g in GROUPS for a in part['groups'][g]['articles']]
    if len(arts) != len(set(arts)): raise PermissionError('Groups share an article')
    if set(arts) & set(manifest['exclusions']['articles']): raise PermissionError('A group uses an excluded article')
    if set(arts) & set(assigned): raise PermissionError('A group uses an assigned article')
    texts = [rows[a]['text_sha256'] for a in arts]
    if len(texts) != len(set(texts)): raise PermissionError('Groups share a full text')
    if set(texts) & {rows[a]['text_sha256'] for a in assigned}: raise PermissionError('A group uses the text of an assigned article')
    for g in GROUPS:
        seqs = part['groups'][g]['sequences']
        if len(seqs) != N_TRAIN or len(set(seqs)) != N_TRAIN: raise PermissionError('Group size: ' + g)
        own = {rows[a]['first'] + k for a in part['groups'][g]['articles'] for k in range(rows[a]['sequences'])}
        if not set(seqs) <= own: raise PermissionError("A sequence lies outside its group's articles: " + g)
    return dict(articles=len(arts), groups=len(GROUPS), n=N_TRAIN)
