import hashlib
import re

from dataclasses import dataclass, field


@dataclass
class Hash:
    algorithm: str
    digest: str

    def __str__(self):
        return f"{self.algorithm}:{self.digest}"


def hash_file(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    blocksize = 128 * h.block_size
    with open(path, "rb") as f:
        while chunk := f.read(blocksize):
            h.update(chunk)
    return Hash(algorithm, h.hexdigest())


def hash_string(data, algorithm):
    h = hashlib.new(algorithm)
    h.update(data.encode())
    digest = h.hexdigest()
    return Hash(algorithm, h.hexdigest())


def hash_parse(hash):
    if type(hash) == Hash:
        return hash
    return Hash(*hash.split(":"))


def hash_validate(path, expected):
    hash = hash_parse(expected)
    found = hash_file(path, hash.algorithm)
    if found != hash:
        raise Exception(f"Hash of '{path}' does not match:\n" +
                        f" - expected: {expected}\n" +
                        f" - found:    {found}")
