#!/usr/bin/env python3

import sys
import argparse

from typing import Iterator

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from pypafgraph.bed import BED


def unsoftmask_cli(parser: argparse.ArgumentParser):
    parser.add_argument(
        "infile",
        default=sys.stdin,
        type=argparse.FileType('r'),
        help="Input fasta file. Use '-' for stdin.",
    )

    parser.add_argument(
        "-o", "--outbed",
        default=sys.stdout,
        type=argparse.FileType('w'),
        help="Output bed file path. Default stdout.",
    )

    parser.add_argument(
        "-f", "--outfasta",
        default=None,
        type=argparse.FileType('w'),
        help="Output fasta file path. Default not written.",
    )

    return


def find_lowercase_stretches(sr: SeqRecord) -> Iterator[BED]:

    start = None
    pos = 0

    for base in sr.seq:
        if base.islower() and start is None:
            start = pos
        elif base.isupper() and start is not None:
            yield BED(sr.id, start, pos)
            start = None

        pos += 1

    if start is not None:
        yield BED(sr.id, start, pos)

    return


def unsoftmask_main(args: argparse.Namespace):

    seqs = SeqIO.parse(args.infile, format="fasta")
    for seq in seqs:
        for bed_row in find_lowercase_stretches(seq):
            print(bed_row, file=args.outbed)

        if args.outfasta is not None:
            seq.seq = seq.seq.upper()
            SeqIO.write(seq, args.outfasta, format="fasta")

    return
