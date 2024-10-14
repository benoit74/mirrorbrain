#!/usr/bin/python

import os
import os.path
import sys

# python equivalent for this:
# find /srv/mirrors/openoffice -type f | head -n 1

# needs local file tree and knowledge of base dir


def find_first_file_in_tree(bdir):
    files = None
    for path, _, files in os.walk(bdir):
        if files:
            found = os.path.join(path, files[0])
            found = found[len(bdir) :]
            found = found.lstrip("/")
            return found
    return None


if __name__ == "__main__":
    bdir = sys.argv[1]
    print(find_first_file_in_tree(bdir))
