from shutil import get_terminal_size

from purity.types import Function, Set


@Function.auto
def f(x: int) -> int:
    return x * 2


def _print_source() -> None:
    width, _ = get_terminal_size((80, 26))
    print("╭", "─" * (width - 2), "╮", sep="")

    with open(__file__, "r") as source_file:
        for line in source_file.read().splitlines():
            rem_space = width - len(line) - 5
            print("│", line, " " * rem_space, "│")

    print("╰", "─" * (width - 2), "╯", sep="")


def playground(*, print_source: bool = False) -> None:
    if print_source:
        _print_source()

    s1 = Set(3, 5, 1)
    g = Set.map(f)
    s2 = g(s1)
    print(s2)
