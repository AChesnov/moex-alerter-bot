#!/usr/bin/env bash

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
FILES="$(git ls-files '*.py')"

function check_git_diff() {
    echo -e "${GREEN}Run ruff fix:${NC}"
    ruff check --fix ${FILES}

    echo -e "${GREEN}Run ruff format fix:${NC}"
    ruff format ${FILES}

    echo -e "${GREEN}Run mypy check:${NC}"
    mypy ${FILES}
}

check_git_diff