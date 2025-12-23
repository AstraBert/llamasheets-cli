import asyncio
from typer import Typer, Option, Exit
from typing import Annotated
from rich.console import Console
from rich.markdown import Markdown
from typing import Literal
from pathlib import Path
from ._logo import print_logo
from .utils import save_api_key, load_api_key, AuthStatus, parse_spreadsheet

app = Typer()
console = Console()


@app.command(name="auth", help="Authorize LlamaCloud usage with an API key")
def auth(
    token: Annotated[
        str | None,
        Option(
            "--token",
            "-t",
            help="LlamaCloud API key. Prefer using `--stdin` for inputting your token from standard input (more secure).",
        ),
    ] = None,
    from_stdin: Annotated[
        bool,
        Option(
            "--stdin",
            help="Input your LlamaCloud API key from standard input.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    if not from_stdin and not token:
        console.print(
            "[red bold]You should provide one between `-t`/`--token` and `--stdin`"
        )
        raise Exit(1)
    elif from_stdin:
        tok = console.input("[bold]Your API key:[/] ", password=True)
        ret = save_api_key(tok)
        if ret.value == 2:
            console.print(
                "[yellow bold]WARNING[/]\nWe noticed that there is already an API key configured that does not match the provided one, do you want to overwrite? [y/n]"
            )
            ans = console.input(">>> ")
            if ans.strip().lower() in ("yes", "y", "yse"):
                save_api_key(tok, overwrite=True)
            else:
                console.print("[green bold]Authentication successful[/]")
                return None
        console.print("[green bold]Authentication successful[/]")
        return None
    elif token:
        ret = save_api_key(token)
        if ret.value == 2:
            console.print(
                "[yellow bold]WARNING[/]\nWe noticed that there is already an API key configured that does not match the provided one, do you want to overwrite? [y/n]"
            )
            ans = console.input(">>> ")
            if ans.strip().lower() in ("yes", "y", "yse"):
                save_api_key(token, overwrite=True)
            else:
                console.print("[green bold]Authentication successful[/]")
                return None
        console.print("[green bold]Authentication successful[/]")
        return None


@app.command(name="parse", help="Parse a spreadsheet file with LlamaSheets.")
def parse(
    file: Annotated[
        str,
        Option(
            "--file", "-f", help="Path to the file to process. Must be .xls/.xlsx. "
        ),
    ],
    sheets: Annotated[
        list[str] | None,
        Option(
            "-s",
            "--sheet",
            help="Name of the sheet(s) to process within the file. Can be used multiple times. Defaults to processing all available sheets.",
        ),
    ] = None,
    include_hidden_cells: Annotated[
        bool,
        Option(
            "--include-hidden-cells/--no-include-hidden-cells",
            help="Whether to include hidden cells when extracting regions from the spreadsheet.",
        ),
    ] = True,
    extraction_range: Annotated[
        str | None,
        Option(
            "--extraction-range",
            help="A1 notation of the range to extract a single region from. If None, the entire sheet is used.",
        ),
    ] = None,
    generate_additional_metadata: Annotated[
        bool,
        Option(
            "--generate-additional-metadata/--no-generate-additional-metadata",
            help="Whether to generate additional metadata (title, description) for each extracted region.",
        ),
    ] = True,
    use_experimental_processing: Annotated[
        bool,
        Option(
            "--use-experimental-processing/--no-use-experimental-processing",
            help="Enables experimental processing. Accuracy may be impacted.",
        ),
    ] = False,
    flatten_hierarchical_tables: Annotated[
        bool,
        Option(
            "--flatten-hierarchical-tables/--no-flatten-hierarchical-tables",
            help="Return a flattened dataframe when a detected table is recognized as hierarchical.",
        ),
    ] = False,
    table_merge_sensitivity: Annotated[
        Literal["strong", "weak"],
        Option(
            "--table-merge-sensitivity",
            help="Influences how likely similar-looking regions are merged into a single table. Useful for spreadsheets that either have sparse tables (strong merging) or many distinct tables close together (weak merging).",
        ),
    ] = "strong",
    save_csv: Annotated[
        bool,
        Option(
            "--save-csv/--no-save-csv",
            help="Whether or not to save the results as CSV files in the `parsed/` folder. Defaults to true.",
        ),
    ] = True,
):
    api_key = load_api_key()
    if isinstance(api_key, AuthStatus):
        console.print(
            "[bold red]Error: you are not authenticated. Run `sheets auth` before using the command again[/]"
        )
        raise Exit(1)
    if not Path(file).exists() or not Path(file).is_file():
        console.print(f"[bold red]No such file: {file}[/]")
        raise Exit(2)
    print_logo()
    try:
        console.log(f"[bold]Starting to process {file}[/]")
        results = asyncio.run(
            parse_spreadsheet(
                api_key=api_key,
                file=file,
                sheets=sheets,
                generate_additional_metadata=generate_additional_metadata,
                include_hidden_cells=include_hidden_cells,
                extraction_range=extraction_range,
                use_experimental_processing=use_experimental_processing,
                flatten_hierarchical_tables=flatten_hierarchical_tables,
                table_merge_sensitivity=table_merge_sensitivity,
                save_csv=save_csv,
            )
        )
        console.log(f"[green bold]Finished processing {file}[/]")
        console.print()
        for result in results:
            console.print(Markdown(f"### {result.metadata['title']}"))
            if (des := result.metadata["description"]) is not None:
                console.print(Markdown(f"**Description**:\n\n{des}"))
            if save_csv:
                console.print(
                    Markdown(
                        f"Saved under `parsed/{result.metadata['title'].lower().replace(' ', '_')}.csv`"
                    )
                )
            console.print(Markdown(result.table))
            console.print("\n\n---\n\n")
        return None
    except Exception as e:
        console.print(f"[bold red]An error occured: {e}[/]")
        raise Exit(3)
