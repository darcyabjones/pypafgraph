#!/usr/bin/env python3

import sys
import argparse

from intervaltree import Interval, IntervalTree

from pypafgraph.bed import BED, bed_to_itree
from pypafgraph.paf import PAF
from pypafgraph.interval_utils import total_intersection
from pypafgraph.utils import get_genome_name


def filter_cli(parser: argparse.ArgumentParser):
    parser.add_argument(
        "inbed",
        default=sys.stdin,
        type=argparse.FileType('r'),
        help="Input bed file. Use '-' for stdin.",
    )
    parser.add_argument(
        "inpaf",
        default=sys.stdin,
        type=argparse.FileType('r'),
        help="Input paf file. Use '-' for stdin.",
    )

    parser.add_argument(
        "-o", "--outfile",
        default=sys.stdout,
        type=argparse.FileType('w'),
        help="Output paf file path. Default stdout.",
    )

    parser.add_argument(
        "-m", "--min-length",
        default=1,
        type=int,
        help="The minimum allowed match length excluding repeats.",
    )

    parser.add_argument(
        "-s", "--sep",
        default=None,
        type=str,
        help=(
            "Split sequence ids by this separator and exclude matches where "
            "both members have the same prefix."
        )
    )

    parser.add_argument(
        "-p", "--prop-overlap",
        default=0.5,
        type=float,
        help="The maximum proportion of bases allowed to be in repeat regions."
    )

    return


def filter_by_interval(
    itree: IntervalTree,
    interval: Interval,
    min_length: int,
    prop_coverage: float
) -> bool:
    """ """

    if itree is None and interval.length() >= min_length:
        return False

    len_intersect = total_intersection(itree, interval)

    if interval.length() <= 0:
        prop_intersect = 0
    else:
        prop_intersect = len_intersect / interval.length()

    lt_min_length = (interval.length() - len_intersect) < min_length
    gt_max_cov = prop_intersect >= prop_coverage
    return lt_min_length or gt_max_cov


def filter_main(args: argparse.Namespace):

    bed = BED.from_file(args.inbed)
    bed_tree = bed_to_itree(bed)

    paf = PAF.from_file(args.inpaf)
    for p in paf:
        if args.sep is not None:
            qgenome = get_genome_name(p.query, args.sep)
            tgenome = get_genome_name(p.target, args.sep)

            if qgenome == tgenome:
                continue

        if p.alilen < args.min_length:
            continue

        query, qinterval = p.query_as_interval()
        if filter_by_interval(bed_tree.get(query, None), qinterval,
                              args.min_length, args.prop_overlap):
            continue

        target, tinterval = p.target_as_interval()
        if filter_by_interval(bed_tree.get(target, None), tinterval,
                              args.min_length, args.prop_overlap):
            continue

        print(p, file=args.outfile)

    return
