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
    html_file = argv[2]
    if not path.exists(md_file):
        stderr.write('Missing {}\n'.format(md_file))
        exit(1)
    with open(md_file) as md_lines, open(html_file, 'w') as html:
        unordered_list_level = 0
        for line in md_lines:
            heading_level = 0
            # Heading h1 to h6 conversion
            if line.startswith('#'):
                heading_level += 1
                while line[heading_level] == '#':
                    heading_level += 1
                if line[heading_level] == ' ':
                    remaining_line = line[heading_level + 1:]
                    html.write(
                        '<h{0}>\n{1}</h{0}>\n'.format(heading_level,
                                                      remaining_line)
                    )
                else:
                    html.write(line)
            # Unordered list conversion
            elif line.startswith('- '):
                if unordered_list_level == 0:
                    unordered_list_level = 1
                    html.write('<ul>\n')
                html.write('<li>\n{}</li>\n'.format(line[2:]))
            elif not line.startswith('- ') and unordered_list_level == 1:
                unordered_list_level = 0
                html.write('</ul>\n')
            # Normal line
            else:
                html.write(line)
    if (unordered_list_level == 1):
        with open(html_file, 'a') as html:
            html.write('</ul>\n')
    exit(0)


if __name__ == "__main__":
    func()
