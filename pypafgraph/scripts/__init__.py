#!/usr/bin/env python3

import sys
import argparse

from pypafgraph.scripts.filter import filter_cli, filter_main
from pypafgraph.scripts.repeats import repeats_cli, repeats_main
from pypafgraph.scripts.unsoftmask import unsoftmask_cli, unsoftmask_main
from pypafgraph.scripts.cluster import cluster_cli, cluster_main
from pypafgraph.scripts.selectseqs import selectseqs_cli, selectseqs_main


def cli(prog: str, args: str) -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        prog=prog,
        description=""
    )

    subparsers = parser.add_subparsers(dest='subparser_name')

    filter_subparser = subparsers.add_parser(
        "filter",
        help="Filter matches."
    )

    filter_cli(filter_subparser)

    repeats_subparser = subparsers.add_parser(
        "repeats",
        help="Find segmental duplications."
    )

    repeats_cli(repeats_subparser)

    unsoftmask_subparser = subparsers.add_parser(
        "unsoftmask",
        help="Find softmasked regions and uppercase sequences."
    )

    unsoftmask_cli(unsoftmask_subparser)

    cluster_subparser = subparsers.add_parser(
        "cluster",
        help="Cluster sequences."
    )

    cluster_cli(cluster_subparser)

    selectseqs_subparser = subparsers.add_parser(
        "selectseqs",
        help="Extract sequences given a tsv of clusters."
    )

    selectseqs_cli(selectseqs_subparser)

    parsed = parser.parse_args(args)

    if parsed.subparser_name is None:
        parser.print_help()
        sys.exit(0)

    return parsed


def main():
    args = cli(prog=sys.argv[0], args=sys.argv[1:])
    try:
        if args.subparser_name == "filter":
            filter_main(args)
        elif args.subparser_name == "repeats":
            repeats_main(args)
        elif args.subparser_name == "unsoftmask":
            unsoftmask_main(args)
        elif args.subparser_name == "cluster":
            cluster_main(args)
        elif args.subparser_name == "selectseqs":
            selectseqs_main(args)
        else:
            raise ValueError("I shouldn't reach this point ever")

    except BrokenPipeError:
        # Pipes get closed and that's normal
        sys.exit(0)

    except KeyboardInterrupt:
        print("Received keyboard interrupt. Exiting.", file=sys.stderr)
        sys.exit(1)

    except EnvironmentError as e:
        print((
            "Encountered a system error.\n"
            "We can't control these, and they're usually related to your OS.\n"
            "Try running again."
        ), file=sys.stderr)
        raise e

    except Exception as e:
        print((
            "I'm so sorry, but we've encountered an unexpected error.\n"
            "This shouldn't happen, so please file a bug report with the "
            "authors.\nWe will be extremely grateful!\n\n"
        ), file=sys.stderr)
        raise e

    return
