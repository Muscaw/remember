from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Dict, Tuple

import click
import yaml


@dataclass(frozen=True)
class Configuration:
    books_location: Path = Path.home() / "notes" / "books"

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> Configuration:
        return Configuration(books_location=Path(data["notes"]["location"]))


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


def construct_filename(document_date: date) -> str:
    return document_date.strftime("%Y-%m-%d") + ".md"


def construct_path(books_location: Path, book_name: str, document_date: date) -> Path:
    return books_location / book_name / construct_filename(document_date)


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
    path = construct_path(conf.books_location, book_name, document_date)
    if not path.exists():
        path.parent.mkdir(parents=True)
    with open(path, "a") as file:
        file.write("- [] " + " ".join(message) + "\n")


@cli.command()
@click.option(
    "-d",
    "--date",
    "document_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
)
@click.option("-b", "--book", "book_name", type=str, default="main")
def show_file(document_date: date, book_name: str) -> None:
    path = construct_path(conf.books_location, book_name, document_date)
    if not path.exists():
        click.echo(f"No notes at {path}")
        return
    with open(path, "r") as file:
        click.echo_via_pager(file.read())

def main():
    global conf
    conf = load_configuration()
    cli()


if __name__ == "__main__":
    main()