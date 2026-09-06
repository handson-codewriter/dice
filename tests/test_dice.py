import subprocess
import sys


def test_single_roll_range():
    result = subprocess.run(
        [sys.executable, "dice.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    output = result.stdout.strip()
    value = int(output)
    assert 1 <= value <= 6
