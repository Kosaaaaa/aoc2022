from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)
    visible = set()

    y_min, x_min = min(coords)
    y_max, x_max = max(coords)

    for y in range(y_min, y_max + 1):
        # down
        val = coords[(y, x_min)]
        visible.add((y, x_min))
        for x in range(x_min + 1, x_max + 1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

        # up
        val = coords[(y, x_max)]
        visible.add((y, x_max))
        for x in range(x_max, -1, -1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

    for x in range(x_min, x_max + 1):
        # right
        val = coords[(y_min, x)]
        visible.add((y_min, x))
        for y in range(y_min + 1, y_max + 1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

        # left
        val = coords[(y_max, x)]
        visible.add((y_max, x))
        for y in range(y_max, -1, -1):
            cand = (y, x)
            if coords[cand] > val:
                visible.add(cand)
                val = coords[cand]

    return len(visible)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
