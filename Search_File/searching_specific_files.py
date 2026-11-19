"""Print matching file paths beneath a directory."""

import fnmatch
import os

DEFAULT_ROOT = "/home/tuts/Documents"
DEFAULT_PATTERN = "*.mp4"


def search_files(root_path, pattern=DEFAULT_PATTERN):
    """Yield paths matching *pattern* while walking *root_path* top-down."""
    for current_root, _directories, filenames in os.walk(root_path):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(current_root, filename)


def main():
    for path in search_files(DEFAULT_ROOT):
        print(path)


if __name__ == "__main__":
    main()
