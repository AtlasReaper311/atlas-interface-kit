#!/usr/bin/env bash
set -eu

# PART 1: Preconditions
command -v git >/dev/null
command -v gh >/dev/null
python3 scripts/check.py
python3 -m unittest discover -s tests -v
git diff --check

# PART 2: Create the approved repository
# This is a GitHub provider write. Run only while authenticated as AtlasReaper311.
gh repo create AtlasReaper311/atlas-interface-kit --public --description "Versioned browser interface foundations for Atlas Systems" --source . --remote origin --push

# PART 3: Establish the implementation branch
git switch -c feat/interface-kit-v0.1.0
git add .
git commit -m "feat: establish Atlas interface kit v0.1.0"
git push -u origin feat/interface-kit-v0.1.0

# PART 4: Open the review checkpoint
gh pr create --draft --base main --head feat/interface-kit-v0.1.0 --title "feat: establish Atlas interface kit v0.1.0" --body-file PR_BODY.md
