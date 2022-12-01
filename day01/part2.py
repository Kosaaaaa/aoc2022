from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    current_elf_calories = 0
    all_elfs_calories = []
    for line in lines:
        if not line:
            all_elfs_calories.append(current_elf_calories)
            current_elf_calories = 0
        else:
            current_elf_calories += int(line)
    if current_elf_calories:
        all_elfs_calories.append(current_elf_calories)

    return sum(list(sorted(all_elfs_calories, reverse=True))[:3])


INPUT_S = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
EXPECTED = 45000


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
