#!/usr/bin/env python3

import itertools
from pathlib import Path
from pprint import pprint
from collections import defaultdict


def find_last_list_occurance(mylist, value):
    """Find last occurance of `value` within list if no other chars are behind it.

    Example:
        >>> find_last_list_occurance(['002', '|', '+--', '|', '|'], value='+--')
        3
        >>> find_last_list_occurance(['002', '|', '+--', '|', '|', '010'], value='+--')
        len(list) == 6
    """
    try:
        idx = len(mylist) - mylist[-1::-1].index(value) - 1
        if any(item == '' for item in mylist[idx:]):
            return len(mylist)
        return idx
    except ValueError:
        return None


def add(t, path):
    for node in path:
        t = t[node]


def make_tree_dict(t):
    return {k: make_tree_dict(t[k]) for k in t}


def tprint(tree, prefix='', file='./result.txt'):
    """Help from /r/TangibleLight.

    Print non-perfect tree-like structure to a file.
    """
    for node in tree.keys():
        with open(file, 'a') as f:
            f.write(f'{prefix} | \n')
            f.write(f'{prefix} +-- {node}\n')
        tprint(tree[node], f'{prefix} |  ')


def main():
    """Result should be like this:

    002
     |
     + -- 003
           |
           + -- 004
           |     |
           |     + -- 012
           |           |
           |           + -- 014
           |
           + -- 008
                 |
                 + -- 009
                 |     |
                 |     + -- 011
                 |     |
                 |     + -- 013
                 |
                 + -- 010
    """
    data = [
        ["002"],
        ["002", "003"],
        ["002", "003", "008"],
        ["002", "003", "008", "009", "013"],
        ["002", "003", "008", "010"],
        ["002", "003", "004", "012", "014"],
        ["002", "003", "008", "009", "011"],
    ]

    # Sort data lexico...lexolo... from lesster to bigger
    data = sorted(data)
    pprint(data)
    # data = [
    #     ["002"],
    #     ["002", "003"],
    #     ["002", "003", "004", "012", "014"],
    #     ["002", "003", "008"],
    #     ["002", "003", "008", "009", "011"],
    #     ["002", "003", "008", "009", "013"],
    #     ["002", "003", "008", "010"],
    # ]

    # Make a dictionary tree from `data` values
    # Found on the internet with both functions
    Tree = lambda: defaultdict(Tree)
    t = Tree()
    for place in data:
        add(t, place)
    dicts = make_tree_dict(t)

    # {'002': {
    #     '003': {
    #         '004': {
    #             '012': {}
    #         },
    #         '008': {
    #             '009': {
    #                 '011': {},
    #                 '013': {}
    #             },
    #             '010': {}
    #         }
    #     }
    # }
    # }

    # Create an empty file if file doesn't already exists
    # If it exists, empty the file
    resfile = Path('./result.txt')
    if resfile.exists():
        with open(resfile, 'w'):
            pass

    # Because I'm not sure how to edit it further, print it into a file
    tprint(dicts, prefix='', file=resfile)

    # Load lines from file into a list
    # and ignore first three characters from each line
    with open(resfile, 'r') as f:
        lines = [line.strip()[3:] for line in f.readlines()]

    # Split lines by space-like chars
    lines = [line.split() for line in lines]

    # Transpose the list of list
    transposed = list(map(list, itertools.zip_longest(*lines, fillvalue='')))

    # Replace all occurrences of `|` after the last `+--` by `   `
    # Example:
    #     ['002', '|', '+--', '|', '|', '|'] --> ['002', '|', '+--', '   ', '   ', '   ']
    trsfm_updated = []
    for line in transposed:
        last_idx = find_last_list_occurance(line, '+--')
        # If last index is found, convert all remaining items to '   '
        if last_idx:
            line = [item if idx <= last_idx else '   ' for (idx, item) in enumerate(line[1:], 1)]
        # If last index is not found (ends with number or something), just return the line
        else:
            line = [item for item in line[1:]]
        trsfm_updated.append(line)

    # Add spaces around existing connectors
    trsfm_updated = [(' | ' if item == '|' else item for item in line) for line in trsfm_updated]
    trsfm_updated = [(' +-- ' if item == '+--' else item for item in line) for line in trsfm_updated]

    # Transform lists back into the original shape
    original_lines = list(map(list, itertools.zip_longest(*trsfm_updated, fillvalue='')))
    original_lines = [f'{"".join(line)}\n' for line in original_lines]

    # Print into terminal
    print("=======")
    for line in original_lines:
        print(line, end='')

    # Write lines into files, rewrite existing
    with open(resfile, 'w') as f:
        f.writelines(original_lines)


if __name__ == '__main__':
    main()
