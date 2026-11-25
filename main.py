"""Ship the finished newspaper image to the grading harness.

The entry image is rendered beforehand and committed next to this
script as entry.png. All this program does is place a copy of it at
/output/entry.png, which is where the grader looks for the final
artefact. Pure standard library, no third-party packages.
"""

import hashlib
import os
import shutil


def entry_file():
    """Absolute path of the entry image shipped with this repo."""
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, "entry.png")


def file_md5(path):
    """Hex digest of a file, read in chunks."""
    digest = hashlib.md5()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ship():
    """Copy the entry image to /output/entry.png and report the result."""
    src = entry_file()
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py: " + src)
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    shutil.copyfile(src, dst)
    if file_md5(src) != file_md5(dst):
        raise SystemExit("copy mismatch: " + dst)
    size = os.path.getsize(dst)
    print("wrote %s (%d bytes, md5 %s)" % (dst, size, file_md5(dst)))
    return dst


if __name__ == "__main__":
    ship()
