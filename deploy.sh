#!/bin/bash
#
# Deploy digital-menu-es (static HTML landing) from this Mac mini to the VPS.
#
# Same pipeline shape as iq-translate/deploy.sh: lock, state file, git pull,
# dirty-worktree guard, rsync, health check. No build step — the site is plain
# HTML + CSS with no JS, so the deploy is a flat rsync of the repo tree.
#
#   rsync ./  -> deployer@VPS:/home/deploy/apps/digital-menu-es
#   nginx serves it on :8080 (config: nginx/digital-menu-es.conf, installed
#   once — see README)
#   health: http://127.0.0.1:8080/ must answer 200
#
# Manual only:
#   bash deploy.sh        (FORCE=1 overrides the dirty-worktree guard)

set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Apple git, not Homebrew's (brew git has hung here before).
GIT=/usr/bin/git

# Repo = the directory this script lives in (works from any cwd).
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
[ -d "$REPO/.git" ] || { echo "deploy: repo not found at $REPO"; exit 1; }
VPS_HOST=46.225.143.221
VPS_USER=deployer
APP_DIR=/home/deploy/apps/digital-menu-es
HEALTH_URL=http://127.0.0.1:8080/

STATE=$HOME/Library/Logs/digital-menu-es.applied
LOCK=$HOME/Library/Logs/digital-menu-es.deploy.lock

# --- lock: two overlapping runs must not race ---
if ! mkdir "$LOCK" 2>/dev/null; then
    if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +30 2>/dev/null)" ]; then
        # stale lock (older than 30 min): steal it
        rmdir "$LOCK" 2>/dev/null && mkdir "$LOCK" 2>/dev/null \
            || { echo "deploy: another run in progress — exiting"; exit 0; }
    else
        echo "deploy: another run in progress — exiting"
        exit 0
    fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

cd "$REPO"

# git pull is not fatal: with no network we still deploy the local state.
if ! "$GIT" pull --ff-only; then
    echo "$(date '+%F %T') git pull failed — deploying local state"
fi
head=$("$GIT" rev-parse HEAD)

# State is the HEAD sha alone — static site, no .env to hash.
[ "$head" = "$(cat "$STATE" 2>/dev/null || true)" ] && exit 0

# Do not ship a half-edited tree; FORCE=1 overrides.
if [ "${FORCE:-}" != "1" ] && { ! "$GIT" diff --quiet || ! "$GIT" diff --cached --quiet; }; then
    echo "deploy: worktree dirty — skipping (FORCE=1 to deploy anyway)"
    exit 0
fi

echo "deploy: shipping static site to $VPS_USER@$VPS_HOST:$APP_DIR (commit ${head:0:8})"
rsync -az --delete \
    --exclude '.git' \
    --exclude 'deploy.sh' \
    --exclude 'nginx' \
    "$REPO/" "$VPS_USER@$VPS_HOST:$APP_DIR/"

code=$(ssh -o BatchMode=yes "$VPS_USER@$VPS_HOST" "curl -s -o /dev/null -w '%{http_code}' $HEALTH_URL" || true)
if [ "$code" = "200" ]; then
    echo "deploy: up — http://$VPS_HOST:8080/"
else
    echo "deploy: health check got '$code' — is nginx/digital-menu-es.conf installed?" >&2
    exit 1
fi

printf '%s\n' "$head" > "$STATE"
echo "deploy: done (${head:0:8})"
