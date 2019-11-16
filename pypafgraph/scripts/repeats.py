#!/usr/bin/env python3

import sys
import argparse
from collections import defaultdict

from typing import Dict
from typing import List

from intervaltree import Interval, IntervalTree

from pypafgraph.bed import BED
from pypafgraph.paf import PAF
from pypafgraph.interval_utils import sym_diff
from pypafgraph.utils import get_genome_name


def repeats_cli(parser: argparse.ArgumentParser):
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
        help="Output bed file path. Default stdout.",
    )

    parser.add_argument(
        "-s", "--sep",
        default=".",
        type=str,
        help=(
            "Split sequence ids by this separator and exclude matches where "
            "both members have the same prefix."
        )
    )
    return


def repeats_main(args: argparse.Namespace):
    paf = PAF.from_file(args.inpaf)

    repeats: Dict[str, List[Interval]] = defaultdict(list)

    for p in paf:
        qgenome = get_genome_name(p.query, args.sep)
        tgenome = get_genome_name(p.target, args.sep)

        if qgenome != tgenome:
            continue

        query, qinterval = p.query_as_interval()
        target, tinterval = p.target_as_interval()

        if (query == target) and qinterval.overlaps(tinterval):
            filtered = sym_diff(qinterval, tinterval)
            repeats[query].extend(filtered)
        else:
            repeats[query].append(qinterval)
            repeats[target].append(tinterval)

    for seqid, intervals in repeats.items():
        itree = IntervalTree(intervals)
        itree.merge_overlaps()
        for interval in itree:
            bed = BED(seqid, interval.begin, interval.end)
            print(bed, file=args.outfile)
    return
