#!/usr/bin/python3
"""
A script that converts Markdown to HTML.
"""

import sys
import os
import re

def convert_markdown_to_html(input_file, output_file):
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    # check that the Markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    in_list = False

    with open(input_file, encoding="utf-8") as f:
        html_lines = []
        for line in f:
            # check for Markdown headings
            match_heading = re.match(r"^(#+) (.*)$", line)
            if match_heading:
                heading_level = len(match_heading.group(1))
                heading_text = match_heading.group(2)
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
                continue

            # check for unordered list items
            match_list_item = re.match(r"^- (.*)$", line)
            if match_list_item:
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                list_item_text = match_list_item.group(1)
                html_lines.append(f"    <li>{list_item_text}</li>")
            else:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                # for lines that don't match any patterns, just add them directly
                elif line.strip():  # ignore empty lines
                    html_lines.append(line.rstrip())

        if in_list:  
            html_lines.append("</ul>")

    # write the HTML output to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

if __name__ == "__main__":
    # check that the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    # get the input and output file names from the command-line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # convert the Markdown file to HTML and write the output to a file
    convert_markdown_to_html(input_file, output_file)

    sys.exit(0)