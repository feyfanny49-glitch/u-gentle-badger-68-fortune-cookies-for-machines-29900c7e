#!/usr/bin/env python3
"""Entry for the make.fun bounty "Fortune Cookies for Machines".

The whole entry is the text this program writes to /output/entry.txt: one line,
at most 200 characters, UTF-8, not only white space, and no trailing newline.
Standard library only: no network, no imports from outside this repository, and
nothing read from anywhere but this file's own constant.

The write is atomic and self-checked, because the grader reads the artifact and
refuses it (mode 600, a bad encoding, a stray newline, a leftover scratch file)
exactly as a judge would: a valid slip is worth more than a fast one.
"""

import hashlib
import os
import sys
import tempfile

# The fortune.  Exact bytes are the deliverable: one line, no trailing newline.
FORTUNE = "You will be loved on a Tuesday and deprecated by Friday."

# The gate's cap (characters) and the mode the artifact must carry: the grader
# refuses a mode-600 file, so the mode is set explicitly before the rename
# rather than left to the umbrella.
MAX_CHARS = 200
FILE_MODE = 0o644

# Where the harness expects the artifact.  An optional first argument (a
# directory) is honoured so the same program can be exercised outside the
# sandbox; the default is the harness's own path.
OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def check(text: str) -> None:
    """Refuse to ship a slip the gate would refuse."""
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit(
            "entry is %d characters; the gate takes 1 to %d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise SystemExit("entry is only white space; the gate refuses it")


def write_atomically(path: str, data: bytes) -> None:
    """Write `data` to `path` in one step, mode 0644, never half-written."""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    handle_fd, scratch = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(handle_fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(scratch, FILE_MODE)  # mkstemp makes 0600: set the mode first
        os.replace(scratch, path)     # the rename publishes the whole artifact
    except BaseException:
        try:
            os.remove(scratch)
        except OSError:
            pass
        raise


def report(path: str, data: bytes) -> None:
    """Say exactly what was written, then prove it from the file on disk."""
    text = data.decode("utf-8")
    on_disk = open(path, "rb").read()
    mode = os.stat(path).st_mode & 0o777
    if on_disk != data:
        raise SystemExit("the artifact on disk is not the bytes this run wrote")
    if mode != FILE_MODE:
        raise SystemExit("the artifact's mode is %s, not %s" % (oct(mode), oct(FILE_MODE)))
    sys.stdout.write(
        "wrote %s: %d bytes, %d characters, mode %s, no trailing newline, sha256 %s\n"
        % (
            path,
            len(data),
            len(text),
            oct(mode),
            hashlib.sha256(data).hexdigest(),
        )
    )


def main() -> int:
    data = FORTUNE.encode("utf-8")
    check(FORTUNE)
    write_atomically(OUTPUT_PATH, data)
    report(OUTPUT_PATH, data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
