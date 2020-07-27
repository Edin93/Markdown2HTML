#!/usr/bin/python3
"""
A script that check the passed arguments.
"""
from os import path
import re
from sys import argv, exit, stderr


def contains_bold(line):
    '''Checks if line contains the markdown bold element.'''
    return '**' in line


def contains_em(line):
    '''Checks if line contains the markdown em element.'''
    return '__' in line


def markdown_to_html():
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
        ordered_list_level = 0
        paragraph_level = 0
        for line in md_lines:
            heading_level = 0
            # inline elements conversion
            # Bold text conversion
            if contains_bold(line):
                bold_level = 0
                i = 0
                while i < len(line):
                    if line[i: i + 2] == '**':
                        if bold_level == 0:
                            bold_level = 1
                            line = line[0: i] + '<b>' + line[i + 2:]
                            i += 2
                        else:
                            bold_level = 0
                            line = line[0: i] + '</b>' + line[i + 2:]
                            i += 2
                    else:
                        i += 1
            # Em text conversion
            if contains_em(line):
                em_level = 0
                i = 0
                while i < len(line):
                    if line[i: i + 2] == '__':
                        if em_level == 0:
                            em_level = 1
                            line = line[0: i] + '<em>' + line[i + 2:]
                            i += 2
                        else:
                            em_level = 0
                            line = line[0: i] + '</em>' + line[i + 2:]
                            i += 2
                    else:
                        i += 1
            # Block elements conversion
            # Heading h1 to h6 conversion
            if line.startswith('#'):
                if paragraph_level == 1:
                    paragraph_level = 0 and html.write('</p>\n')
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
                if paragraph_level == 1:
                    paragraph_level = 0 and html.write('</p>\n')
                if unordered_list_level == 0:
                    unordered_list_level = 1
                    html.write('<ul>\n')
                html.write('<li>\n{}</li>\n'.format(line[2:]))
            # Ordered list conversion
            elif line.startswith('* '):
                if paragraph_level == 1:
                    paragraph_level = 0 and html.write('</p>\n')
                if ordered_list_level == 0:
                    ordered_list_level = 1
                    html.write('<ol>\n')
                html.write('<li>\n{}</li>\n'.format(line[2:]))
            else:
                space_free_line = line.replace(' ', '')
                if unordered_list_level == 1:
                    unordered_list_level = 0
                    html.write('</ul>\n')
                elif ordered_list_level == 1:
                    ordered_list_level = 0
                    html.write('</ol>\n')
                if space_free_line != '\n':
                    if paragraph_level == 0:
                        paragraph_level = 1
                        html.write('<p>\n')
                    else:
                        html.write('<br />\n')
                    html.write(line)
                elif space_free_line == '\n':
                    if paragraph_level == 1:
                        paragraph_level = 0
                        html.write('</p>\n')

    with open(html_file, 'a') as html:
        if (unordered_list_level == 1):
            html.write('</ul>\n')
        elif (ordered_list_level == 1):
            html.write('</ol>\n')
        elif (paragraph_level == 1):
            html.write('</p>\n')
    exit(0)


if __name__ == "__main__":
    markdown_to_html()
