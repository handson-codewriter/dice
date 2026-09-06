import argparse
import random
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    print(rng.randint(1, 6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
