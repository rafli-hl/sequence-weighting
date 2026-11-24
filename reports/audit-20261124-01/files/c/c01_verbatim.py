"""POST HOC audit script (area C). Are the estimator pieces of n8_analysis.py verbatim copies of N7's sealed source?
Reads only the clone. Usage: python -I -B c01_verbatim.py <REPO>"""
import ast, hashlib, sys, difflib
from pathlib import Path
repo = Path(sys.argv[1])
N8 = repo / 'preregistration/natural-text-dense-replication-20261114'
N7 = repo / 'preregistration/natural-text-matched-confirmation-20261104/sealed-source'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def seg(path, name):
    src = path.read_text(encoding='utf-8')
    for f in ast.walk(ast.parse(src)):
        if isinstance(f, ast.FunctionDef) and f.name == name: return ast.get_source_segment(src, f)
    raise KeyError(name)
def dump(path, name):
    src = path.read_text(encoding='utf-8')
    for f in ast.walk(ast.parse(src)):
        if isinstance(f, ast.FunctionDef) and f.name == name: return ast.dump(f)
mine = N8 / 'analysis/n8_analysis.py'
print('n8_analysis.py sha256', sha(mine))
for rel, name in (('vendor/core.py', 'exponent'), ('text_analysis.py', 'exponent_upper'), ('text_analysis.py', 'objective_at'),
                  ('matched_analysis.py', 'read_along'), ('fewepoch_analysis.py', '_betacf'), ('fewepoch_analysis.py', 'betai'),
                  ('fewepoch_analysis.py', 'p_two_sided'), ('matched_analysis.py', 'side'), ('matched_analysis.py', 'sign_test'),
                  ('matched_analysis.py', 'draw_row'), ('matched_analysis.py', 'leave_one_out'), ('matched_analysis.py', 'fits_used')):
    a, b = seg(N7 / rel, name), seg(mine, name)
    same_text = a == b; same_ast = dump(N7 / rel, name) == dump(mine, name)
    print(f'{name:16s} vs N7 {rel:22s} text identical: {same_text}; AST identical: {same_ast}')
    if not same_text:
        for line in difflib.unified_diff(a.splitlines(), b.splitlines(), 'N7', 'N8', lineterm='', n=0): print('      ' + line[:230])
for rel in ('vendor/core.py', 'text_analysis.py', 'fewepoch_analysis.py'):
    print(f'N8 source/{rel} byte-identical to N7 sealed-source/{rel}:', sha(N8 / 'source' / rel) == sha(N7 / rel), sha(N7 / rel)[:16])
