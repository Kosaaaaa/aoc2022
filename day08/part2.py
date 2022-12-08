from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)

    y_min, x_min = min(coords)
    y_max, x_max = max(coords)

    val = -1

    def coords_compute(x: int, y: int) -> int:
        n = coords[(y, x)]

        up = 0
        for cand_y in range(y - 1, y_min - 1, -1):
            up += 1
            if coords[(cand_y, x)] >= n:
                break

        down = 0
        for cand_y in range(y + 1, y_max + 1):
            down += 1
            if coords[(cand_y, x)] >= n:
                break

        left = 0
        for cand_x in range(x - 1, x_min - 1, -1):
            left += 1
            if coords[(y, cand_x)] >= n:
                break

        right = 0
        for cand_x in range(x + 1, x_max + 1):
            right += 1
            if coords[(y, cand_x)] >= n:
                break

        return up * down * left * right

    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            val = max(coords_compute(x, y), val)

    return val


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
