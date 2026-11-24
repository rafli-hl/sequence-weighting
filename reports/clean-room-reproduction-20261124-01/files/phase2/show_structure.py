import json, sys
a = json.load(open(sys.argv[1], encoding="utf-8"))
def walk(o, pre="", depth=0, maxdepth=4):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and depth < maxdepth:
                print("  " * depth + str(k) + ("  {dict %d}" % len(v) if isinstance(v, dict) else "  [list %d]" % len(v)))
                walk(v, pre + "/" + str(k), depth + 1, maxdepth)
            else:
                s = json.dumps(v)
                print("  " * depth + str(k) + " = " + (s if len(s) < 160 else s[:160] + "..."))
    elif isinstance(o, list):
        if o and isinstance(o[0], (dict, list)):
            print("  " * depth + "[0]:")
            walk(o[0], pre + "/0", depth + 1, maxdepth)
        else:
            s = json.dumps(o)
            print("  " * depth + (s if len(s) < 160 else s[:160] + "..."))
skip = set(sys.argv[2:])
for k, v in a.items():
    if k in skip:
        print(k, "(skipped)", type(v).__name__, len(v) if hasattr(v, "__len__") else "")
        continue
    print("#", k)
    walk({k: v}, maxdepth=5)
