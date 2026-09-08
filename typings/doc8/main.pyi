


class Result:


    errors: list[tuple[str, str, int | str, str, str]]


def doc8(*, paths: list[str]) -> Result:
    ...
