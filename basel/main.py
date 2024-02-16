import argparse
from pathlib import Path
import sys

from basel import config
from basel import ReportFormat
from basel.client import Basel
from basel.dtos import LogType
from basel.exporters import FileExporter
from basel.loaders import ModuleLoader
from basel.parsers import PythonParser
from basel.reports import Reporter

COMMANDS = {
    "report": {
        "method": "report",
        "args": [
            ("path", "root_path"),
            ("exclude", "exclude_components"),
            ("no-packages", "exclude_packages"),
            ("filter", "filter_by_components"),
            ("format", "report_format"),
        ],
    },
    "rel": {
        "method": "component_relations",
        "args": [
            ("path", "root_path"),
            ("exclude", "exclude_components"),
            ("no-packages", "exclude_packages"),
            ("filter", "filter_by_components"),
            ("format", "report_format"),
        ],
    },
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


def setup_basel_client() -> Basel:
    parser = PythonParser()
    loader = ModuleLoader(parser)

    reporter = Reporter(loader)
    exporter = FileExporter()

    client = Basel(loader, exporter, reporter)

    return client


HELPER_FOOTER_LOG = """
FORMATS: basic|html|mean_i|mean_a|mean|uml
"""


def main():
    parser = argparse.ArgumentParser(
        prog=config.PROJECT_NAME,
        description="Calculate the abstraction and stability",
        epilog=HELPER_FOOTER_LOG,
    )

    parser.add_argument("command", choices=["report", "rel"])
    parser.add_argument("-p", "--path", required=True, type=Path, nargs="+")

    parser.add_argument(
        "-e",
        "--exclude",
        type=cast_list_string,
        help="Exclude components from report",
    )
    parser.add_argument(
        "-np", "--no-packages", action="store_true", help="Exculde all python package"
    )

    parser.add_argument(
        "-f", "--filter", help="Filter Report by Components", type=cast_list_string
    )

    parser.add_argument(
        "-fmt",
        "--format",
        help="Report Format, 'basic' by default",
        type=ReportFormat,
        default=None,
    )

    if len(sys.argv) == 1:
        parser.print_help()
        return

    _args = parser.parse_args()

    basel = setup_basel_client()

    command_name = _args.command
    command_spec = COMMANDS.get(command_name)

    method_name = command_spec.get("method")
    method_args = get_args_from_namespace(command_name, _args)

    method = getattr(basel, method_name)

    result = method(**method_args)

    error_color = "\033[91m"
    success_color = "\033[92m"

    stdout = ""
    for log in result.logs:
        color = success_color
        if log.type == LogType.ERROR:
            color = error_color

        stdout += f"\n{color}{log.content}{color}"

    if result.content:
        stdout += str(result.content)

    print(stdout)


if __name__ == "__main__":
    main()
