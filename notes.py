from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Tuple

import click
import yaml


@dataclass(frozen=True)
class Configuration:
    notes_location: Path = Path.home() / "notes" / "books"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Configuration:
        return Configuration(notes_location=Path(data["notes"]["location"]))


def load_configuration() -> Configuration:
    config_path = Path("~/notes/config.yml")
    if config_path.exists():
        with open("~/notes/config.yml", "r") as file:
            data = yaml.safe_load(file)
            return Configuration.from_dict(data)
    else:
        return Configuration()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("message", nargs=-1)
@click.option(
    "-d",
    "--date",
    "document_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
)
@click.option("-b", "--book", "book_name", type=str, default="main")
def remember(message: Tuple[str, ...], document_date: date, book_name: str) -> None:
    if len(message) == 0:
        return
    if message[0] == "to":
        message = message[1:]
    filename = document_date.strftime("%Y-%m-%d") + ".md"
    path = conf.notes_location / book_name / filename
    if not path.exists():
        path.parent.mkdir(parents=True)
    with open(conf.notes_location / book_name / filename, "a") as file:
        file.write("- " + " ".join(message) + "\n")


if __name__ == "__main__":
    global conf
    conf = load_configuration()
    cli()
