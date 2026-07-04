# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Algorithm functions.'''

from collections import OrderedDict


def flatten(iterable):
    '''Flatten a list of iterables into a single list.'''

    result = []
    for item in iterable:
        result.extend(item)
    return result


def uniq(iterable):
    '''Return list of unique items, preserving order.'''

    result = []
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def partition(iterable, predicate):
    '''Split an iterable into two lists based on a predicate.

    Args:
        iterable:
            The input iterable to split.
        predicate (callable):
            A function returning True or False for each element.

    Returns:
        tuple: (matched, unmatched) where
            matched   -- list of items for which predicate(item) is True
            unmatched -- list of items for which predicate(item) is False
    '''

    a, b = [], []
    for item in iterable:
        if predicate(item):
            a.append(item)
        else:
            b.append(item)
    return (a, b)


def group_by(iterable, keyfunc):
    '''Group items from an iterable by a key function.

    Args:
        iterable:
            The input iterable of items to group.
        keyfunc (callable):
            Function applied to each item to determine its group key.

    Returns:
        OrderedDict:
            A mapping of key -> list of items with that key, preserving
            the order of first appearance of each key.
    '''
    result = OrderedDict()

    for item in iterable:
        val = keyfunc(item)

        if val in result:
            result[val].append(item)
        else:
            result[val] = [item]

    return result


def numbers_are_contiguous(numbers):
    '''Return True if the list of integers is contiguous (1, 2, 3, 4, ...)'''

    if not numbers:
        return False

    sorted_nums = sorted(numbers)
    return all(b - a == 1 for a, b in zip(sorted_nums, sorted_nums[1:]))


class SparseList(list):
    '''A list that automatically grows when assigning past its end.

     Assigning to an index greater than or equal to the current length extends
     the list with the configured default value until the index exists.
     '''

    def __init__(self, iterable=(), default=None):
        super().__init__(iterable)
        self.default = default

    def _extend_to(self, index):
        if index >= len(self):
            self.extend([self.default] * (index + 1 - len(self)))

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            super().__setitem__(index, value)
        else:
            if index < 0:
                super().__setitem__(index, value)
            else:
                self._extend_to(index)
                super().__setitem__(index, value)

    def insert(self, index, value):
        self._extend_to(index)
        super().insert(index, value)
