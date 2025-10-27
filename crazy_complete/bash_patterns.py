import re
from collections import defaultdict

def tokenize(s):
    """
    Tokenize a string by splitting around non-alphanumeric characters,
    but keep delimiters (like -, =, /, .).
    """
    tokens = re.split(r'([^\w])', s)
    return [t for t in tokens if t != ""]

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_terminal = False

def insert_trie(root, tokens):
    node = root
    for token in tokens:
        node = node.children[token]
    node.is_terminal = True

def trie_to_pattern(node):
    """
    Recursively convert the trie into a Bash extglob pattern.
    """
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

    if len(parts) == 1:
        return parts[0]
    else:
        return "@(" + "|".join(sorted(parts)) + ")"

def compact_glob_trie(strings):
    """
    Build a recursive glob pattern that matches all input strings.
    """
    strings = sorted(set(strings))
    if len(strings) == 1:
        return strings[0]

    # Tokenize each string
    token_lists = [tokenize(s) for s in strings]

    # Build Trie
    root = TrieNode()
    for tokens in token_lists:
        insert_trie(root, tokens)

    # Convert Trie to pattern
    return trie_to_pattern(root)

def make_pattern(strings):
    candidate0 = '|'.join(strings)
    candidate1 = compact_glob_trie(strings)

    return candidate0 if len(candidate0) < len(candidate1) else candidate1
