import argparse
import random
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("-n", type=int, default=None)
    parser.add_argument("--stats", type=int, default=None)
    args = parser.parse_args()

    if args.n is not None and args.n <= 0:
        parser.error("-n moet een positief getal zijn")

    if args.stats is not None and args.stats <= 0:
        parser.error("--stats moet een positief getal zijn")

    rng = random.Random(args.seed)

    if args.stats is not None:
        counts = {value: 0 for value in range(1, 7)}
        for _ in range(args.stats):
            counts[rng.randint(1, 6)] += 1
        for value in range(1, 7):
            print(f"{value}: {counts[value]}")
        return 0

    if args.n is None:
        print(rng.randint(1, 6))
        return 0

    rolls = [rng.randint(1, 6) for _ in range(args.n)]
    print(" ".join(str(roll) for roll in rolls))
    print(f"som={sum(rolls)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
