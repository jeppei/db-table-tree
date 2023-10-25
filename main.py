import argparse
from expandable_tree import ExpandableTree

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--table", nargs="?", type=str,  default="none", help="")
    cli.add_argument("--env",   nargs="?", type=str,  default="prod", help="")
    cli.add_argument("--id",    nargs="?", type=int,  default=1, help="")
    args = cli.parse_args()

    expandable_tree = ExpandableTree(
        args.table,
        args.id,
        args.env
    )
