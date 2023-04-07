from argparse import ArgumentParser, Namespace

from purity.playground import playground


def parse_args(args: list[str] | None = None) -> Namespace:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest="subcommand")

    playground_parser = subparsers.add_parser(name="playground")
    playground_parser.add_argument("--print-source", action="store_true")

    return parser.parse_args(args)


def main_debug(args: list[str] | None = None) -> int:
    parsed_args = parse_args(args)

    if parsed_args.subcommand == "playground":
        playground(print_source=parsed_args.print_source)
    else:
        print("If you wanted to access the playground, use: `purity playground`.")
        return 1

    return 0


def main() -> int:
    return main_debug()
