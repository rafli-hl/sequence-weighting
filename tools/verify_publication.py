"""Check this publication copy against its manifest, and check its Markdown links.

    python tools/verify_publication.py            # from the repository root; Python 3.8+, no dependencies

1. Every row of PUBLICATION_MANIFEST.csv (path, bytes, sha256) is compared with the file on disk, and every published
   file must have a row. The published files are git's tracked files; in a copy without git (a downloaded archive)
   they are every file that .gitignore does not exclude, so environments, caches, fetched assets, run folders and the
   estimator fixture's output left by a reader's own work are not counted. A file whose
   bytes differ only by line endings (CRLF from a Windows checkout with core.autocrlf=true) is reported as
   LINE_ENDINGS, not as a content mismatch. To get the canonical bytes on Windows, clone with
       git -c core.autocrlf=false clone https://github.com/rafli-hl/sequence-weighting.git
2. Every inline Markdown link to a local path in a published file, outside fenced code, is resolved
   case-sensitively. Links listed in
   PUBLICATION_LINK_LIMITATIONS.json as known unavailable are reported separately.

Exit status is 0 when there are no content mismatches, no missing or unlisted files and no unexpected broken links.
"""
import csv
import fnmatch, hashlib, json, os, re, subprocess, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def exists_case_sensitive(path):
    p = ROOT
    for part in path.relative_to(ROOT).parts:
        if part in ("", "."):
            continue
        if part == "..":
            p = p.parent; continue
        if not p.is_dir() or part not in os.listdir(p):
            return False
        p = p / part
    return True


def ignore_rules():
    """The patterns of .gitignore, as (pattern, directory_only, anchored). The file has no negated patterns."""
    rules = []
    for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        assert not line.startswith("!"), "negated .gitignore patterns are not supported here"
        directory_only = line.endswith("/")
        line = line.rstrip("/")
        anchored = "/" in line
        rules.append((line.lstrip("/"), directory_only, anchored))
    return rules


def is_ignored(rel, rules):
    """True if .gitignore excludes this path, following git's rules for the plain patterns the file uses."""
    parts = rel.split("/")
    for pattern, directory_only, anchored in rules:
        # Candidate paths: every leading directory, and the file itself unless the pattern names directories only.
        prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + (0 if directory_only else 1))]
        for prefix in prefixes:
            if anchored:
                if fnmatch.fnmatchcase(prefix, pattern):
                    return True
            elif fnmatch.fnmatchcase(prefix.rsplit("/", 1)[-1], pattern):
                return True
    return False


def published_files():
    """The files of this copy: git's tracked files in a checkout, otherwise every file .gitignore does not exclude."""
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
        return {p for p in out.decode("utf-8").split("\0") if p}
    except (OSError, subprocess.CalledProcessError):
        rules = ignore_rules()
        files = (p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
        return {rel for rel in files if not rel.startswith(".git/") and not is_ignored(rel, rules)}


def check_manifest(published):
    ok = line_endings = 0; bad, missing = [], []
    with open(ROOT / "PUBLICATION_MANIFEST.csv", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    unlisted = sorted(published - {r["path"] for r in rows} - {"PUBLICATION_MANIFEST.csv"})
    for r in rows:
        f = ROOT / r["path"]
        if not f.is_file():
            missing.append(r["path"]); continue
        b = f.read_bytes()
        if len(b) == int(r["bytes"]) and sha(b) == r["sha256"]:
            ok += 1
        elif sha(b.replace(b"\r\n", b"\n")) == r["sha256"] or sha(b.replace(b"\n", b"\r\n").replace(b"\r\r\n", b"\r\n")) == r["sha256"]:
            line_endings += 1
        else:
            bad.append(r["path"])
    return len(rows), ok, line_endings, bad, missing, unlisted


LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def check_links(published):
    known = {(e["document"], e["target"]) for e in json.loads((ROOT / "PUBLICATION_LINK_LIMITATIONS.json").read_text(encoding="utf-8"))["links"]}
    checked, broken, known_hit = 0, [], []
    for rel in sorted(p for p in published if p.endswith(".md")):
        md = ROOT / rel
        if not md.is_file():
            continue  # a missing file is reported by the manifest check
        fenced = False
        for n, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced; continue
            if fenced:
                continue
            for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                    continue
                checked += 1
                dest = (md.parent / urllib.parse.unquote(target.split("#")[0])).resolve()
                if not exists_case_sensitive(dest):
                    (known_hit if (rel, target) in known else broken).append(f"{rel}:{n} -> {target}")
    return checked, broken, known_hit


if __name__ == "__main__":
    published = published_files()
    total, ok, crlf, bad, missing, unlisted = check_manifest(published)
    print(f"manifest: {total} rows; {ok} exact; {crlf} differ only in line endings; {len(bad)} mismatched; {len(missing)} missing; "
          f"{len(unlisted)} published files not in the manifest")
    for p in bad[:20]: print("  MISMATCH", p)
    for p in missing[:20]: print("  MISSING", p)
    for p in unlisted[:20]: print("  UNLISTED", p)
    if crlf:
        print("  LINE_ENDINGS: this checkout converted line endings. Clone with core.autocrlf=false for canonical bytes.")
    checked, broken, known_hit = check_links(published)
    print(f"links: {checked} local Markdown links checked; {len(known_hit)} known unavailable; {len(broken)} unexpected broken")
    for b in broken: print("  BROKEN", b)
    sys.exit(1 if bad or missing or unlisted or broken else 0)
