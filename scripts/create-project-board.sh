#!/usr/bin/env bash
# Creates the Phase 1 Projects v2 board and adds every open sprint-1 / sprint-2 issue.
#
# Requires the `project` scope, which the default gh login does not include:
#     gh auth refresh -s project
#
# Idempotent-ish: re-running creates a SECOND board. Check `gh project list` first.
set -euo pipefail

OWNER="${OWNER:-DeemanthPoonacha}"
REPO="${REPO:-DeemanthPoonacha/delegate}"
TITLE="${TITLE:-Delegate — Phase 1}"

if ! gh auth status 2>&1 | grep -q "'project'"; then
  echo "Missing the 'project' scope. Run:  gh auth refresh -s project" >&2
  exit 1
fi

echo "Creating board: $TITLE"
NUM=$(gh project create --owner "$OWNER" --title "$TITLE" --format json --jq '.number')
echo "Board #$NUM"

echo "Adding fields"
gh project field-create "$NUM" --owner "$OWNER" --name "Sprint" \
  --data-type SINGLE_SELECT --single-select-options "S1,S2" >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Role" \
  --data-type SINGLE_SELECT --single-select-options "be,mob,ops" >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Estimate (days)" \
  --data-type NUMBER >/dev/null

echo "Adding issues"
count=0
for label in sprint-1 sprint-2; do
  while read -r url; do
    [ -z "$url" ] && continue
    gh project item-add "$NUM" --owner "$OWNER" --url "$url" >/dev/null
    count=$((count + 1))
    printf '.'
  done < <(gh issue list --repo "$REPO" --label "$label" --state open --limit 100 --json url --jq '.[].url')
done
echo
echo "Added $count issues to board #$NUM"
gh project view "$NUM" --owner "$OWNER" --web 2>/dev/null || \
  echo "Board: https://github.com/users/$OWNER/projects/$NUM"
