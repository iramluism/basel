import argparse
from pathlib import Path

from basel import config
from basel.client import Basel
from basel.components import ModuleComponentLoader
from basel.views import ConsoleView

COMMANDS = {
    "report": {
        "method": "report",
        "args": [
            ("path", "root_path"),
            ("ignore_dependencies", "ignore_dependencies"),
            ("exclude", "exclude_components"),
            ("no-packages", "exclude_packages"),
            ("filter", "filter_by_components"),
        ],
    }
}


def get_args_from_namespace(command, namespace):
    comman_spec = COMMANDS.get(command)
    kwargs = {}

    for command_arg, method_arg in comman_spec.get("args"):
        value = getattr(namespace, command_arg, None)
        kwargs[method_arg] = value

    return kwargs


def cast_list_string(string):
    if string:
        return string.split(",")


def main():
    parser = argparse.ArgumentParser(
        prog=config.PROJECT_NAME,
        description="Calculate the abstraction and stability",
    )

    parser.add_argument("command", choices=["report"])
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument(
        "--ignore-dependencies",
        type=cast_list_string,
        help="Remove dependencies (modules, external libreries)",
    )
    parser.add_argument(
        "--exclude",
        type=cast_list_string,
        help="Exclude components from report",
    )
    parser.add_argument(
        "--no-packages", action="store_true", help="Exculde all python package"
    )

    parser.add_argument(
        "-f", "--filter", help="Filter Report by Components", type=cast_list_string
    )

    _args = parser.parse_args()

    loader = ModuleComponentLoader()
    console_view = ConsoleView()

    basel = Basel(loader=loader, view=console_view)

    command_name = _args.command
    command_spec = COMMANDS.get(command_name)

    method_name = command_spec.get("method")
    method_args = get_args_from_namespace(command_name, _args)

    method = getattr(basel, method_name)
    method(**method_args)


if __name__ == "__main__":
    main()
