import json
import pytest

from outpack.config import *


def test_create_empty_config():
    cfg = config_new("archive", False)
    assert type(cfg) == Config
    assert cfg.schema_version == outpack_schema_version()
    assert cfg.core.path_archive == "archive"
    assert not cfg.core.use_file_store
    assert cfg.core.hash_algorithm == "sha256"
    assert cfg.location == {}


def test_must_use_some_storage():
    with pytest.raises(Exception) as e:
        config_new(None, False)
    assert e.match("invalid path_archive")


def test_can_serialise_config():
    cfg = config_new("archive", True)
    s = config_serialise(cfg)
    assert type(s) == str
    assert Config.from_json(s) == cfg


def test_can_serialise_locations_as_list():
    cfg = config_new("archive", True)
    cfg.location["src"] = Location("src", "file", "/path/to/file")
    s = config_serialise(cfg)
    d = json.loads(s)
    assert type(d["location"]) == list
    assert d["location"][0] == \
        {"name": "src", "type": "file", "path": "/path/to/file"}
    assert Config.from_json(s) == cfg
