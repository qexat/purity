from collections.abc import Callable, Iterator
from typing import Any, Generic, Never, Self, TypeVar as _TypeVar, overload

from purity.utils import get_true_anno

Number = _TypeVar("Number", int, float, complex)
NumericTypes = int, float, complex

Domain = _TypeVar("Domain")
Codomain = _TypeVar("Codomain")
NumberDomain = _TypeVar("NumberDomain", int, float, complex)
NumberCodomain = _TypeVar("NumberCodomain", int, float, complex)


class TypeError(TypeError):
    @classmethod
    def from_uncompatible_morphism(cls, morphism: str, comorphk: str) -> Self:
        return cls(f"cannot transform morphism {morphism!r} into {comorphk} comorphism")


class TypedError(TypeError):
    @classmethod
    def from_pyfunction_args_nb(
        cls,
        func_name: str,
        expected_nb: int,
        received_nb: int,
    ) -> Self:
        return cls(
            f"expected {expected_nb} args,"
            f"but {func_name} has {received_nb} typed args"
        )

    @classmethod
    def from_pyfunction_no_return(cls, func_name: str) -> Self:
        return cls(f"{func_name}: return typing is missing")


class DomainError(TypeError):
    pass


class Morphism(Generic[Domain, Codomain]):
    @property
    def __pyfunction__(self) -> Callable[[Domain], Codomain]:
        return self.__underlying

    @property
    def domain(self) -> type[Domain]:
        return self.__domain

    @property
    def codomain(self) -> type[Codomain]:
        return self.__codomain

    def __init__(
        self,
        pyfunction: Callable[[Domain], Codomain],
        /,
        domain: type[Domain],
        codomain: type[Codomain],
    ) -> None:
        self.__underlying = pyfunction
        self.__domain = domain
        self.__codomain = codomain

    def __call__(self, x: Domain) -> Codomain:
        return self.__pyfunction__(x)


class Function(Morphism[NumberDomain, NumberCodomain]):
    def __call__(self, x: NumberDomain) -> NumberCodomain:
        return self.__pyfunction__(x)

    @classmethod
    def auto(cls, pyfunction: Callable[[NumberDomain], NumberCodomain], /) -> Self:
        fname = pyfunction.__qualname__
        args_anno = {
            k: v for k, v in pyfunction.__annotations__.items() if k != "return"
        }
        return_anno: type | str | None = pyfunction.__annotations__.get("return", None)
        nb_args = len(args_anno)

        if nb_args != 1:
            raise TypedError.from_pyfunction_args_nb(fname, 1, nb_args)

        arg_anno: type | str = next(iter(args_anno.values()))
        arg_type = get_true_anno(arg_anno)

        if return_anno is None:
            raise TypedError.from_pyfunction_no_return(fname)

        return_type = get_true_anno(return_anno)

        if arg_type not in NumericTypes:
            raise DomainError(f"{fname}: arg must be numeric")

        if return_type not in NumericTypes:
            raise DomainError(f"{fname}: return value must be numeric")

        return cls(pyfunction, domain=arg_type, codomain=return_type)


class Set(Generic[Number]):
    @overload
    @classmethod
    def map(cls, morphism: Morphism[Self, Self]) -> Morphism[Self, Self]:
        pass

    @overload
    @classmethod
    def map(
        cls,
        morphism: Morphism[NumberDomain, NumberCodomain],
    ) -> "Morphism[Set[NumberDomain], Set[NumberCodomain]]":
        pass

    @overload
    @classmethod
    def map(cls, morphism: Morphism[Any, Any]) -> Never:
        pass

    @classmethod
    def map(cls, morphism: Morphism[Any, Any]) -> Morphism[Self, Self]:  # type: ignore
        if morphism.domain == cls and morphism.codomain == cls:
            return morphism
        elif morphism.domain in NumericTypes and morphism.codomain in NumericTypes:

            def comorphism(xs: Self) -> Self:
                return cls(*tuple(map(morphism, xs)))

            return Morphism(comorphism, cls, cls)
        else:
            raise TypeError.from_uncompatible_morphism(repr(morphism), "set")

    def __init__(self, *values: Number) -> None:
        self.__underlying = set(values)

    def __repr__(self) -> str:
        return repr(self.__underlying)

    def __iter__(self) -> Iterator[Number]:
        yield from self.__underlying

    def add(self, value: Number) -> Self:
        return type(self)(*self.__underlying, value)

    def remove(self, value: Number) -> Self:
        return type(self)(*(self.__underlying - {value}))
