from __future__ import annotations

import argparse
import curses
import enum
import os.path
from unittest import mock

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Face(enum.Enum):
    TOP = enum.auto()
    BACK = enum.auto()
    LEFT = enum.auto()
    FRONT = enum.auto()
    RIGHT = enum.auto()
    BOTTOM = enum.auto()


def ccw_pt(x: int, y: int, *, size: int) -> tuple[int, int]:
    return y, size - x - 1


def ccw(coords: set[tuple[int, int]], *, size: int) -> set[tuple[int, int]]:
    return {ccw_pt(x, y, size=size) for (x, y) in coords}


def cw(coords: set[tuple[int, int]], *, size: int) -> set[tuple[int, int]]:
    return ccw(ccw(ccw(coords, size=size), size=size), size=size)


def compute(s: str) -> int:
    parts = s.split('\n\n')




    grid = parts[0].split('\n')
    cmd = parts[1]


    width = max([len(line) for line in grid])
    height = len(grid)
    grid = [' ' + line.ljust(width) + ' ' for line in grid]
    width += 2
    height += 2
    grid = [' ' * width] + grid + [' ' * width]

    ins_list = []
    buffer = ''
    for c in cmd.strip('\n'):
        if c in 'LR':
            if buffer != '':
                ins_list += [int(buffer)]
                buffer = ''
            ins_list += [c]
        else:
            buffer += c

    if buffer != '':
        ins_list += [int(buffer)]

    x = y = 1
    dir_lookup = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for j in range(width):
        if grid[1][j] == '.':
            y = j
            break
    dir_cache = x, y

    face_size = round(pow(sum([c != ' ' for line in grid for c in line]) // 6, 0.5))

    Q = [dir_cache]
    visited = {dir_cache: [None] * 4}
    while len(Q) > 0:
        # print(Q)
        v, *Q = Q
        x, y = v
        for direction in range(4):
            i, j = dir_lookup[direction]
            i, j = x + i * face_size, y + j * face_size
            if not (0 <= i < height and 0 <= j < width):
                continue
            if grid[i][j] == ' ':
                continue
            w = (i, j)
            if w not in visited:
                visited[v][direction] = w
                w_list = [None] * 4
                w_list[(direction + 2) % 4] = v
                visited[w] = w_list
                Q += [w]

    faces = {}
    for i, j in visited:
        faces[(i // face_size, j // face_size)] = [((v[0] // face_size, v[1] // face_size) if v is not None else v) for
                                                   v in
                                                   visited[(i, j)]]

    while sum([edge is None for key in faces for edge in faces[key]]) > 0:
        for face in faces:
            for direction in range(4):
                if faces[face][direction] is None:
                    for delta in -1, 1:
                        common_face = faces[face][(direction + delta) % 4]
                        if common_face is None:
                            continue
                        common_face_edge = faces[common_face].index(face)
                        missing_face = faces[common_face][(common_face_edge + delta) % 4]
                        if missing_face is None:
                            continue
                        missing_face_edge = faces[missing_face].index(common_face)
                        faces[missing_face][(missing_face_edge + delta) % 4] = face
                        faces[face][direction] = missing_face
                        break

    x, y = dir_cache
    direction = 0
    edge_top_offset_out = [[1, 1], [1, face_size], [face_size, face_size], [face_size, 1]]
    for step in ins_list:
        if step == 'R':
            direction = (direction + 1) % 4
        elif step == 'L':
            direction = (direction - 1) % 4
        else:
            dx, dy = dir_lookup[direction]
            new_dir = direction
            for i in range(step):
                nx, ny = x + dx, y + dy
                if grid[nx][ny] == ' ':
                    # compute current edge prop
                    cur_face = (x - 1) // face_size, (y - 1) // face_size
                    cur_offset = 0
                    while tuple([
                        a * face_size + b + c * cur_offset for a, b, c in
                        zip(
                            cur_face, edge_top_offset_out[(direction + 1) % 4],
                            dir_lookup[(direction + 1) % 4],
                        )
                    ]) != (x, y):
                        cur_offset += 1
                    # Compute next edge prop
                    next_face = faces[cur_face][direction]
                    new_dir = (faces[next_face].index(cur_face) + 2) % 4
                    nx, ny = tuple([
                        a * face_size + b + c * cur_offset for a, b, c in
                        zip(next_face, edge_top_offset_out[new_dir], dir_lookup[(new_dir + 1) % 4])
                    ])
                if grid[nx][ny] == '#':
                    break
                else:
                    x, y = nx, ny
                    direction = new_dir
                    dx, dy = dir_lookup[direction]

    return x * 1000 + y * 4 + direction


INPUT_S = '''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
'''
EXPECTED = 5031


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    with mock.patch.object(
            curses,
            'wrapper',
            lambda fn, *args, **kwargs: fn(mock.Mock(), *args, **kwargs),
    ):
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
