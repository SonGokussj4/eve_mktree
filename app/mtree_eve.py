#!/usr/bin/env python3

from pathlib import Path
from pprint import pprint
from collections import defaultdict

DATA_FOLDER = Path('/ST/Evektor/UZIV/JVERNER/PROJEKTY/UZIV/JFROLEK/NEZALOHUJESE/20181205_eve-mktree/DATA')


def add(t, path):
    for node in path:
        t = t[node]


def make_tree_dict(t):
    return {k: make_tree_dict(t[k]) for k in t}


def tprint(tree, pref='-', root=True):
    """Prints the contents of a dictionary, formatted as a tree.

    pref: each line of output has this prepended. used to
            "nest" trees within each other

    root: if true, no decoration is performed on this level
            sub-trees will still be decorated.
    """
    last = len(tree) - 1

    # no decoration by default
    b_con = c_con = b_end = c_end = ''

    if not root:  # add decorations
        b_con = ' ├─ '  # branch, continuing
        c_con = ' │  '  # indent, continuing
        b_end = ' └─ '  # branch, ending
        c_end = '    '  # indent, ending

    for i, node in enumerate(tree):
        b, c = b_con, c_con

        if i == last:  # use the ending versions of indentations
            b, c = b_end, c_end

        print(f'{pref}{c_con}')
        print(f'{pref}{b}{node}')
        pre = f'{pref}{c}'

        tprint(tree[node], pre, False)


class Variant:

    def __init__(self, all_files: list):
        self.all_files = all_files
        self.pc = self.get_pc()

    def get_pc(self):
        if len(self.all_files) < 0:
            print("SHIT, LIST IS EMPTY")
            return None
        return self.all_files[0]

    @property
    def header(self):
        lines = (line.rstrip() for line in open(self.pc, 'r'))
        header_lines = []
        for line in lines:
            if line.startswith('#'):
                header_lines.append(line)
            else:
                break
        return header_lines

    @property
    def names(self):
        names = [item.replace('#n ', '').rstrip('~') for item in self.header if item.startswith(('#n', '$n'))]
        return names

    @property
    def nodes(self):
        if len(self.names) < 2:
            return [self.names[0]]
        else:
            return self.names[-2:]


def main():
    """Result should be like this:

    002
     |
     + -- 003
           |
           + -- 004
           |     |
           |     + -- 012
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
    # data = [
    #     ["002"],
    #     ["002", "003"],
    #     ["002", "003", "008"],
    #     ["002", "003", "008", "009", "013"],
    #     ["002", "003", "008", "010"],
    #     ["002", "003", "004", "012"],
    #     ["002", "003", "008", "009", "011"],
    # ]
    curdir = Path('.')
    # curdir = Path('/ST/Evektor/UZIV/JVERNER/PROJEKTY/UZIV/JFROLEK/NEZALOHUJESE/20181205_eve-mktree/DATA/')

    variants = []

    for item in DATA_FOLDER.iterdir():
        if not item.is_dir():
            continue
        folder = item
        # print("DEBUG: folder:", folder)
        folder_num = folder.name.split('_')[-1]

        # Grab only .pc files that have the same project number as parent folder
        # possible matches in name: '_002_' or '_002.'
        # '**/*' .. all files recursively
        files = [x for x in folder.glob('*.pc')
                 if x.is_file()
                 if f'_{folder_num}_' in x.name or f'_{folder_num}.' in x.name]

        variants.append(Variant(files))

    list_of_names = []
    for variant in variants:
        # print("\n#####################################################################################################")
        # print("#####################################################################################################")
        # print("variant.pc", variant.pc)
        # print("variant.names", variant.names)
        # print("variant.nodes", variant.nodes)
        joined_names = ';'.join(variant.names)
        list_of_names.append(joined_names)

    # print("================")
    vars_list = [var for var in list_of_names]
    # for variant in vars_list:
    #     print(variant)

    vars_list_sorted = sorted(vars_list)
    # print("DEBUG: vars_list_sorted:", vars_list_sorted)
    # print("================")
    vars_list = [items.split(';') for items in vars_list_sorted]

    Tree = lambda: defaultdict(Tree)
    t = Tree()
    for place in vars_list:
        add(t, place)

    dicts = make_tree_dict(t)
    # pprint(dicts)
    tprint(dicts, pref='', root=True)


if __name__ == '__main__':
    main()


# from collections import UserDict
# import collections


# __author__ = 'github.com/hangtwenty'


# def tupperware(mapping):
#     """ Convert mappings to 'tupperwares' recursively.
#     Lets you use dicts like they're JavaScript Object Literals (~=JSON)...
#     It recursively turns mappings (dictionaries) into namedtuples.
#     Thus, you can cheaply create an object whose attributes are accessible
#     by dotted notation (all the way down).
#     Use cases:
#         * Fake objects (useful for dependency injection when you're making
#          fakes/stubs that are simpler than proper mocks)
#         * Storing data (like fixtures) in a structured way, in Python code
#         (data whose initial definition reads nicely like JSON). You could do
#         this with dictionaries, but namedtuples are immutable, and their
#         dotted notation can be clearer in some contexts.
#     .. doctest::
#         >>> t = tupperware({
#         ...     'foo': 'bar',
#         ...     'baz': {'qux': 'quux'},
#         ...     'tito': {
#         ...             'tata': 'tutu',
#         ...             'totoro': 'tots',
#         ...             'frobnicator': ['this', 'is', 'not', 'a', 'mapping']
#         ...     }
#         ... })
#         >>> t # doctest: +ELLIPSIS
#         Tupperware(tito=Tupperware(...), foo='bar', baz=Tupperware(qux='quux'))
#         >>> t.tito # doctest: +ELLIPSIS
#         Tupperware(frobnicator=[...], tata='tutu', totoro='tots')
#         >>> t.tito.tata
#         'tutu'
#         >>> t.tito.frobnicator
#         ['this', 'is', 'not', 'a', 'mapping']
#         >>> t.foo
#         'bar'
#         >>> t.baz.qux
#         'quux'
#     Args:
#         mapping: An object that might be a mapping. If it's a mapping, convert
#         it (and all of its contents that are mappings) to namedtuples
#         (called 'Tupperwares').
#     Returns:
#         A tupperware (a namedtuple (of namedtuples (of namedtuples (...)))).
#         If argument is not a mapping, it just returns it (this enables the
#         recursion).
#     """
#     if (isinstance(mapping, collections.Mapping) and
#             not isinstance(mapping, ProtectedDict)):
#         for key, value in mapping.items():
#             mapping[key] = tupperware(value)
#         return namedtuple_from_mapping(mapping)
#     return mapping


# def namedtuple_from_mapping(mapping, name="Tupperware"):
#     this_namedtuple_maker = collections.namedtuple(name, mapping.keys())
#     return this_namedtuple_maker(**mapping)


# class ProtectedDict(UserDict):
#     """ A class that exists just to tell `tupperware` not to eat it.
#     `tupperware` eats all dicts you give it, recursively; but what if you
#     actually want a dictionary in there? This will stop it. Just do
#     ProtectedDict({...}) or ProtectedDict(kwarg=foo).
#     """
#     pass


# def tupperware_from_kwargs(**kwargs):
#     return tupperware(kwargs)


# def get_dict_depth(d, level=1):
#     if not isinstance(d, dict) or not d:
#         return level
#     return max(get_dict_depth(d[k], level + 1) for k in d)


# def add(t, path):
#     for node in path:
#         t = t[node]


# def make_tree_dict(t):
#     return {k: make_tree_dict(t[k]) for k in t}


# def grab_children(father):
#     local_list = []
#     for key, value in father.items():
#         local_list.append(key)
#         local_list.extend(grab_children(value))
#     return local_list
