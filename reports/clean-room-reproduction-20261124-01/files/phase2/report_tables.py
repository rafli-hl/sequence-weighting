import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
A, B = c["variants"]["ecdf_arrays"], c["variants"]["ordinal_record"]
print("| Statistic | Draw | Status (mine / published) | Bracket | Intervals holding | Weight: primary | Weight: published | Value: primary | Value: ordinal_record | Value: published | Diff primary | Diff ordinal_record |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for ra, rb in zip(A["matched"]["rows"], B["matched"]["rows"]):
    step, draw, ms, ps, lo, hi, n, wm, wp, vm, vp, d = ra
    vb = rb[9]
    f = lambda x, k=9: "" if x is None else ("%." + str(k) + "f") % x
    print("| %s | %s | %s / %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        step, draw, ms, ps, ("E%s-E%s" % (lo, hi)) if lo else ("E3 (fixed)" if ms == "READ" else "none"), n, f(wm, 7), f(wp, 7), f(vm, 10), f(vb, 10), f(vp, 10),
        "" if vm is None else "%.1e" % abs(vm - vp), "" if vb is None else "%.1e" % abs(vb - vp)))
print()
for v in ("ecdf_arrays", "ordinal_arrays", "ecdf_record", "ordinal_record"):
    f = c["variants"][v]["fits"]
    print(v, "max|dp| %.3e at %s, mean %.3e, n>1e-6: %d" % (f["max_abs_dp"], f["at"], f["mean_abs_dp"], f["n_over_1e-6"]))
    for s, e in c["variants"][v]["statistics"].items():
        if e.get("mean_pub") is not None:
            print("   %s mean %.10f CI [%.10f, %.10f] d_mean %.1e d_ci %.1e loo %.1e | pub mean %.10f CI [%.10f, %.10f]" % (s, e["mean_mine"], e["ci_mine"][0], e["ci_mine"][1], e["d_mean"], e["d_ci"], e["loo_max_abs_diff"], e["mean_pub"], e["ci_pub"][0], e["ci_pub"][1]))
    print("   loo sides pub/mine S3:", c["variants"][v]["statistics"]["S3"].get("loo_pub_sides"))
