from __future__ import annotations

import argparse
import heapq
import os.path
import string
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Pair: TypeAlias = tuple[int, int]
Graph: TypeAlias = dict[Pair, list[Pair]]


def parse_input(s: str) -> tuple[list[str], Graph, Pair, Pair]:
    """
    Returns (grid, graph, start_point, goal_point)
    graph is represented as a dict mapping each point (x, y)
    to the list of points from which that point is accessible
    """
    grid = [line.strip() for line in s.splitlines()]
    graph: Graph = {}
    width, height = len(grid[0]), len(grid)
    start = goal = (0, 0)
    elevation = dict(zip(string.ascii_lowercase, range(26)))
    elevation.update({'S': elevation['a'], 'E': elevation['z']})
    for y in range(height):
        for x in range(width):
            graph[(x, y)] = []
            cell = grid[y][x]
            if cell == 'S':
                start = (x, y)
                continue
            if cell == 'E':
                goal = (x, y)
            for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if 0 <= nx < width and 0 <= ny < height:
                    if elevation[grid[ny][nx]] - elevation[cell] >= -1:
                        graph[(x, y)].append((nx, ny))
    return grid, graph, start, goal


def find_paths(graph: Graph, goal: tuple[int, int]) -> dict[Pair, int]:
    """
    Returns a dict mapping each point on the grid to the number of steps
    required to move from that point to the goal.
    """
    q = [(0, goal)]
    path_lengths = {goal: 0}
    while q:
        cost, current = heapq.heappop(q)
        for point in graph[current]:
            if point not in path_lengths or cost + 1 < path_lengths[point]:
                path_lengths[point] = cost + 1
                heapq.heappush(q, (cost + 1, point))
    return path_lengths


def compute(s: str) -> int:
    grid, graph, start, goal = parse_input(s)
    path_lengths = find_paths(graph, goal)
    return min(l for (x, y), l in path_lengths.items() if grid[y][x] in 'aS')


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
