"""POST HOC audit script (auditor B): descriptive check, on N7's PUBLISHED per-draw values (MATCHED.csv), of two statements in
N8-protocol-draft.md section 1: S3's leave-one-draw-out intervals, and the readouts at which N7's P1 read width 768."""
import csv, math, statistics, sys
T = {4: 2.7764451051977987, 5: 2.5705818366147395}
rows = list(csv.DictReader(open(sys.argv[1] + '/reports/natural-text-matched-analysis-20261105-01/MATCHED.csv', encoding='utf-8')))
for name in ('S3', 'P1'):
    v = {r['draw']: float(r['value']) for r in rows if r['statistic'] == name and r['status'] == 'READ'}
    m = statistics.fmean(v.values()); sd = statistics.stdev(v.values()); h = T[5] * sd / math.sqrt(6)
    print(f'{name}: all six: {m:+.6f} [{m - h:+.6f}, {m + h:+.6f}]')
    for d in v:
        w = [x for k, x in v.items() if k != d]; m = statistics.fmean(w); h = T[4] * statistics.stdev(w) / math.sqrt(5)
        print(f'   without {d}: {m:+.6f} [{m - h:+.6f}, {m + h:+.6f}]  includes 0: {m - h <= 0 <= m + h}')
print('P1 read_at_readout (epochs):', [round(float(r['read_at_readout']), 3) for r in rows if r['statistic'] == 'P1'], '-> N8 path covers epochs 2.0 to 3.5')
