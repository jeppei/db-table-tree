import argparse
from main_window import MainWindow

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--table", nargs="?", type=str,  default="none", help="")
    cli.add_argument("--env",   nargs="?", type=str,  default="prod", help="")
    cli.add_argument("--id",    nargs="?", type=int,  default=1, help="")
    args = cli.parse_args()

    main_window = MainWindow(
        args.table,
        args.id,
        args.env
    )
