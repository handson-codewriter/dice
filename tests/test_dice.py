import subprocess
import sys


def test_single_roll_range():
    result = subprocess.run(
        [sys.executable, "dice.py"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    value = int(output)
    assert 1 <= value <= 6


def test_seed_is_deterministic():
    first = subprocess.run(
        [sys.executable, "dice.py", "--seed", "42"],
        capture_output=True,
        text=True,
        check=False,
    )
    second = subprocess.run(
        [sys.executable, "dice.py", "--seed", "42"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert first.returncode == 0
    assert second.returncode == 0
    assert first.stdout == second.stdout


def test_multiple_dice_and_sum():
    result = subprocess.run(
        [sys.executable, "dice.py", "-n", "3", "--seed", "42"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 2
    rolls = lines[0].split(" ")
    assert len(rolls) == 3
    for roll in rolls:
        value = int(roll)
        assert 1 <= value <= 6
    assert lines[1] == f"som={sum(int(r) for r in rolls)}"

    bad = subprocess.run(
        [sys.executable, "dice.py", "-n", "0"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert bad.returncode == 2
    assert bad.stderr.strip() != ""

    negative = subprocess.run(
        [sys.executable, "dice.py", "-n", "-1"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert negative.returncode == 2
    assert negative.stderr.strip() != ""


def test_n_and_stats_are_mutually_exclusive():
    result = subprocess.run(
        [sys.executable, "dice.py", "-n", "3", "--stats", "60"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert result.stderr.strip() != ""
    assert result.stdout.strip() == ""


def test_stats_distribution():
    result = subprocess.run(
        [sys.executable, "dice.py", "--stats", "600"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert len(lines) == 6
    counts = {}
    for line in lines:
        value, count = line.split(":")
        counts[int(value)] = int(count)
    assert sorted(counts.keys()) == [1, 2, 3, 4, 5, 6]
    for value in range(1, 7):
        assert 60 <= counts[value] <= 140
