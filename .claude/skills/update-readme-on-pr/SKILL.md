---
name: update-readme-on-pr
description: Refresh README.md to match the repository's contents before opening a pull request. Use whenever a PR is about to be created or updated — "create a PR", "open a pull request", "gh pr create", "raise a PR for this branch" — and also when asked to check whether the README is stale. Keeps the root contents index and each assignment folder's README in step with the files actually on the branch.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# Update README on PR

Documentation in this repo drifts silently: a notebook gets added, renamed, or moved into a new
assignment folder, and the index in `README.md` still describes the old layout. This skill closes
that gap at the one moment it is cheap to fix — just before a pull request is opened.

## When to run

Run **before** `gh pr create`, so the README change is part of the PR rather than a follow-up
commit. Also run when asked to update or verify the README against the current branch.

Do not run on a branch with no committed changes, and do not touch the README when the branch's
changes cannot affect it (a typo fix inside one notebook cell, for example).

## Procedure

### 1. See what the branch actually changed

```bash
git fetch origin main --quiet
git diff --name-status origin/main...HEAD
```

Use `main...HEAD` (three dots) so the comparison is against the merge base, not whatever `main`
looks like right now. `--name-status` marks each path `A`dded, `M`odified, `D`eleted or `R`enamed —
adds, deletes and renames are the ones that usually require a README edit.

### 2. Decide whether the README is stale

The root `README.md` is an index, not a changelog. It needs editing when the branch:

- adds, deletes, or renames a notebook, a course folder, or an assignment folder;
- changes what a piece of work *does* in a way the one-line description no longer covers
  (different tickers, different horizon, a new section of analysis);
- changes a path the README links to.

It does **not** need editing for edits internal to a file that leave its purpose intact.

If nothing qualifies, say so and stop — a no-op is a valid outcome. Never manufacture an edit to
look busy.

### 3. Make the edit

- Keep the existing table structure and tone. Edit the affected rows; leave the rest alone.
- New assignment → new row: course, a link to the **folder** (not the file), and one sentence on
  what the work does. Percent-encode spaces in link targets (`Assignment%201%20-%20Compute%20Alpha/`).
- Describe only what you have verified by reading the files on the branch. Do not infer results,
  grades, or conclusions that are not written down.
- If an assignment folder gained files but has no `README.md`, flag it to the user rather than
  writing one unasked — an assignment write-up is theirs to author.

### 4. Check the links resolve

Every relative link must point at a path that exists on this branch:

```bash
grep -o '](\([^)h#][^)]*\))' README.md | sed 's/](//; s/)$//' | \
  while IFS= read -r p; do
    d=$(printf '%b' "${p//%/\\x}")   # percent-decode %20 etc.
    [ -e "$d" ] || echo "BROKEN: $p"
  done
```

A README that indexes files with dead links is worse than one that is slightly behind.

### 5. Commit onto the PR branch

```bash
git add README.md
git commit -m "Update README index for <what changed>"
```

Then open the PR as normal. Mention in the PR body that the README index was refreshed.

## Notes

- This is a *skill*, so it runs when the PR flow is recognised — reliable in practice, but it is not
  an enforcement mechanism. For a hard guarantee, add a GitHub Action on `pull_request` or a
  `pre-push` hook that fails when the README is stale.
- Assignment-level `README.md` files are the write-up for that assignment. This skill keeps their
  *links and paths* correct; it does not rewrite their content.
