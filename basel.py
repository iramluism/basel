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

    _args = parser.parse_args()

    basel = setup()
    if _args.command == "report":
        basel.report(_args.path)


if __name__ == "__main__":
    main()
