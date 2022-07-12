import os
import os.path

from .config import config_new, config_read, config_write
from .util import find_file_descend


def outpack_init(root, path_archive="archive", use_file_store=False):
    path_outpack = os.path.join(root, ".outpack")
    if os.path.exists(path_outpack):
        raise Exception(f"outpack already initialised at '{root}'")

    config = config_new(path_archive, use_file_store)
    os.makedirs(path_outpack)
    os.makedirs(os.path.join(path_outpack, "metadata"))
    os.makedirs(os.path.join(path_outpack, "location"))
    config_write(config, root)


def root_open(path):
    if type(path) == Root:
        return path
    if not os.path.exists(os.path.join(path, ".outpack")):
        raise Exception(f"'{path}' does not look like an outpack root")
    return Root(path)


def root_locate(path):
    if type(path) == Root:
        return path
    if path is None:
        path = "."
    path_found = find_file_descend(".outpack", path)
    if path_found is None:
        raise Exception("Did not find existing outpack root from " +
                        f"directory '{path}'")
    return Root(path_found)


class Root:
    def __init__(self, path):
        self.path = path
        self.config = config_read(path)
