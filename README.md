# LlamaSheets CLI

A command-line tool for parsing spreadsheet files using [LlamaSheets](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/).  
Supports `.xls` and `.xlsx` files, with options for advanced extraction and metadata generation.

<div align="center">
    <img src="./image.png" alt="LlamaSheets logo" width=300, height=300>
</div>

## Installation

```bash
pip install llamasheets-cli
```

Or, with uv, you can do directly:

```bash
uv tool install llamasheets-cli
```

## Usage

### 1. Authenticate

Before using the CLI, you must authenticate with your LlamaCloud API key.

```bash
sheets auth --token <YOUR_API_KEY>
```
Or, for more secure input:
```bash
sheets auth --stdin
```
You will be prompted to enter your API key securely.

> _If an API key is already configured, you will be warned and asked if you want to overwrite it._

### 2. Parse a Spreadsheet

Once authenticated, you can parse a spreadsheet:

```bash
sheets parse --file path/to/your.xlsx
```

**Options**

- `--file`, `-f` **(required)**: Path to the `.xls` or `.xlsx` file to process.
- `--sheet`, `-s`: Name of the sheet(s) to process. Can be used multiple times. Defaults to all sheets.
- `--include-hidden-cells/--no-include-hidden-cells`: Include hidden cells in extraction. Default: `--include-hidden-cells`
- `--extraction-range`: A1 notation of the range to extract (e.g., `A1:D20`). Default: entire sheet.
- `--generate-additional-metadata/--no-generate-additional-metadata`: Generate extra metadata (title, description) for each region. Default: `--generate-additional-metadata`
- `--use-experimental-processing/--no-use-experimental-processing`: Enable experimental processing. Default: `--no-use-experimental-processing`
- `--flatten-hierarchical-tables/--no-flatten-hierarchical-tables`: Flatten hierarchical tables. Default: `--no-flatten-hierarchical-tables`
- `--table-merge-sensitivity [strong|weak]`: How aggressively to merge similar regions. Default: `strong`
- `--save-csv/--no-save-csv`: Save results as CSV files in the `parsed/` folder. Default: `--save-csv`

**Example**

```bash
sheets parse -f data.xlsx -s Sheet1 -s Sheet2 --extraction-range A1:D20 --no-save-csv
```

**Output**

- Results are displayed in your terminal with markdown formatting.
- If `--save-csv` is enabled, CSV files are saved in the `parsed/` directory, named after the extracted region titles.


## License and Contributions

This project is distributed under the [MIT License](./LICENSE).

Contributions are welcome and encouraged, and should follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).