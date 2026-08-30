"""CLI:  uv run faultprop smoke | grid | cases"""
from __future__ import annotations

import os

import typer
from dotenv import load_dotenv
from rich import print

from .runner import run_grid
from .workflow.cases import load_cases

load_dotenv()
app = typer.Typer(no_args_is_help=True)


@app.command()
def cases():
    """List loaded cases and their correct actions."""
    for c in load_cases():
        print(f"[bold]{c.case_id}[/bold]  {c.correct_action.value:<18} ambiguous={c.ambiguous}  {c.rationale[:70]}")


@app.command()
def smoke(model: str = typer.Option(None), case: str = typer.Option(None)):
    """One case, single topology, no faults. Proves the plumbing works."""
    model = model or os.environ.get("FAULTPROP_MODEL") or typer.BadParameter("set --model or FAULTPROP_MODEL")
    out = run_grid("single", "none", 0.0, model, repeats=1, cases=[case] if case else None)
    print(f"wrote {out}")


@app.command()
def grid(topology: str = "single", fault: str = "none", lam: float = 0.0,
         model: str = typer.Option(None), repeats: int = 1):
    """Run one cell of the experiment grid."""
    model = model or os.environ["FAULTPROP_MODEL"]
    out = run_grid(topology, fault, lam, model, repeats=repeats)
    print(f"wrote {out}")


if __name__ == "__main__":
    app()
