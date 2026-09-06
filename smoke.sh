#!/usr/bin/env bash
set -euo pipefail

output=$(python3 dice.py)

if ! [[ "$output" =~ ^[1-6]$ ]]; then
    echo "smoke: onverwachte output '$output'" >&2
    exit 1
fi

echo "smoke: ok ($output)"
