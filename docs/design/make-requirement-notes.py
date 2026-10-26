#!/usr/bin/env python3
"""Make one small note per requirement and per use case for Obsidian.

Reads srs/SRS_Industrial_Fault_Detection.md and writes to docs/design/requirements/.
Existing notes keep their 'status' value; only the text is refreshed.
Run from the repo root:  python3 docs/design/make-requirement-notes.py
"""
import re, pathlib, json

root = pathlib.Path(__file__).resolve().parent.parent.parent
srs = (root / "srs" / "SRS_Industrial_Fault_Detection.md").read_text(encoding="utf-8").splitlines()
out = root / "docs" / "design" / "requirements"
out.mkdir(parents=True, exist_ok=True)
plan = json.loads((root / "docs" / "design" / "test-plan.json").read_text(encoding="utf-8"))
SC, TS = plan["scenarios"], plan["tests"]
def scen_names(keys):
    return ", ".join(SC[k.strip()]["name"] for k in keys.split(","))


def old_status(path):
    if path.exists():
        m = re.search(r"^status: (.*)$", path.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip()
    return "not-set"

req = re.compile(r"^((?:FR|PR|NFR)-\d+[a-z]?): (.*)$")
count = 0
for line in srs:
    m = req.match(line.strip())
    if not m:
        continue
    rid, text = m.groups()
    kind = rid.split("-")[0]
    p = out / f"{rid}.md"
    tp = TS.get(rid)
    fm_test = f"test: {tp['method']}\nscenarios: [{scen_names(tp['scenarios'])}]\n" if tp else ""
    body_test = ""
    if tp:
        body_test = (f"## How to test (draft)\n\n- **Method:** {tp['method']}\n"
                     f"- **Seeded scenario:** {scen_names(tp['scenarios'])}\n"
                     f"- **What to do:** {tp['steps']}\n- **Passes if:** {tp['pass']}\n\n")
    p.write_text(
        f"---\ntitle: {rid}\nkind: {kind}\nstatus: {old_status(p)}\n{fm_test}tags: [requirement, {kind}]\n---\n\n"
        f"# {rid}\n\n{text}\n\n{body_test}"
        f"Status is one of: built, simulated, left-out, not-set. Change the `status` line above.\n\n"
        f"The pages that cover this requirement show up under Backlinks.\n",
        encoding="utf-8")
    count += 1

uc_head = re.compile(r"^### \*\*(UC-\d+): (.*)\*\*$")
i = 0
ucs = 0
while i < len(srs):
    m = uc_head.match(srs[i].strip())
    if m:
        uid, title = m.groups()
        actor = goal = ""
        for j in range(i + 1, min(i + 12, len(srs))):
            a = re.match(r"\*\*Primary Actor:\*\* (.*)", srs[j])
            g = re.match(r"\*\*Goal:\*\* (.*)", srs[j])
            if a: actor = a.group(1)
            if g: goal = g.group(1)
        (out / f"{uid}.md").write_text(
            f"---\ntitle: {uid}\nkind: UC\ntags: [use-case]\n---\n\n# {uid}: {title}\n\n"
            f"**Who:** {actor}\n\n**Goal:** {goal}\n\n"
            f"The full steps are in the SRS. The pages that support this use case show up under Backlinks.\n",
            encoding="utf-8")
        ucs += 1
    i += 1
print(f"{count} requirement notes, {ucs} use case notes")

# one table of every test, and the list of scenarios
order = sorted(TS, key=lambda r: (r.split("-")[0], int(re.search(r"\d+", r).group()), r))
lines = ["---","title: Test plan","status: draft","tags: [design, test-plan]","---","","# Test plan","",
 "Back to [[page-map]].","",
 "Every requirement, how it is tested, and which seeded scenario shows it. Made by the script from `test-plan.json`. Edit that file, not this note.","",
 "## The four ways to test","",
 "| Method | Meaning |","| --- | --- |",
 "| inject | Play a seeded scenario and watch the result. |",
 "| look | Check something on screen. |",
 "| inspect | Show it in the settings, the database or the code. |",
 "| measure | Run the seed data and read off a number. |","",
 "## Every requirement","",
 "| Requirement | Method | Scenario | Passes if |","| --- | --- | --- | --- |"]
for r in order:
    x = TS[r]
    lines.append(f"| [[{r}]] | {x['method']} | {scen_names(x['scenarios'])} | {x['pass']} |")
lines += ["","## The seeded scenarios","","| Scenario | What the seed data does | Tests |","| --- | --- | --- |"]
for k, v in SC.items():
    users = [r for r in order if k in [s.strip() for s in TS[r]["scenarios"].split(",")]]
    lines.append(f"| {v['name']} | {v['what']} | {len(users)} |")
(root / "docs" / "design" / "test-plan.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("test plan written")
