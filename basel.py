import argparse
from pathlib import Path

from src import config
from src.client import Basel
from src.components import ModuleComponentLoader
from src.views import ConsoleView


def setup() -> Basel:
    loader = ModuleComponentLoader()
    view = ConsoleView()

    basel = Basel(
        loader=loader,
        view=view,
    )

    return basel


def main():
    parser = argparse.ArgumentParser(
        prog=config.PROJECT_NAME, description="Calculate the abstraction and stability"
    )

    parser.add_argument("command", choices=["report"])
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument("--ignore-dependencies", type=str)

    _args = parser.parse_args()

    basel = setup()
    if _args.command == "report":
        ignore_dependencies = None
        if _args.ignore_dependencies:
            ignore_dependencies = _args.ignore_dependencies.split(",")

        basel.report(_args.path, ignore_dependencies)


if __name__ == "__main__":
    main()
