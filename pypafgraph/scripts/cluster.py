#!/usr/bin/env python3

import sys
import argparse

import networkx as nx

import markov_clustering as mc

from pypafgraph.paf import PAF
from pypafgraph.clustering import paf_to_graph


def cluster_cli(parser: argparse.ArgumentParser):
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
        "-c", "--min-cov",
        default=0.0,
        type=float,
        help=("The minimum coverage allowed for a connection between "
              "two sequences to be called.")
    )

    parser.add_argument(
        "-i", "--inflation",
        default=1.4,
        type=float,
        help=""
    )

    parser.add_argument(
        "-e", "--expansion",
        default=2.0,
        type=float,
        help=""
    )

    parser.add_argument(
        "-p", "--plot",
        default=None,
        type=str,
        help="Plot the clusters"
    )

    parser.add_argument(
        "--plot-width",
        default=8,
        type=float,
        help="The width of the plot in inches."
    )

    parser.add_argument(
        "--plot-height",
        default=5,
        type=float,
        help="The height of the plot in inches."
    )

    parser.add_argument(
        "--plot-dpi",
        default=300,
        type=float,
        help="The resolution of the plot in dpi."
    )
    return


def plot_clusters(filename, matrix, clusters, height=5, width=7, dpi=300):
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots(figsize=(width, height))

    mc.draw_graph(
        matrix,
        clusters,
        node_size=50,
        with_labels=False,
        edge_color="silver",
        ax=ax
    )

    fig.savefig(filename, dpi=dpi)
    return


def cluster_main(args: argparse.Namespace):
    paf = PAF.from_file(args.inpaf)
    G = paf_to_graph(paf, min_cov=args.min_cov)

    nodes = list(G.nodes())
    matrix = nx.to_scipy_sparse_matrix(G, nodelist=nodes)
    result = mc.run_mcl(
        matrix,
        expansion=args.expansion,
        inflation=args.inflation
    )
    clusters = mc.get_clusters(result)

    named_clusters = [
        [nodes[i] for i in cl]
        for cl
        in clusters
    ]

    for i, cluster_members in enumerate(named_clusters, 1):
        for member in cluster_members:
            print(f"{i}\t{member}", file=args.outfile)

    if args.plot is not None:
        plot_clusters(
            args.plot,
            matrix,
            clusters,
            args.plot_height,
            args.plot_width,
            args.plot_dpi
        )

    return
