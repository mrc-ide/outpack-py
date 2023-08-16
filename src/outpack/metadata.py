from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from dataclasses_json import dataclass_json


@dataclass_json()
@dataclass
class PacketFile:
    path: str
    size: float
    hash: str  # noqa: A003


@dataclass_json()
@dataclass
class PacketDependsPath:
    here: str
    there: str


@dataclass_json()
@dataclass
class PacketDepends:
    packet: str
    query: str
    files: List[PacketDependsPath]


@dataclass_json
@dataclass
class GitInfo:
    sha: str
    branch: str
    url: List[str]


@dataclass_json()
@dataclass
class MetadataCore:
    id: str  # noqa: A003
    name: str
    parameters: Dict[str, Union[bool, int, float, str]]
    time: Dict[str, float]
    files: List[PacketFile]
    depends: List[PacketDepends]
    git: Optional[GitInfo]


@dataclass_json()
@dataclass
class PacketLocation:
    packet: str
    time: float
    hash: str  # noqa: A003


def read_metadata_core(path):
    with open(path) as f:
        return MetadataCore.from_json(f.read().strip())


def read_packet_location(path):
    with open(path) as f:
        return PacketLocation.from_json(f.read().strip())