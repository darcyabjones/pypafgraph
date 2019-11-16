from typing import List
from intervaltree import Interval, IntervalTree


def intersect(left: Interval, right: Interval) -> Interval:
    """ Find the intersection of two interval objects.

    Example:
    >>> from intervaltree import Interval
    >>> left = Interval(0, 5)
    >>> right = Interval(3, 10)
    >>> intersect(left, right)
    Interval(3, 5)
    """

    lstart = min([left.begin, left.end])
    lend = max([left.begin, left.end])
    rstart = min([right.begin, right.end])
    rend = max([right.begin, right.end])
    lbound = max([lstart, rstart])
    rbound = min([lend, rend])
    return Interval(lbound, rbound)


def union(left: Interval, right: Interval) -> Interval:
    """ Find the union of two interval objects.

    Example:
    >>> from intervaltree import Interval
    >>> left = Interval(0, 5)
    >>> right = Interval(3, 10)
    >>> union(left, right)
    Interval(0, 10)
    """

    lstart = min([left.begin, left.end])
    lend = max([left.begin, left.end])
    rstart = min([right.begin, right.end])
    rend = max([right.begin, right.end])

    if not ((lstart < rend) and (lend > rstart)):
        raise ValueError("Left and right must be overlapping.")

    lbound = min([lstart, rstart])
    rbound = max([lend, rend])
    return Interval(lbound, rbound)


def diff(left: Interval, right: Interval) -> List[Interval]:
    """ Find the regions in left, without the intersection with right.

    Examples:
    >>> left = Interval(0, 5)
    >>> right = Interval(3, 10)
    >>> diff(left, right)
    [Interval(0, 3)]
    >>> left = Interval(0, 10)
    >>> right = Interval(3, 6)
    >>> diff(left, right)
    [Interval(0, 3), Interval(6, 10)]
    >>> left = Interval(3, 6)
    >>> right = Interval(0, 10)
    >>> diff(left, right)
    []
    >>> left = Interval(0, 10)
    >>> right = Interval(10, 20)
    >>> diff(left, right)
    [Interval(0, 10)]
    >>> left = Interval(5, 10)
    >>> right = Interval(0, 4)
    >>> diff(left, right)
    [Interval(5, 10)]
    >>> left = Interval(5, 10)
    >>> right = Interval(0, 7)
    >>> diff(left, right)
    [Interval(7, 10)]
    """

    if not left.overlaps(right):
        return [left]

    lstart = min([left.begin, left.end])
    lend = max([left.begin, left.end])
    rstart = min([right.begin, right.end])
    rend = max([right.begin, right.end])

    out = []
    if rstart > lstart:
        out.append(Interval(lstart, min([rstart, lend])))

    if rend < lend:
        out.append(Interval(max([lstart, rend]), lend))

    return out


def sym_diff(left: Interval, right: Interval) -> List[Interval]:
    """ The symmetric difference/XOR of the two sets.

    Examples:
    >>> left = Interval(0, 10)
    >>> right = Interval(8, 15)
    >>> sym_diff(left, right)
    [Interval(0, 8), Interval(10, 15)]
    """
    inter = intersect(left, right)
    uni = union(left, right)
    return diff(uni, inter)


def total_intersection(itree: IntervalTree, interval: Interval) -> int:
    if interval.length() <= 0:
        return 0

    total = 0
    ovlps = IntervalTree(itree.overlap(interval))
    ovlps.merge_overlaps()
    for ovlp in ovlps:
        inter = intersect(interval, ovlp)
        total += inter.length()

    return total
