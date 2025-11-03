'''Module for creating Bash globs.'''

from collections import defaultdict

from .algo import numbers_are_contiguous


class TrieNode:
    '''Trie class.'''

    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_terminal = False

    def insert(self, string):
        '''Insert string into trie.'''

        node = self
        for char in string:
            node = node.children[char]
        node.is_terminal = True


def _build_pattern(parts):
    if len(parts) == 1:
        return parts[0]

    try:
        ints = sorted(map(int, parts))
        if numbers_are_contiguous(ints):
            return f'[{ints[0]}-{ints[-1]}]'
    except ValueError:
        pass

    return "@(" + "|".join(sorted(parts)) + ")"


def trie_to_pattern(node):
    '''
    Recursively convert the trie into a Bash extglob pattern.
    '''
    if not node.children:
        return ""

    parts = []
    for token, child in node.children.items():
        sub = trie_to_pattern(child)
        if sub:
            parts.append(token + sub)
        else:
            parts.append(token)

    # Terminal means that this path can end here
    if node.is_terminal:
        parts.append("")  # Represent the option to stop early

    return _build_pattern(parts)


def compact_glob_trie(strings):
    '''
    Build a recursive glob pattern that matches all input strings.
    '''
    strings = sorted(set(strings))
    if len(strings) == 1:
        return strings[0]

    # Build Trie
    root = TrieNode()
    for string in strings:
        root.insert(string)

    # Convert Trie to pattern
    return trie_to_pattern(root)


def make_pattern(strings):
    '''Make a glob pattern that matches `strings`.'''

    candidate0 = '|'.join(strings)
    candidate1 = compact_glob_trie(strings)

    return candidate0 if len(candidate0) < len(candidate1) else candidate1
