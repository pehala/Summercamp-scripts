import itertools

from .entity import BaseEntity


def expand(entities: list[BaseEntity]) -> list[BaseEntity]:
    return list(itertools.chain.from_iterable(itertools.repeat(entity, int(entity.amount)) for entity in entities))


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i : i + n]


def cluster(entities: list[BaseEntity], size) -> list[list[BaseEntity]]:
    return list(divide_chunks(entities, size))
