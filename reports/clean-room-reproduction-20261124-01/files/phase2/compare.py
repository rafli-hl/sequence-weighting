#!/usr/bin/env python
"""Phase 2: compare the frozen outputs with the published tables. Reads only; changes nothing frozen.

Usage: python -I -B compare.py <frozen out folder> <published folder> <comparison output json>
"""
import csv
import json
import os
import sys

OUT, PUB, DEST = sys.argv[1], sys.argv[2], sys.argv[3]
VARIANTS = ["ecdf_arrays", "ordinal_arrays", "ecdf_record", "ordinal_record"]
STEPS = ["P1", "S1", "S3", "S4", "S5", "S2"]
DRAWS = ["m01", "m02", "m03", "m04", "m05", "m06"]


def rd_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fl(x):
    return None if x in ("", None) else float(x)


pub_points = {(r["draw"], int(r["width"]), r["tag"], float(r["epoch"])): r for r in rd_csv(os.path.join(PUB, "POINTS.csv"))}
pub_fits = {(r["draw"], int(r["width"]), r["tag"], float(r["epoch"])): r for r in rd_csv(os.path.join(PUB, "FITS.csv"))}
pub_matched = {(r["statistic"], r["draw"]): r for r in rd_csv(os.path.join(PUB, "MATCHED.csv"))}
with open(os.path.join(PUB, "ANALYSIS.json"), encoding="utf-8") as f:
    pub = json.load(f)

report = {"published_rows": {"POINTS": len(pub_points), "FITS": len(pub_fits), "MATCHED": len(pub_matched)}, "variants": {}}
print("published rows: POINTS %d, FITS %d, MATCHED %d" % (len(pub_points), len(pub_fits), len(pub_matched)))
print("POINTS.p == FITS.p for every fit:", all(pub_points[k]["p"] == pub_fits[k]["p"] for k in pub_points))
print("published MATCHED statistics:", sorted({k[0] for k in pub_matched}))


def maxdiff(pairs):
    """pairs: list of (key, mine, published). Returns (max abs diff, key)."""
    best = (0.0, None)
    for key, a, b in pairs:
        if a is None or b is None:
            if a is not b:
                best = (float("inf"), key)
            continue
        d = abs(a - b)
        if d > best[0]:
            best = (d, key)
    return best


for v in VARIANTS:
    mine = {(r["draw"], int(r["width"]), r["rate"], float(r["readout"])): r for r in rd_csv(os.path.join(OUT, v, "per_readout.csv"))}
    with open(os.path.join(OUT, v, "analysis.json"), encoding="utf-8") as f:
        an = json.load(f)
    mm = {(r["step"], r["draw"]): r for r in rd_csv(os.path.join(OUT, v, "matched.csv"))}
    mc = {(r["step"], r["draw"]): r for r in rd_csv(os.path.join(OUT, v, "contrasts.csv"))}
    res = {}
    assert set(mine) == set(pub_fits) == set(pub_points), "fit keys differ"

    # ---- A. the 240 fits
    dp = [(k, float(mine[k]["p_star"]), float(pub_fits[k]["p"])) for k in mine]
    md = maxdiff(dp)
    over = [(k, a, b) for k, a, b in dp if abs(a - b) > 1e-6]
    res["fits"] = {
        "n": len(dp), "max_abs_dp": md[0], "at": md[1], "n_over_1e-6": len(over), "over_1e-6": over,
        "mean_abs_dp": sum(abs(a - b) for _, a, b in dp) / len(dp),
        "max_rel_objective": max(abs(float(mine[k]["objective"]) / float(pub_fits[k]["objective"]) - 1) for k in mine),
        "max_abs_total_gain": max(abs(float(mine[k]["total_gain"]) - float(pub_fits[k]["total_gain"])) for k in mine),
        "flags_equal": all((mine[k]["at_lower"] == "1") == (pub_fits[k]["lower"] == "True")
                           and (mine[k]["at_upper"] == "1") == (pub_fits[k]["upper"] == "True") for k in mine),
        "published_reasons": sorted({pub_fits[k]["reason"] for k in mine}),
        "mine_all_defined": all(mine[k]["defined"] == "1" for k in mine),
    }
    # ---- B. losses
    res["losses"] = {}
    for col, pcol in (("train", "train"), ("val", "validation"), ("gap", "gap")):
        res["losses"][col] = maxdiff([(k, float(mine[k][col]), float(pub_points[k][pcol])) for k in mine])[0]
    res["losses"]["train_array_vs_published"] = maxdiff([(k, float(mine[k]["train_array"]), float(pub_points[k]["train"])) for k in mine])[0]
    res["losses"]["train_record_vs_published"] = maxdiff([(k, float(mine[k]["train_record"]), float(pub_points[k]["train"])) for k in mine])[0]
    res["losses"]["val_record_vs_published"] = maxdiff([(k, float(mine[k]["val_record"]), float(pub_points[k]["validation"])) for k in mine])[0]

    # ---- C. matched readings (MATCHED.csv), and the same fields in ANALYSIS.json rows
    rows = []
    worst = {"weight": 0.0, "target": 0.0, "p_read": 0.0, "p_first": 0.0, "position": 0.0, "value": 0.0}
    structural = []
    for (step, draw), pr in sorted(pub_matched.items()):
        if (step, draw) in mm:
            m = mm[(step, draw)]
            my_status = "READ" if m["status"] == "AVAILABLE" else {"target outside the path": "TARGET_OUTSIDE_PATH",
                                                                    "undefined fit": "UNDEFINED_FIT",
                                                                    "draw missing": "DRAW_MISSING"}[m["reason"]]
            ok = my_status == pr["status"] and fl(m["bracket_lo"]) == fl(pr["between_low"]) \
                and fl(m["bracket_hi"]) == fl(pr["between_high"]) \
                and int(m["n_intervals"]) == int(pr["intervals_holding_the_target"])
            if not ok:
                structural.append([step, draw, my_status, pr["status"], m["bracket_lo"], pr["between_low"],
                                   m["bracket_hi"], pr["between_high"], m["n_intervals"], pr["intervals_holding_the_target"]])
            diffs = {}
            for mine_col, pub_col, name in (("weight_on_later", "weight", "weight"), ("target", "target", "target"),
                                            ("p768_read", "p_read", "p_read"), ("p512_E3", "p_first", "p_first"),
                                            ("position", "read_at_readout", "position"), ("value", "value", "value")):
                a, b = fl(m[mine_col]), fl(pr[pub_col])
                if a is None and b is None:
                    continue
                d = float("inf") if (a is None or b is None) else abs(a - b)
                diffs[name] = d
                worst[name] = max(worst[name], d)
            rows.append([step, draw, my_status, pr["status"], m["bracket_lo"], m["bracket_hi"], m["n_intervals"],
                         fl(m["weight_on_later"]), fl(pr["weight"]), fl(m["value"]), fl(pr["value"]), diffs])
        else:
            # fixed-update statistics: published MATCHED.csv may list them too
            c = mc[(step, draw)]
            my_status = "READ" if c["status"] == "AVAILABLE" else c["reason"]
            if my_status != pr["status"]:
                structural.append([step, draw, my_status, pr["status"]])
            a, b = fl(c["value"]), fl(pr["value"])
            d = abs(a - b)
            worst["value"] = max(worst["value"], d)
            rows.append([step, draw, my_status, pr["status"], "", "", "", None, fl(pr["weight"]), a, b, {"value": d}])
    res["matched"] = {"rows_compared": len(rows), "structural_mismatches": structural, "max_abs_diff": worst, "rows": rows}

    # ---- D. registered statistics
    st = {}
    for s in STEPS:
        a, p = an["statistics"][s], pub["statistics"][s]
        e = {"n_mine": a["n_available"], "n_pub": len(p["available"]),
             "available_equal": a["available_draws"] == p["available"],
             "label_mine": a["label"], "label_pub": p["label"], "label_equal": a["label"] == p["label"],
             "side_mine": a["side"], "status_pub": p["status"],
             "unavailable_mine": a["unavailable"], "unavailable_pub": p["unavailable"],
             "counts_equal": [a["unavailable_counts"]["undefined fit"], a["unavailable_counts"]["target outside the path"],
                              a["unavailable_counts"]["draw missing"]]
             == [p["unavailable_counts"]["UNDEFINED_FIT"], p["unavailable_counts"]["TARGET_OUTSIDE_PATH"],
                 p["unavailable_counts"]["DRAW_MISSING"]],
             "sign_mine": [a["sign_test"]["positive"], a["sign_test"]["negative"], a["sign_test"]["p_two_sided"]],
             "sign_pub": [p["sign_test"]["positive"], p["sign_test"]["negative"], p["sign_test"]["p"]],
             "max_abs_value_diff": max(abs(a["values"][d] - p["values"][d]) for d in p["values"]),
             "values_same_draws": sorted(d for d in a["values"] if a["values"][d] is not None) == sorted(p["values"])}
        e["sign_equal"] = e["sign_mine"] == e["sign_pub"]
        if "interval" in p:
            pi = p["interval"]
            e.update(mean_mine=a["mean"], mean_pub=pi["mean"], d_mean=abs(a["mean"] - pi["mean"]),
                     sd_mine=a["sd"], sd_pub=pi["sd"], d_sd=abs(a["sd"] - pi["sd"]),
                     ci_mine=[a["ci_low"], a["ci_high"]], ci_pub=pi["interval"],
                     d_ci=max(abs(a["ci_low"] - pi["interval"][0]), abs(a["ci_high"] - pi["interval"][1])),
                     t_crit_mine=a["t_crit"], t_crit_pub=pi["t_critical"], df_equal=a["df"] == pi["df"],
                     pub_t_p=pi.get("p"))
        else:
            e.update(mean_mine=a["mean"], mean_pub=None, ci_mine=[a["ci_low"], a["ci_high"]], ci_pub=None,
                     note="published has no interval for this statistic")
        if p.get("leave_one_out"):
            lm = {r["dropped"]: r for r in a["leave_one_out"]["intervals"]}
            dl, sides = 0.0, True
            for d, pr in p["leave_one_out"].items():
                dl = max(dl, abs(lm[d]["ci_low"] - pr["interval"][0]), abs(lm[d]["ci_high"] - pr["interval"][1]),
                         abs(lm[d]["mean"] - pr["mean"]))
                mine_side = {"above": "ABOVE", "below": "BELOW", "spans": "SPANS"}[lm[d]["side"]]
                sides = sides and ((mine_side == pr["side"]) or (mine_side == "SPANS" and not pr["excludes_zero"]))
                e.setdefault("loo_pub_sides", {})[d] = [pr["side"], pr["excludes_zero"], lm[d]["side"]]
            e.update(loo_n=len(p["leave_one_out"]), loo_max_abs_diff=dl, loo_sides_equal=sides)
        else:
            e.update(loo_n=0, loo_mine_is_none=a["leave_one_out"] is None)
        e["saturation_mine"] = a["saturation"]["label"]
        e["flagged_pub"] = p.get("flagged")
        e["S32_pub"] = p.get("S32")
        st[s] = e
    res["statistics"] = st
    res["sequence_pub"] = [[x["step"], x["label"], x["status"], x["read_as_confirmation"], x["confirmed"]] for x in pub["sequence"]]
    res["sequence_mine"] = [[s, an["statistics"][s]["label"], an["statistics"][s]["side"], an["statistics"][s]["reached"]] for s in STEPS]
    res["section7_row_mine"] = an["section7_row"]

    # ---- E. diagnostics and descriptives
    diag = {"records_against_arrays": [an["records_against_arrays"]["max_abs_difference"],
                                       pub["records_against_arrays"]["max_absolute_difference"]],
            "fit_bounds_pub": pub["fit_bounds"],
            "fit_bounds_mine": {"upper": an["fit_summary"]["n_at_upper"], "lower": an["fit_summary"]["n_at_lower"],
                                "undefined": an["fit_summary"]["n_fits"] - an["fit_summary"]["n_defined"]}}
    no = {}
    for arm, pa in pub["not_overfit"]["arms"].items():
        w, r = arm.split("|")
        ma = an["not_overfit"]["w%s_%s" % (w, r)]
        no[arm] = {"label_mine": ma["label"], "label_pub": pa["label"],
                   "d_mean": abs(ma["mean"] - pa["interval"]["mean"]),
                   "d_ci": max(abs(ma["ci_low"] - pa["interval"]["interval"][0]), abs(ma["ci_high"] - pa["interval"]["interval"][1]))}
    diag["not_overfit"] = no
    br = {"max_d_value": 0.0, "max_d_mean": 0.0, "max_d_ci": 0.0, "max_d_panel": {"p": 0.0, "train": 0.0, "validation": 0.0, "gap": 0.0}}
    for ek, ev in pub["by_readout"].items():
        for cname, rate in (("D4", "lr1e-04"), ("D2", "lr3e-04")):
            pc = ev["contrasts"][cname]
            mcn = an["descriptives"]["fixed_update_by_readout"]["%s_%s" % (rate, ek)]
            br["max_d_value"] = max(br["max_d_value"], max(abs(mcn["values"][d] - pc["values"][d]) for d in pc["values"]))
            br["max_d_mean"] = max(br["max_d_mean"], abs(mcn["mean"] - pc["interval"]["mean"]))
            br["max_d_ci"] = max(br["max_d_ci"], abs(mcn["ci_low"] - pc["interval"]["interval"][0]),
                                 abs(mcn["ci_high"] - pc["interval"]["interval"][1]))
        for arm, pp in ev["panel"].items():
            w, r = arm.split("|")
            mp = an["descriptives"]["panel"]["w%s_%s_%s" % (w, r, ek)]
            for a_, b_ in (("p_star", "p"), ("train", "train"), ("val", "validation"), ("gap", "gap")):
                br["max_d_panel"][b_] = max(br["max_d_panel"][b_], abs(mp[a_] - pp[b_]))
    diag["by_readout"] = br
    re_ = {}
    for w in ("512", "768"):
        pv = pub["rate_effects"][w]["p"]
        mv = an["descriptives"]["rate_effect_at_E3"]["w%s_3e-4_minus_1e-4" % w]
        re_[w] = {"same_sign_max_diff": max(abs(mv["values"][d] - pv["values"][d]) for d in pv["values"]),
                  "opposite_sign_max_diff": max(abs(mv["values"][d] + pv["values"][d]) for d in pv["values"]),
                  "mean_mine": mv["mean"], "mean_pub": pv["interval"]["mean"],
                  "ci_mine": [mv["ci_low"], mv["ci_high"]], "ci_pub": pv["interval"]["interval"]}
    diag["rate_effects_p"] = re_
    cl = {}
    for arm, pl in pub["losses"].items():
        w, r = arm.split("|")
        if r == "E0":
            me = an["descriptives"]["e0"]["w%s" % w]
            cl[arm] = {"d_train": abs(me["train_mean"] - pl["train"]), "d_validation": abs(me["val_mean"] - pl["validation"])}
        else:
            mcl = an["descriptives"]["clipping"]["w%s_%s" % (w, r)]
            per = mcl["per_draw"]
            gmean = sum(x["gradient_norm_mean"] for x in per.values()) / len(per)
            gmax = max(x["gradient_norm_max"] for x in per.values())
            cl[arm] = {"d_clip_fraction_mean": abs(mcl["clip_fraction_mean"] - pl["clipping"]["clip_fraction_mean"]),
                       "d_gradient_norm_mean": abs(gmean - pl["clipping"]["gradient_norm_mean"]),
                       "d_gradient_norm_max": abs(gmax - pl["clipping"]["gradient_norm_max"])}
    diag["losses_block"] = cl
    res["diagnostics"] = diag
    report["variants"][v] = res

    print("\n================ variant %s ================" % v)
    f = res["fits"]
    print("FITS: n=%d  max|dp|=%.3e at %s  mean|dp|=%.3e  n(|dp|>1e-6)=%d  max rel objective diff=%.3e  max|d total_gain|=%.3e  flags equal=%s  all defined=%s  published reasons=%s"
          % (f["n"], f["max_abs_dp"], f["at"], f["mean_abs_dp"], f["n_over_1e-6"], f["max_rel_objective"],
             f["max_abs_total_gain"], f["flags_equal"], f["mine_all_defined"], f["published_reasons"]))
    print("LOSSES max|diff| vs POINTS.csv: this variant train %.3e val %.3e gap %.3e | array-mean train %.3e | record train %.3e, record val %.3e"
          % (res["losses"]["train"], res["losses"]["val"], res["losses"]["gap"], res["losses"]["train_array_vs_published"],
             res["losses"]["train_record_vs_published"], res["losses"]["val_record_vs_published"]))
    m = res["matched"]
    print("MATCHED: rows %d, structural mismatches (status/bracket/count): %d %s" % (m["rows_compared"], len(m["structural_mismatches"]), m["structural_mismatches"]))
    print("   max|diff|: " + ", ".join("%s %.3e" % (k, x) for k, x in m["max_abs_diff"].items()))
    for s in STEPS:
        e = st[s]
        if e.get("mean_pub") is not None:
            print("%s: n %d/%d  mean %.12f | %.12f (d %.2e)  CI [%.12f, %.12f] | [%.12f, %.12f] (d %.2e)  sd d %.2e  label %s | %s  sign %s | %s  LOO n=%d max d %.2e sides equal %s  values d %.2e"
                  % (s, e["n_mine"], e["n_pub"], e["mean_mine"], e["mean_pub"], e["d_mean"], e["ci_mine"][0], e["ci_mine"][1],
                     e["ci_pub"][0], e["ci_pub"][1], e["d_ci"], e["d_sd"], e["label_mine"], e["label_pub"], e["sign_mine"],
                     e["sign_pub"], e["loo_n"], e["loo_max_abs_diff"], e["loo_sides_equal"], e["max_abs_value_diff"]))
        else:
            print("%s: n %d/%d  label %s | %s  sign %s | %s  unavailable %s | %s  values d %.2e  (published prints no interval; mine, not read: mean %.12f CI [%.12f, %.12f])"
                  % (s, e["n_mine"], e["n_pub"], e["label_mine"], e["label_pub"], e["sign_mine"], e["sign_pub"],
                     e["unavailable_mine"], e["unavailable_pub"], e["max_abs_value_diff"], e["mean_mine"], e["ci_mine"][0], e["ci_mine"][1]))
    print("DIAG: records_against_arrays mine %.12e | published %.12e ; fit_bounds mine %s | published %s"
          % (diag["records_against_arrays"][0], diag["records_against_arrays"][1], diag["fit_bounds_mine"], diag["fit_bounds_pub"]))
    print("   NOT_OVERFIT:", {k: (x["label_mine"], x["label_pub"], "%.2e" % x["d_mean"], "%.2e" % x["d_ci"]) for k, x in no.items()})
    print("   by_readout contrasts: max d value %.2e, mean %.2e, CI %.2e ; panel max d %s" % (br["max_d_value"], br["max_d_mean"], br["max_d_ci"], {k: "%.2e" % x for k, x in br["max_d_panel"].items()}))
    print("   rate effects (p): " + "; ".join("w%s same-sign d %.2e, opposite-sign d %.2e" % (w, x["same_sign_max_diff"], x["opposite_sign_max_diff"]) for w, x in re_.items()))
    print("   losses block:", {k: {a: "%.2e" % b for a, b in x.items()} for k, x in cl.items()})

with open(DEST, "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=1, sort_keys=True, default=str)
    f.write("\n")
print("\nwrote", DEST)
