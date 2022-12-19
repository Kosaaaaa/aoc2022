from __future__ import annotations

import argparse
import collections
import math
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

TIME_MINUTES = 32


class Blueprint(NamedTuple):
    id: int
    ore_bot_ore: int
    cla_bot_ore: int
    obs_bot_ore: int
    obs_bot_cla: int
    geo_bot_ore: int
    geo_bot_obs: int


def parse_blueprints(s: str) -> list[Blueprint]:
    blueprints = []
    for line in s.splitlines()[:3]:
        numbers = re.findall(r'\d+', line)
        blueprints.append(Blueprint(*[int(x) for x in numbers]))

    return blueprints


def compute_blueprint(blueprint: Blueprint, time_minutes: int) -> int:
    max_ore = max(
        blueprint.ore_bot_ore,
        blueprint.cla_bot_ore,
        blueprint.obs_bot_ore,
        blueprint.geo_bot_ore,
    )

    seen = set()
    best_at: dict[int, int] = {}
    todo = collections.deque([(0, 1, 0, 0, 0, 0, 0, 0, 0)])
    while todo:
        m, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo = todo.popleft()

        ore = min(max_ore * (time_minutes - m), ore)
        cla = min(blueprint.obs_bot_cla * (time_minutes - m), cla)
        obs = min(blueprint.geo_bot_obs * (time_minutes - m), obs)
        ore_b = min(ore_b, max_ore)
        cla_b = min(cla_b, blueprint.obs_bot_cla)
        obs_b = min(obs_b, blueprint.geo_bot_obs)

        tup = (m, ore_b, cla_b, obs_b, geo_b, ore, cla, obs, geo)
        if tup in seen:
            continue
        else:
            seen.add(tup)

        best_at[m] = max(best_at.get(m, 0), geo)

        if m == time_minutes:
            continue

        # always buy geode if possible
        if ore >= blueprint.geo_bot_ore and obs >= blueprint.geo_bot_obs:
            todo.append((
                m + 1,
                ore_b,
                cla_b,
                obs_b,
                geo_b + 1,
                ore + ore_b - blueprint.geo_bot_ore,
                cla + cla_b,
                obs + obs_b - blueprint.geo_bot_obs,
                geo + geo_b,
            ))
            continue

        # can buy obsidian?
        if ore >= blueprint.obs_bot_ore and cla >= blueprint.obs_bot_cla:
            todo.append((
                m + 1,
                ore_b,
                cla_b,
                obs_b + 1,
                geo_b,
                ore + ore_b - blueprint.obs_bot_ore,
                cla + cla_b - blueprint.obs_bot_cla,
                obs + obs_b,
                geo + geo_b,
            ))

        # can buy clay?
        if ore >= blueprint.cla_bot_ore:
            todo.append((
                m + 1,
                ore_b,
                cla_b + 1,
                obs_b,
                geo_b,
                ore + ore_b - blueprint.cla_bot_ore,
                cla + cla_b,
                obs + obs_b,
                geo + geo_b,
            ))

        # can buy ore?
        if ore >= blueprint.ore_bot_ore:
            todo.append((
                m + 1,
                ore_b + 1,
                cla_b,
                obs_b,
                geo_b,
                ore + ore_b - blueprint.ore_bot_ore,
                cla + cla_b,
                obs + obs_b,
                geo + geo_b,
            ))

        # buy nothing
        todo.append((
            m + 1,
            ore_b,
            cla_b,
            obs_b,
            geo_b,
            ore + ore_b,
            cla + cla_b,
            obs + obs_b,
            geo + geo_b,
        ))

    return best_at[time_minutes]


def compute(s: str) -> int:
    return math.prod([compute_blueprint(blueprint, TIME_MINUTES) for blueprint in parse_blueprints(s)])


INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''  # noqa: E501
EXPECTED = 56 * 62


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
