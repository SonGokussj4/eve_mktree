#!/usr/bin/env python3

from pprint import pprint
from collections import defaultdict
# import pptree

# def printTree(L, indent=""):
#     for i in L:
#         if isinstance(i, str):
#             print(indent, 'Root: ', i)
#         else:
#             print(indent, '--Subtree: ', i)
#             printTree(i, indent + "    ")


# def createTreeFromEdges(edges):
#     tree = {}
#     for v1, v2 in edges:
#         tree.setdefault(v1, []).append(v2)
#         tree.setdefault(v2, []).append(v1)
#     return tree


def main():
#     """Result should be like this:

#     002
#      |
#      + -- 003
#            |
#            + -- 004
#            |     |
#            |     + -- 012
#            |
#            + -- 008
#                  |
#                  + -- 009
#                  |     |
#                  |     + -- 011
#                  |     |
#                  |     + -- 013
#                  |
#                  + -- 010
#     """
    data = [
        ["002"],
        ["002", "003"],
        ["002", "003", "008"],
        ["002", "003", "008", "009", "013"],
        ["002", "003", "008", "010"],
        ["002", "003", "004", "012"],
        ["002", "003", "008", "009", "011"],
    ]

    data = sorted(data)

    pprint(data)
    print("=============")

#     ls_set = set()
#     for ls in data:
#         if len(ls) < 2:
#             continue
#         for parent, child in zip(ls[0:-1], ls[1:]):
#             # print("{}-{}".format(parent, child))
#             ls_set.add((parent, child))

#     ls = sorted(ls_set)
#     pprint(ls)

#     res = createTreeFromEdges(ls)
#     pprint(res)

#     print("=============")

#     N002 = pptree.Node("002")
#     N003 = pptree.Node("003", N002)
#     N008 = pptree.Node("008", N003)
#     N009 = pptree.Node("009", N008)
#     N013 = pptree.Node("013", N009)
#     N010 = pptree.Node("010", N003)
#     N004 = pptree.Node("004", N003)
#     N012 = pptree.Node("012", N004)
#     N011 = pptree.Node("011", N009)

#     pptree.print_tree(N002)


#     # for idx, tpl in enumerate(ls, 1):
#     #     parent, child = tpl

#     # import itertools

#     # res = map(list, itertools.zip_longest(*data, fillvalue='---'))
#     # res2 = [ls for ls in res]
#     # for item in res2:
#     #     print(item)
#     # print("=============")

#     # new = []
#     # uniques = []
#     # for ls in res2:
#     #     ls_new = []
#     #     for item in ls:
#     #         if item in uniques:
#     #             ls_new.append("---")
#     #         else:
#     #             uniques.append(item)
#     #             ls_new.append(item)
#     #     new.append(ls_new)

#     # pprint(new)
#     # print("=============")

#     # res3 = map(list, itertools.zip_longest(*new, fillvalue='|'))
#     # res = [[ele if ele != '---' else '+--' for ele in item] for item in res3]
#     # pprint(res)




    def get_dict_depth(d, level=1):
        if not isinstance(d, dict) or not d:
            return level
        return max(get_dict_depth(d[k], level + 1) for k in d)


    def add(t, path):
        for node in path:
            t = t[node]


    def make_tree_dict(t):
        return {k: make_tree_dict(t[k]) for k in t}


    def grab_children(father):
        local_list = []
        for key, value in father.items():
            local_list.append(key)
            local_list.extend(grab_children(value))
        return local_list


    def tprint(tree, prefix='', file='./result.txt'):
        """Tiny help."""
        for node in tree.keys():
            with open(file, 'a') as f:
                f.write(f'{prefix}| \n')
                f.write(f'{prefix}+--{node}\n')
            tprint(tree[node], f'{prefix}|  ')

    Tree = lambda: defaultdict(Tree)
    t = Tree()
    for place in data:
        add(t, place)

    # print("=============")
    dicts = make_tree_dict(t)
    # pprint(dicts)

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

    # depth = get_dict_depth(dicts)
    # print("DEBUG: depth:", depth)
    from pathlib import Path
    resfile = Path('./result.txt')
    if resfile.exists():
        with open(resfile, 'w'):
            pass

    tprint(dicts, prefix='', file=resfile)

    print("=============")

    # Load up into list:
    with open(resfile, 'r') as f:
        lines = [line.strip()[3:] for line in f.readlines()]

    for line in lines:
        print(line)
        splitted = line.split()
        # print(splitted)

    import numpy



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
