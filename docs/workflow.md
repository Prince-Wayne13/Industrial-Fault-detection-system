# How we work

One rule: **decide first in writing, then change the document.** That keeps the decisions and the document from drifting apart.

## Steps

1. **Discuss.** Put open questions in `open-items.md`.
2. **Decide.** When the team agrees, record it:
   - a requirement choice goes in `requirement-decisions.md`, against its requirement number, with who decided it;
   - a how-we-build-it choice goes in `design-decisions.md`.
   Then remove the item from `open-items.md`.
3. **Apply.** Change the Word file `srs/SRS_Industrial_Fault_Detection.docx`. Update the version and the revision history on the cover.
4. **Export.** Run `./scripts/export-md.sh` (needs pandoc). It refreshes the plain-text copy.
5. **Commit.** Save the Word file and the text copy together, with a message that names the requirements, for example `FR-7: alerts as pop-ups to connected users`.
6. **Tag.** When a version is handed in or shared: `git tag -a v2.0 -m "SRS v2.0"`.
7. **Check.** Before every hand-in, run the document against `docs/review/general-questions-checklist.md` and fill in the "After" column.

## Rules of thumb

- One topic per commit. Do not mix a renumbering with a new requirement.
- Never edit `srs/SRS_Industrial_Fault_Detection.md` by hand. It is overwritten by the script.
- Removing text from the document needs the team's agreement. Say so in the commit message.
- For a big change, work on a branch (`git switch -c fr6-trend-check`) and merge it when the team agrees.
- Word cannot merge two people's edits. Only one person edits the Word file at a time.

## The few git commands you need

| Task | Command |
| --- | --- |
| See what changed | `git status` and `git diff` |
| Save your work | `git add -A` then `git commit -m "message"` |
| See the history | `git log --oneline` |
| Compare two versions | `git diff v1.5 v1.6 -- srs/SRS_Industrial_Fault_Detection.md` |
| Start a branch | `git switch -c branch-name` |
| Go back to main | `git switch main` |
| Share your work | `git push` |
| Get the team's work | `git pull` |
