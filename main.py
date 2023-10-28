import argparse
from main_window import MainWindow

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--env",   nargs="?", type=str,  default="local", help="")
    cli.add_argument("--table", nargs="?", type=str,  default=None, help="")
    cli.add_argument("--id",    nargs="?", type=int,  default=None, help="")
    args = cli.parse_args()

    main_window = MainWindow(
        args.table,
        args.id,
        args.env
    )
