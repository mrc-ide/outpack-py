import os
import shutil
from typing import Dict, List

from outpack.location import LocationDriver
from outpack.metadata import MetadataCore, PacketFile, PacketLocation
from outpack.root import find_file_by_hash, root_open
from outpack.static import LOCATION_LOCAL
from outpack.util import read_string


class OutpackLocationPath(LocationDriver):
    def __init__(self, path):
        self.__root = root_open(path, locate=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass

    def list(self) -> Dict[str, PacketLocation]:
        return self.__root.index.location(LOCATION_LOCAL)

    def metadata(self, packet_ids: List[str]) -> Dict[str, str]:
        all_ids = self.__root.index.location(LOCATION_LOCAL).keys()
        missing_ids = set(packet_ids).difference(all_ids)
        if missing_ids:
            missing_msg = "', '".join(missing_ids)
            msg = f"Some packet ids not found: '{missing_msg}'"
            raise Exception(msg)
        ret = {}
        for packet_id in packet_ids:
            path = self.__root.path / ".outpack" / "metadata" / packet_id
            ret[packet_id] = read_string(path)
        return ret

    def fetch_file(self, _packet: MetadataCore, file: PacketFile, dest: str):
        if self.__root.config.core.use_file_store:
            path = self.__root.files.filename(file.hash)
            if not os.path.exists(path):
                msg = f"Hash '{file.hash}' not found at location"
                raise Exception(msg)
        else:
            path = find_file_by_hash(self.__root, file.hash)
            if path is None:
                msg = f"Hash '{file.hash}' not found at location"
                raise Exception(msg)
        shutil.copyfile(path, dest)
