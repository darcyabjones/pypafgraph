#!/usr/bin/env python3


def get_genome_name(string: str, sep: str) -> str:
    """ Just split by separator and return first element.

    Example:
    >>> get_genome_name("test.one.two", '.')
    'test'
    >>> get_genome_name("test_one", ".")
    'test_one'
    """
    return string.split(sep, maxsplit=1)[0]
