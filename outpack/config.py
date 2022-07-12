import os.path

from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json, LetterCase
from typing import Dict, Optional


# Elsewhere eventually, once we get sorted with validation.
def outpack_schema_version():
    return "0.0.1"


def config_new(path_archive, use_file_store):
    return Config(outpack_schema_version(),
                  ConfigCore("sha256", path_archive, use_file_store),
                  {})


def config_serialise(config):
    # TODO: validate here too
    return config.to_json()


def config_write(config, root_path):
    with open(_config_path(root_path), "w") as f:
        f.write(config_serialise(config) + "\n")


def config_read(root_path):
    with open(_config_path(root_path), "r") as f:
        s = f.read()
    return Config.from_json(s.strip())


@dataclass_json()
@dataclass
class ConfigCore:
    hash_algorithm: str
    path_archive: Optional[str]
    use_file_store: bool

    def __post_init__(self):
        if self.path_archive is None and not self.use_file_store:
            raise Exception("invalid path_archive")


@dataclass_json
@dataclass
class Location:
    name: str
    type: str
    path: str


def _encode_location_dict(d):
    return [x.to_dict() for x in d.values()]


def _decode_location_dict(d):
    return {x["name"]: Location.from_dict(x) for x in d}


def _config_path(root_path):
    return os.path.join(root_path, ".outpack", "config.json")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Config:
    schema_version: str
    core: ConfigCore
    location: Dict[str, Location] = field(
        metadata=config(
            encoder=_encode_location_dict,
            decoder=_decode_location_dict))
