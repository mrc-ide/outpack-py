import pytest
import os.path
from outpack.root import *
import outpack.config


def test_create_new_root(tmp_path):
    outpack_init(tmp_path)
    assert os.path.exists(tmp_path)
    assert os.path.exists(os.path.join(tmp_path, ".outpack"))
    root = root_open(tmp_path)
    assert type(root) == Root
    assert root.config == outpack.config.config_new("archive", False)


def test_error_if_root_not_present_when_opening(tmp_path):
    with pytest.raises(Exception) as e:
        root_open(str(tmp_path))
    assert e.match("'.+' does not look like an outpack root")


def test_error_if_root_not_present_when_locating(tmp_path):
    with pytest.raises(Exception) as e:
        root_locate(None)
    assert e.match("Did not find existing outpack root from directory '.'")


def test_locate_root_from_subdir(tmp_path):
    outpack_init(tmp_path)
    sub = tmp_path / "sub" / "directory"
    sub.mkdir(parents=True)
    a = root_locate(sub)
    b = root_open(str(tmp_path))
    assert a.path == b.path
    assert a.config == b.config


def test_no_double_initialisation(tmp_path):
    p = str(tmp_path)
    outpack_init(p)
    with pytest.raises(Exception) as e:
        outpack_init(p)
    assert e.match("outpack already initialised at '.+'")


def test_opening_root_object_returns_it(tmp_path):
    outpack_init(tmp_path)
    r = root_open(tmp_path)
    assert root_open(r) == r
    assert root_locate(r) == r
