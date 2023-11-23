def instability(in_deps: float, out_deps: float) -> float:
    total_deps = in_deps + out_deps
    if not total_deps:
        return 1

    return round(out_deps / total_deps, 2)


def stability(in_deps: float, out_deps: float) -> float:
    return round(1 - instability(in_deps, out_deps), 2)


def abstraction(abs_classes: float, imp_classes: float) -> float:
    total_classes = abs_classes + imp_classes
    if not total_classes:
        return 1

    return round(abs_classes / (abs_classes + imp_classes), 2)


def implementation(abs_classes: float, imp_classes: float) -> float:
    return round(1 - abstraction(abs_classes, imp_classes), 2)
