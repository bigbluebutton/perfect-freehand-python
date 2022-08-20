# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any

import pytest

# Using yaml to load "json" documents so I can have things like trailing commas
import yaml


@pytest.fixture(scope="module")
def shared_datadir(request: pytest.Item) -> Path:
    return Path(request.fspath).parent / "data"


@pytest.fixture
def datadir(request: pytest.Item) -> Path:
    return Path(request.fspath).with_suffix("")


@pytest.fixture(scope="module")
def input_json_all(shared_datadir: Path) -> Any:
    with open(shared_datadir / "inputs.json", "rb") as f:
        return yaml.safe_load(f)


@pytest.fixture
def input_json(input_json_all: Any, request: Any) -> Any:
    try:
        name = request.param
    except AttributeError:
        marker = request.node.get_closest_marker("input_json")
        if marker is None:
            name = request.node.name
        else:
            name = marker.args[0]

    return input_json_all[name]


@pytest.fixture
def output_json(datadir: Path, request: Any) -> Any:
    try:
        filename = request.param
    except AttributeError:
        filename = request.node.name

    with open(datadir / f"output_{filename}.json", "rb") as f:
        return yaml.safe_load(f)
