from __future__ import annotations

import argparse
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

reg = re.compile(
    r'^Sensor at x=(-?\d+), y=(-?\d+): '
    r'closest beacon is at x=(-?\d+), y=(-?\d+)$',
)


class Sensor(NamedTuple):
    x: int
    y: int
    beacon_x: int
    beacon_y: int

    @property
    def distance(self) -> int:
        return abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

    def c_dist(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)


def compute(s: str, m: int = 4000000) -> int:
    beacons = set()

    sensors = []
    for line in s.splitlines():
        match = reg.match(line)
        assert match is not None
        sensor = Sensor(
            int(match[1]), int(match[2]),
            int(match[3]), int(match[4]),
        )
        sensors.append(sensor)
        beacons.add((sensor.beacon_x, sensor.beacon_y))

    for sensor in sensors:
        top_y = sensor.y + sensor.distance - 1
        bottom_y = sensor.y - sensor.distance - 1

        for i in range(sensor.distance):
            for x, y in (
                    (sensor.x + i, top_y - i),
                    (sensor.x - i, top_y - i),
                    (sensor.x + i, bottom_y + i),
                    (sensor.x - i, bottom_y + i),
            ):
                if x < 0 or y < 0 or x > m or y > m:
                    continue
                elif (x, y) in beacons:
                    continue

                for sensor_2 in sensors:
                    if sensor_2.c_dist(x, y) <= sensor_2.distance:
                        break
                else:
                    return x * 4000000 + y

    raise AssertionError('unreachable')


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, m=20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
