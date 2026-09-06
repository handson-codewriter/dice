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
