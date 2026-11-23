#!/usr/bin/env python3
"""THE HORIZON — entrypoint for the news-image-20261123 entry.

The grader runs this file as `python3 -P -s /bot/main.py` with no
arguments, on a read-only filesystem, and expects the program to
write the day's image to /output/entry.png. The front page itself
is drawn by render.py, with the day's stories in news.py; this
entrypoint renders that page to the grader's output path.

    python3 main.py            # writes /output/entry.png
                               # (or $MAKEFUN_OUTPUT_DIR/entry.png)

Pure Python standard library, no network, deterministic.
"""

import os
import sys

# The grader's -P flag keeps this file's directory off sys.path,
# so put it back before importing the page renderer.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    render.render(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
