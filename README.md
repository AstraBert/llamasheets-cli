# LlamaSheets CLI

CLI application for [LlamaSheets](https://developers.llamaindex.ai/python/cloud/llamasheets/getting_started/)

## Usage

Authenticate with the `auth` command:

```sh
sheets auth [OPTIONS]
```

Authorize LlamaCloud usage with an API key.

**Options:**

- `--token`, `-t` &lt;TEXT&gt;  
    LlamaCloud API key. Prefer using `--stdin` for inputting your token from standard input (more secure).
- `--stdin`  
    Input your LlamaCloud API key from standard input.

Parse a spreadsheet once you are authenticated with the `parse` command:

```sh
sheets parse [OPTIONS]
```

Parse a spreadsheet file with LlamaSheets.

**Options:**

- `--file`, `-f` &lt;TEXT&gt;  
    Path to the file to process. Must be `.xls` or `.xlsx`. **[required]**
- `--sheet`, `-s` &lt;TEXT&gt;  
    Name of the sheet(s) to process within the file. Can be used multiple times. Defaults to all sheets.
- `--include-hidden-cells` / `--no-include-hidden-cells`  
    Whether to include hidden cells when extracting regions from the spreadsheet.  
    Default: `--include-hidden-cells`
- `--extraction-range` &lt;TEXT&gt;  
    A1 notation of the range to extract a single region from. If not set, the entire sheet is used.
- `--generate-additional-metadata` / `--no-generate-additional-metadata`  
    Whether to generate additional metadata (title, description) for each extracted region.  
    Default: `--generate-additional-metadata`
- `--use-experimental-processing` / `--no-use-experimental-processing`  
    Enables experimental processing. Accuracy may be impacted.  
    Default: `--no-use-experimental-processing`
- `--flatten-hierarchical-tables` / `--no-flatten-hierarchical-tables`  
    Return a flattened dataframe when a detected table is recognized as hierarchical.  
    Default: `--no-flatten-hierarchical-tables`
- `--table-merge-sensitivity` [strong|weak]  
    Influences how likely similar-looking regions are merged into a single table.  
    Use `strong` for sparse tables, `weak` for many distinct tables close together.  
    Default: `strong`
- `--save-csv` / `--no-save-csv`  
    Whether to save the results as CSV files in the `parsed/` folder.  
    Default: `--save-csv`