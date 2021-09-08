import os
import json
from . import command
import argparse
import nltk


class ManagementUtility:
    def __init__(self, argv: list = None) -> None:
        self.argv = argv
        self.parser = self.setup_parser()
        self.setup_nltk()

    @classmethod
    def setup_nltk(cls) -> None:
        nltk.download("brown")
        nltk.download("wordnet_ic")
        nltk.download("punkt")
        nltk.download("semcor")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("wordnet")

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
