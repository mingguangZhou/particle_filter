# MIT License
#
# Copyright (c) 2026 Charlie Song
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Clock-source contracts for simulator and onboard localization launches."""

import ast
from pathlib import Path

import yaml


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _literal_use_sim_time_values(relative_path):
    tree = ast.parse(
        (PACKAGE_ROOT / relative_path).read_text(encoding='utf-8')
    )
    values = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if (
                isinstance(key, ast.Constant) and
                key.value == 'use_sim_time' and
                isinstance(value, ast.Constant) and
                isinstance(value.value, bool)
            ):
                values.append(value.value)
    return values


def _configured_use_sim_time(relative_path):
    config = yaml.safe_load(
        (PACKAGE_ROOT / relative_path).read_text(encoding='utf-8')
    )
    return config['particle_filter']['ros__parameters']['use_sim_time']


def test_onboard_localization_uses_wall_clock_everywhere():
    assert _configured_use_sim_time('config/localize.yaml') is False
    assert _literal_use_sim_time_values('launch/localize_launch.py') == [
        False,
        False,
    ]
    assert _literal_use_sim_time_values(
        'launch/localize_onboard_rviz_launch.py'
    ) == [False]


def test_sim_localization_uses_simulator_clock_everywhere():
    assert _configured_use_sim_time('config/localize_sim.yaml') is True
    assert _literal_use_sim_time_values('launch/localize_sim_launch.py') == [
        True,
        True,
    ]
