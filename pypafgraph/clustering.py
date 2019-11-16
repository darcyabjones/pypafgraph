#!/usr/bin/env python3

from typing import Dict
from typing import List, Iterable
from typing import Tuple

from collections import defaultdict

from intervaltree import Interval, IntervalTree

import networkx as nx

from pypafgraph.paf import PAF


def paf_to_intervals(pafs: Iterable[PAF]) -> Dict[Tuple[str, str], float]:
    """ """

    pairwise_intervals: Dict[Tuple[str, str], List[Interval]] = defaultdict(list)  # noqa
    lengths: Dict[str, int] = dict()

    for paf in pafs:
        if paf.query == paf.target:
            continue

        lengths[paf.query] = paf.qlen
        lengths[paf.target] = paf.tlen

        if paf.qlen < paf.tlen:
            _, interval = paf.query_as_interval()
            id_ = (paf.query, paf.target)
        elif paf.tlen < paf.qlen:
            _, interval = paf.target_as_interval()
            id_ = (paf.target, paf.query)
        elif paf.query < paf.target:
            _, interval = paf.query_as_interval()
            id_ = (paf.query, paf.target)
        else:
            _, interval = paf.target_as_interval()
            id_ = (paf.target, paf.query)

        pairwise_intervals[id_].append(interval)

    pairwise_covs: Dict[Tuple[str, str], float] = dict()

    for (query, target), intervals in pairwise_intervals.items():
        itree = IntervalTree(intervals)
        itree.merge_overlaps()

        ali_length = 0
        for interval in itree:
            ali_length += interval.length()

        contig_length = lengths[query]
        cov = ali_length / contig_length
        pairwise_covs[(query, target)] = cov

    return pairwise_covs


def paf_to_graph(
    pafs: Iterable[PAF],
    min_cov: float = 0.0,
    G: nx.Graph = None
) -> nx.Graph:
    """ """

    if G is None:
        G = nx.Graph()

    covs = paf_to_intervals(pafs)

    for (query, target), cov in covs.items():
        if cov >= min_cov:
            G.add_edge(query, target, weight=cov)

    return G
