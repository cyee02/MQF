---
name: pr-readme
description: Update the repository README.md to reflect the branch's changes before opening a pull request. Use whenever the user asks to create, open, or raise a PR (gh pr create), or asks to refresh the README index of notebooks, assignments, and course folders.
---

# PR README update

Every pull request in this repo must carry a README.md that matches what the
branch actually contains. Run this before `gh pr create`, never after.

## Steps

1. **See what changed.** Diff the branch against the base:

   ```bash
   BASE=$(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|origin/||' || echo main)
   git diff --name-status "origin/$BASE"...HEAD
   git status --porcelain
   ```

   Include uncommitted work — it will be committed as part of the PR.

2. **Take stock of the repo layout.** The README is an index of course
   material, so list what exists now, not what the diff touched alone:

   ```bash
   find . -name '*.ipynb' -not -path './.git/*' -not -path '*/.ipynb_checkpoints/*' | sort
   find . -name 'README.md' -not -path './.git/*' | sort
   ```

3. **Read the current `README.md`** at the repo root. If it does not exist,
   create it using the structure in "README shape" below.

4. **Update it.** Apply only what the branch justifies:
   - New notebook, folder, or assignment → add a row linking to it.
   - Renamed or moved file → fix the path so no link 404s.
   - Deleted file → remove its row.
   - A folder that has its own `README.md` → link the folder, since GitHub
     renders that README when the folder is opened.
   - Nothing structural changed → leave the README alone and say so. Do not
     invent churn to have something to commit.

   Use URL-encoded paths for links containing spaces (`%20`).

5. **Commit and open the PR.** Include the README change in the same commit or
   a dedicated `docs: update README` commit on the branch, then create the PR.
   Mention the README update in the PR body.

## README shape

Keep it short and scannable — this is a coursework repo, not a product:

```markdown
# MQF

Coursework, notebooks, and notes for the MQF programme.

## QF600 — Asset Pricing

| Work | Notes |
|---|---|
| [Assignment 1 — Compute Alpha](QF600/Assignment%201%20-%20Compute%20Alpha/) | Alpha/beta decomposition of an investor portfolio vs. a benchmark |

## QF627 — Programming

| Notebook | Topic |
|---|---|
| [Pre-course 01](QF627_PreCourse_01_Introduction_PREview.ipynb) | Python introduction |
```

## Checks before finishing

- Every link resolves to a path that exists (`ls` the target).
- No entry describes work that is not on the branch.
- The README's headings still match the folders on disk.
