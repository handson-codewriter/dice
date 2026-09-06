#!/usr/bin/env bash
set -euo pipefail

output=$(python3 dice.py)

if ! [[ "$output" =~ ^[1-6]$ ]]; then
    echo "smoke: onverwachte output '$output'" >&2
    exit 1
fi

echo "smoke: ok ($output)"

output_n=$(python3 dice.py -n 2)
mapfile -t lines_n <<< "$output_n"

if [[ ${#lines_n[@]} -ne 2 ]]; then
    echo "smoke: onverwacht aantal regels in '$output_n'" >&2
    exit 1
fi

if ! [[ "${lines_n[0]}" =~ ^[1-6]\ [1-6]$ ]]; then
    echo "smoke: onverwachte worp-regel '${lines_n[0]}'" >&2
    exit 1
fi

if ! [[ "${lines_n[1]}" =~ ^som=[0-9]+$ ]]; then
    echo "smoke: onverwachte som-regel '${lines_n[1]}'" >&2
    exit 1
fi

echo "smoke: ok (-n 2: ${lines_n[0]} / ${lines_n[1]})"

output_stats=$(python3 dice.py --stats 60)
mapfile -t lines_stats <<< "$output_stats"

if [[ ${#lines_stats[@]} -ne 6 ]]; then
    echo "smoke: onverwacht aantal regels in '$output_stats'" >&2
    exit 1
fi

total=0
for value in 1 2 3 4 5 6; do
    line="${lines_stats[$((value - 1))]}"
    if ! [[ "$line" =~ ^${value}:\ [0-9]+$ ]]; then
        echo "smoke: onverwachte stats-regel '$line'" >&2
        exit 1
    fi
    count="${line#*: }"
    total=$((total + count))
done

if [[ "$total" -ne 60 ]]; then
    echo "smoke: som van tellingen ($total) is niet 60" >&2
    exit 1
fi

echo "smoke: ok (--stats 60, totaal=$total)"
