"""Deliver the finished newspaper image to the grader.

The image is rendered ahead of time and committed beside this script
as entry.png. This program only moves a copy of it into the output
directory the grader reads from, then prints a short summary so the
run log shows what was shipped. Standard library only.
"""

import hashlib
import os
import shutil
import sys


def repo_dir():
    return os.path.dirname(os.path.abspath(__file__))


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    src = os.path.join(repo_dir(), "entry.png")
    if not os.path.isfile(src):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    dst_dir = output_dir()
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Verify the copy landed intact before reporting success.
    if digest(dst) != digest(src):
        print("copy mismatch: %s differs from %s" % (dst, src), file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    print("shipped %s (%d bytes, md5 %s)" % (dst, size, digest(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
