#!/bin/bash
# Usage: ./check_build.sh [repo_name]
# If no repo name is provided, it defaults to 'Syllabus'

REPO=${1:-Syllabus}
OWNER="petemits"

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}⏳ Monitoring GitHub Pages build for ${OWNER}/${REPO}...${NC}"

# Function to draw a progress bar
draw_bar() {
    local percent=$1
    local status_text=$2
    local filled=$((percent / 2)) # 50 characters total width
    local empty=$((50 - filled))
    
    printf "\r["
    for ((i=0; i<filled; i++)); do printf "█"; done
    for ((i=0; i<empty; i++)); do printf "░"; done
    printf "] %3d%% - %s" "$percent" "$status_text"
}

# Loop to poll status every 2 seconds
while true; do
    # Fetch status and error message from GitHub API
    STATUS_JSON=$(gh api repos/$OWNER/$REPO/pages/builds/latest 2>/dev/null)
    
    if [ -z "$STATUS_JSON" ]; then
        draw_bar 10 "Initializing/Queued..."
        sleep 2
        continue
    fi

    STATUS=$(echo "$STATUS_JSON" | jq -r '.status')
    ERROR_MSG=$(echo "$STATUS_JSON" | jq -r '.error.message // ""')

    case $STATUS in
        "queued")
            draw_bar 15 "Queued (Waiting for runner)..."
            ;;
        "building")
            draw_bar 50 "Building (Processing your site)..."
            ;;
        "built")
            draw_bar 100 "Built Successfully! Site is Live."
            echo -e "\n\n${GREEN}✅ Build Complete!${NC}"
            echo -e "Your site is live at: ${BLUE}https://${OWNER}.github.io/${REPO}/${NC}"
            break
            ;;
        "errored")
            draw_bar 100 "Build Failed."
            echo -e "\n\n${RED}❌ Build Error:${NC} $ERROR_MSG"
            echo "Try triggering a new build: gh api --method POST repos/$OWNER/$REPO/pages/builds"
            break
            ;;
        *)
            draw_bar 10 "Unknown Status ($STATUS)..."
            ;;
    esac
    
    sleep 2
done
echo "" # Add a new line at the end
