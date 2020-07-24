#!/usr/bin/python3
"""
A script that check the passed arguments.
"""
from sys import argv, exit, stderr
from os import path


def func():
    """Verify the passed args."""
    if len(argv) < 3:
        stderr.write('Usage: ./markdown2html.py README.md README.html\n')
        exit(1)
    md_file = argv[1]
    if not path.exists(md_file):
        stderr.write('Missing {}\n'.format(md_file))
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    func()
