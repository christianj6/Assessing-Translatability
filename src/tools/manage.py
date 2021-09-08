import os
import json
from . import command
import argparse


class ManagementUtility:
    def __init__(self, argv: list = None) -> None:
        self.argv = argv
        self.parser = self.setup_parser()

    @classmethod
    def setup_parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-e", "--europarl", nargs="?", default="check_string_for_empty"
        )
        parser.add_argument(
            "-w", "--wikipedia", nargs="?", default="check_string_for_empty"
        )
        parser.add_argument(
            "-s", "--subtitles", nargs="?", default="check_string_for_empty"
        )
        parser.add_argument("-f", "--file", type=str)

        return parser

    def execute(self) -> None:
        args = self.parser.parse_args()
        command.run(**vars(args))


def execute_from_command_line(argv: list = None) -> None:
    utility = ManagementUtility(argv)
    utility.execute()
