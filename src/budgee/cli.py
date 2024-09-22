"""Command-line interface."""

from pathlib import Path

import rich_click as click

from budgee.manager import Manager


@click.command()
@click.option(
    "--context",
    default=None,
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    help="Path to the context file to load.",
)
@click.version_option()
def cli(context: Path | None = None) -> None:
    """Launches the command-line interface.

    Args:
        context: Path to the context file to load.
    """
    manager = Manager() if context is None else Manager.load(context)
    manager.summarize()
