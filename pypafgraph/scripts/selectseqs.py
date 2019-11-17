#!/usr/bin/env python3

import argparse

from os import mkdir
from os.path import join as pjoin
from collections import defaultdict

from Bio import SeqIO


def selectseqs_cli(parser: argparse.ArgumentParser):
    parser.add_argument(
        "table",
        type=argparse.FileType('r'),
        help="Input clusters tsv file. Use '-' for stdin.",
    )
    parser.add_argument(
        "infile",
        type=argparse.FileType('r'),
        help="Input fasta file. Use '-' for stdin.",
    )

    parser.add_argument(
        "-p", "--prefix",
        default="component",
        type=str,
        help="Prefix of cluster fasta files.",
    )

    parser.add_argument(
        "-o", "--outdir",
        default=".",
        type=str,
        help="Output directory to write fasta files to.",
    )

    parser.add_argument(
        "-u", "--unplaced",
        default="unplaced",
        type=str,
        help="The name to give sequences that aren't assigned a cluster."
    )

    parser.add_argument(
        "-m", "--min-size",
        default=1,
        type=int,
        help=(
            "Minimum cluster size to include, other sequences will be "
            "unplaced."
        )
    )

    return


def parse_tsv(handle):
    out = dict()

    for line in handle:
        sline = line.strip().split("\t")
        out[sline[1]] = sline[0]

    return out


def count_clusters(d):
    counts = defaultdict(int)
    for seqid, cluster in d.items():
        counts[cluster] += 1

    return counts


def filter_clusters(clusters, counts, min_size=1):
    out = dict()
    for seqid, cluster in clusters.items():
        if counts[cluster] >= min_size:
            out[seqid] = cluster
    return out


def write_components(components, touched, outdir):
    for component in components:
        if touched[component]:
            mode = "a"
        else:
            mode = "w"

        touched[component] = True

        filename = pjoin(outdir, f"{component}.fasta")
        with open(filename, mode) as handle:
            SeqIO.write(components[component], handle, format="fasta")
    return


def selectseqs_main(args: argparse.Namespace):

    seqid_to_component = parse_tsv(args.table)
    cluster_counts = count_clusters(seqid_to_component)
    seqid_to_component = filter_clusters(
        seqid_to_component,
        cluster_counts,
        min_size=args.min_size
    )
    touched_components = {
        f"{args.prefix}{c}": False
        for c in seqid_to_component.values()
    }
    touched_components[args.unplaced] = False

    chunk_size = 10000
    components = defaultdict(list)
    seqs = SeqIO.parse(args.infile, format="fasta")

    if args.outdir != ".":
        mkdir(args.outdir)

    for i, seq in enumerate(seqs, 1):
        component = seqid_to_component.get(seq.id, None)
        if component is None:
            component = args.unplaced
        else:
            component = f"{args.prefix}{component}"

        components[component].append(seq)

        if i % chunk_size == 0:
            write_components(components, touched_components, args.outdir)
            components = defaultdict(list)

    write_components(components, touched_components, args.outdir)
    return
