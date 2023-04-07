from shutil import get_terminal_size


def get_true_anno(anno: type | str) -> type:
    if isinstance(anno, type):
        return anno
    return eval(anno, globals())


def source_print(source_path: str) -> None:
    width, _ = get_terminal_size((80, 26))
    print("╭", "─" * (width - 2), "╮", sep="")

    with open(source_path, "r") as source_file:
        for line in source_file.read().splitlines():
            rem_space = width - len(line) - 5
            print("│", line, " " * rem_space, "│")

    print("╰", "─" * (width - 2), "╯", sep="")
