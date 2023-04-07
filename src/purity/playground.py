from purity.types import Function, Set
from purity.utils import source_print


@Function.auto
def f(x: int) -> int:
    return x * 2


def playground(*, print_source: bool = False) -> None:
    if print_source:
        source_print(__file__)

    s1 = Set(3, 5, 1)
    g = Set.map(f)
    s2 = g(s1)
    print(s2)
