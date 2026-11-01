# QF600 Final Project — Group 6 Set-up Guide

This guide takes you from a fresh laptop to working on the project with Claude Code in VS Code. Allow about 30–45 minutes.

**Key dates**
| What | When |
|------|------|
| Report, code and slides submission | **Tue 03 Nov 2026** |
| Presentation (20 min incl. Q&A) | **Wed 04 Nov 2026** |

---

## What's in this folder

| File | What it is | Submitted? |
|------|-----------|-----------|
| `01 - Project Report Group 6.docx` | Project report | Yes |
| `02 - Dataset Metadata Group 6.md` | Source, description, rows and columns of each dataset | Yes |
| `03 - execution_script_group_6.ipynb` | The notebook. All numbers and figures come from here | Yes |
| `04 - Presentation Slides Group 6.pptx` | Slides | Yes |
| `05 - Presentation Script.docx` | Script for each presenter, matching the slides | No |
| `QF600_Group_Project_Walkthrough.docx` | Our six-step execution plan | — |
| `plan.md` | Set-up plan for the project tooling | — |
| `context/` | Markdown summaries of the guideline, papers, lectures and Prof Liu's feedback (what Claude reads) | — |
| `figures/`, `outputs/` | Figures and numbers produced by the notebook | — |

Some files are **not in GitHub** (the repo is public). You get them from the team bundle (step 7):
`course_materials/` (guideline + lecture notes), `reference_paper/`, `reference_style/QF627_*.ipynb`, `datasets/`.

> Deliverables 01, 04 and 05 are created by the skills once the analysis is ready. If one is missing, it hasn't been created yet.

---

## 1. Install VS Code

1. Download from <https://code.visualstudio.com/> and install.
   - **Windows:** tick "Add to PATH" and "Open with Code" during install.
   - **Mac:** drag *Visual Studio Code* into *Applications*. Then open VS Code, press `Cmd+Shift+P`, type `shell command`, and choose **Shell Command: Install 'code' command in PATH**.
2. Open VS Code, go to the Extensions view (`Ctrl+Shift+X` on Windows, `Cmd+Shift+X` on Mac), and install:
   - **Python** (Microsoft)
   - **Jupyter** (Microsoft)

## 2. Install Git

- **Windows:** install from <https://git-scm.com/download/win> and keep the default options.
- **Mac:** open Terminal and run `git --version`. If Git isn't installed, macOS offers to install it. Click **Install**.

Then tell Git who you are (one time only):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 3. Install Python (3.11 or newer)

- Download from <https://www.python.org/downloads/>.
  - **Windows:** tick **"Add python.exe to PATH"** on the first installer screen.
- Check it worked. On Windows, the command may be `python` rather than `python3`.

```bash
python3 --version
```

## 4. Get a GitHub account and access

1. Sign up at <https://github.com> if you don't have an account.
2. Send your GitHub username to Chong Yee. You'll be added as a collaborator on `cyee02/MQF` so you can push changes.
3. Accept the invite email from GitHub.

## 5. Clone the repository

In VS Code: press `Ctrl+Shift+P` (`Cmd+Shift+P` on Mac), choose **Git: Clone**, and paste:

```
https://github.com/cyee02/MQF.git
```

Pick a folder (for example `Documents/`). Open it when VS Code asks. Sign in to GitHub in the browser if prompted.

> **Open the `QF600/Final Assignment` folder in VS Code** (*File → Open Folder…*) when working on this project. The project's Claude skills and `CLAUDE.md` live in that folder (`QF600/Final Assignment/.claude/skills/`), so they only apply to this project and don't interfere with other courses in the repo. Opening the `MQF` root also works: the skills load once Claude works on files in this folder.

## 6. Set up the Python environment

Open the VS Code terminal (``Ctrl+` ``) and run the commands below. If VS Code already has `QF600/Final Assignment` open, the terminal starts there: skip the `cd` line.

**Mac**
```bash
cd "QF600/Final Assignment"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
cd "QF600/Final Assignment"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks the activate script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

When you open the notebook, click **Select Kernel** (top right) → **Python Environments** → choose the one in `.venv`.

## 7. Get the team bundle (files not in GitHub)

Chong Yee shares a zip named `QF600_Final_Group6_bundle_<date>.zip`.

1. Put the zip directly inside `QF600/Final Assignment/`.
2. In Claude Code (step 9), type:
   ```
   Unpack the team bundle
   ```
   Claude checks the files, asks before overwriting anything you've changed, and updates the dataset metadata.

   *Without Claude:* unzip it in place so that `course_materials/`, `reference_paper/`, `reference_style/` and `datasets/` sit directly under `QF600/Final Assignment/`.
3. You can delete the zip afterwards. Zips are gitignored, so it won't be uploaded by accident.

## 8. Add your FRED API key

The notebook downloads interest-rate data from FRED.

1. Get a free key at <https://fred.stlouisfed.org/docs/api/api_key.html>. Create an account, then go to *My Account → API Keys*.
2. In `QF600/Final Assignment/`, copy `credentials.example.yaml` to a new file named `credentials.yaml`.
3. Replace `<your-fred-api-key>` with your key, so the line reads `fred_key: abc123…`. The notebook reads it as `creds["fred_key"]`.

`credentials.yaml` is gitignored. **Never paste your key into the notebook itself**, because the repo is public.

## 9. Install Claude Code in VS Code

You need a Claude account with Claude Code access: a **Pro, Max, Team or Enterprise** plan, or an Anthropic Console account with API credit.

1. Open the Extensions view (`Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Search **Claude Code** and install the one published by **Anthropic**.
3. Click the Claude (spark) icon in the sidebar or the top-right of the editor to open the Claude panel.
4. Click **Sign in** and log in with your Claude account in the browser. Return to VS Code when it says you're signed in.
5. Check it's working by typing in the Claude panel:
   ```
   Read QF600/Final Assignment/README.md and summarise what this project is about
   ```

Tips:
- Claude asks for permission before editing files or running commands. Read the request, then approve or decline.
- Type `/` in the Claude panel to see available commands and skills.
- Select code in the editor before asking. Claude sees your selection.

## 10. Project skills (what to ask Claude)

These skills come with the repo (in `QF600/Final Assignment/.claude/skills/`) and apply only to this project. You don't install anything extra: just ask in plain English, or type `/` and pick the skill.

| Skill | Ask something like | What it does |
|-------|--------------------|--------------|
| `qf600-notebook` | "Add the Exhibit 3 replication to the notebook" | Edits the notebook in the course style; saves figures to `figures/` and numbers to `outputs/results.json` |
| `qf600-report` | "Update the report's Step 4 section" | Updates the Word report from the notebook's numbers and figures |
| `qf600-slides` | "Update slide 6 and its script" | Updates slides and the presenter script together (speaker tag, timing, clicks) |
| `qf600-data-sync` | "I added a dataset, sync the metadata" | Profiles new files in `datasets/` and updates `02 - Dataset Metadata` and the report annex |
| `qf600-sync-check` | "Run the sync check" | Finds anything changed since the last sync, asks you to confirm each change, then updates the other files |
| `qf600-bundle` | "Pack the team bundle" / "Unpack the team bundle" | Zips or unzips the files not in GitHub |
| `pr-readme` | "Open a PR" | Updates the repo README before opening a pull request |


### Other useful skills

These aren't specific to this project, but they help with it. Type `/` in the Claude panel to see which ones your account has.

**Built into Claude Code**

| Skill | Use it for | Example |
|-------|-----------|---------|
| `/code-review` | Check notebook or script changes for bugs before you push (e.g. look-ahead bias, wrong date alignment) | `/code-review` |
| `/simplify` | Tidy up code you've written: remove duplication, make cells shorter and clearer | `/simplify` |
| `/security-review` | Check your branch for leaked API keys or passwords before pushing (the repo is public) | `/security-review` |

**Anthropic document skills** (availability depends on your Claude plan and settings. If they don't show up, Claude can still do the task, just less reliably)

| Skill | Use it for | Example |
|-------|-----------|---------|
| `docx` | Reading or editing the report and presenter script | "Use the docx skill to fix the heading numbering in the report" |
| `pptx` | Reading or editing the slides, speaker notes and animations | "Use the pptx skill to check every slide has a speaker tag" |
| `pdf` | Reading the guideline, lecture notes and papers in `course_materials/` and `reference_paper/` | "Find where the paper defines the high-rate regime" |
| `xlsx` | Opening Excel datasets (e.g. Damodaran's returns file) | "Convert the Damodaran xls to CSV in datasets/" |
| `dataviz` | Making charts readable on a projector: colours, labels, font sizes | "Make figure 3 readable on the big screen" |

**Golden rule:** the notebook is the only source of numbers and figures. If you change a number in the report or slides by hand, run **"Run the sync check"** so the other files are updated (or your edit is flagged).

## 11. Day-to-day workflow

1. **Get the latest changes** before you start: in the VS Code *Source Control* panel, click **⋯ → Pull**, or run `git pull`.
2. **Work on your own branch**, so you don't overwrite each other:
   ```bash
   git checkout -b <your-name>-<topic>      # e.g. ramona-step4-oos
   ```
3. Make your changes (with or without Claude).
4. Ask Claude: **"Run the sync check"**. Confirm the changes it lists.
5. Commit and push. In *Source Control*, write a message, click **Commit**, then **Sync / Publish Branch**.
6. Ask Claude **"Open a PR"**, or open one on GitHub. Tell the group chat.

**Word and PowerPoint files:** two people editing the same `.docx`/`.pptx` at the same time can't be merged automatically. Say in the group chat which file you're editing, and close Word/PowerPoint before pulling.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python3: command not found` (Windows) | Use `python`, or reinstall Python with "Add to PATH" ticked |
| Notebook can't find `fredapi` / `pandas` | Kernel isn't the `.venv` one. Use **Select Kernel** and pick `.venv` |
| `FileNotFoundError: credentials.yaml` | Do step 8 |
| Notebook can't find a file in `datasets/` | Do step 7 (team bundle) |
| Claude doesn't list the `qf600-*` skills | Open `QF600/Final Assignment` as the VS Code folder (or ask Claude about a file in it); pull the latest `main` |
| `git push` rejected | Run `git pull` first, then push again. Ask Chong Yee if you get a permissions error |
