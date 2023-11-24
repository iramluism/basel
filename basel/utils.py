from typing import List

DECIMALS = 2


def instability(in_deps: float, out_deps: float) -> float:
    """Calculate the instability
                            output dependencies
     Instability =  -----------------------------------------
                    output dependencies + input dependencies

    :param in_deps: input dependencies
    :param out_deps: output dependencies

    :return: instability
    """

    total_deps = in_deps + out_deps
    if not total_deps:
        return 1

    return round(out_deps / total_deps, DECIMALS)


def stability(in_deps: float, out_deps: float) -> float:
    """Calculate the stability
                            input dependencies
      Stability =  -----------------------------------------
                    input dependencies + output dependencies

      Stability = 1 - instability

    :param in_deps: input dependencies
    :param out_deps: output dependencies

    :return: Stability
    """

    return round(1 - instability(in_deps, out_deps), DECIMALS)


def abstraction(abs_classes: float, imp_classes: float) -> float:
    """Calculate the abstraction
                            abstract classes
     abstraction = -------------------------------------------
                    abstract classes + implementation classes

    :param abs_classes: abstract classes
    :param imp_classes: implementation classes

    :return: abstraction
    """

    total_classes = abs_classes + imp_classes
    if not total_classes:
        return 1

    return round(abs_classes / (abs_classes + imp_classes), DECIMALS)


def implementation(abs_classes: float, imp_classes: float) -> float:
    """Calculate the implementation
                              implementation classes
      implementation =  -----------------------------------------
                        implementation classes + abstract classes

      implementation = 1 - abstraction

    :param abs_classes: abstract classes
    :param imp_classes: implementation classes

    :return: implementation
    """

    return round(1 - abstraction(abs_classes, imp_classes), DECIMALS)


def abs_error_to_main_sequence(instability: float, abstraction: float) -> float:
    """Calculate the absolute error between the instability and abstraction
    point to the main sequence.

    error = |instability + abstraction - 1|

    :param instability: instability value
    :param abstraction: abstraction value
    :return: absolute error to the main sequence
    """
    return round(abs(instability + abstraction - 1), DECIMALS)


def mean(values: List[float]) -> float:
    """Calculate the mean
    :param values: the list of floats
    :return: the mean values
    """

    if not values:
        return 0

    n_values = len(values)
    sum_values = sum(values)

    _mean = round(sum_values / n_values, DECIMALS)

    return _mean
