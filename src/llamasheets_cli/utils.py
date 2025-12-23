import json
import os

from dataclasses import dataclass
from base64 import b64encode, b64decode
from typing import TypedDict, Literal
from llama_cloud_services.beta.sheets import (
    LlamaSheets,
    SpreadsheetParsingConfig,
    SpreadsheetResultType,
)
from pathlib import Path
from enum import IntEnum


class AuthStatus(IntEnum):
    ALREADY_AUTHENTICATED = 0
    NEW_AUTHENTICATED = 1
    KEY_CONFLICT = 2
    UNAUTHENTICATED = 3


CONFIG_FILE = Path.cwd() / ".llamasheets.config.json"


class SpreadsheetMetadata(TypedDict):
    title: str
    description: str | None


@dataclass
class SpreadsheetRepr:
    table: str
    metadata: SpreadsheetMetadata


async def parse_spreadsheet(
    api_key: str,
    file: str,
    sheets: list[str] | None,
    include_hidden_cells: bool,
    extraction_range: str | None,
    generate_additional_metadata: bool,
    use_experimental_processing: bool,
    flatten_hierarchical_tables: bool,
    table_merge_sensitivity: Literal["weak", "strong"],
    save_csv: bool,
) -> list[SpreadsheetRepr]:
    config = SpreadsheetParsingConfig(
        sheet_names=sheets,
        include_hidden_cells=include_hidden_cells,
        extraction_range=extraction_range,
        generate_additional_metadata=generate_additional_metadata,
        use_experimental_processing=use_experimental_processing,
        flatten_hierarchical_tables=flatten_hierarchical_tables,
        table_merge_sensitivity=table_merge_sensitivity,
    )
    client = LlamaSheets(api_key=api_key)
    result = await client.aextract_regions(file, config=config)
    if save_csv:
        os.makedirs("parsed/", exist_ok=True)
    reprs: list[SpreadsheetRepr] = []
    untitled = 0
    for region in result.regions:
        df = await client.adownload_region_as_dataframe(
            result.id,
            region.region_id,
            result_type=SpreadsheetResultType.TABLE,
        )
        if region.title is None:
            untitled += 1
            title = f"untitled_region_{untitled}"
        else:
            title = region.title
        metadata = SpreadsheetMetadata(title=title, description=region.description)
        md_table = df.to_markdown()
        if save_csv:
            df.to_csv(
                os.path.join("parsed", title.lower().replace(" ", "_") + ".csv"),
                index=False,
            )
        reprs.append(SpreadsheetRepr(table=md_table, metadata=metadata))
    return reprs


def save_api_key(api_key: str, overwrite: bool = False) -> AuthStatus:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        if (enc_token := data.get("api_key")) is not None:
            token = b64decode(enc_token).decode("utf-8")
            if token != api_key:
                if not overwrite:
                    return AuthStatus.KEY_CONFLICT
                else:
                    enc_apikey = b64encode(bytes(api_key, encoding="utf-8")).decode(
                        "utf-8"
                    )
                    data["api_key"] = enc_apikey
                    with open(CONFIG_FILE, "w") as f:
                        json.dump(data, f, indent=2)
                    return AuthStatus.NEW_AUTHENTICATED
            else:
                return AuthStatus.ALREADY_AUTHENTICATED
        else:
            enc_apikey = b64encode(bytes(api_key, encoding="utf-8")).decode("utf-8")
            data["api_key"] = enc_apikey
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=2)
            return AuthStatus.NEW_AUTHENTICATED
    else:
        enc_apikey = b64encode(bytes(api_key, encoding="utf-8")).decode("utf-8")
        data = {"api_key": enc_apikey}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return AuthStatus.NEW_AUTHENTICATED


def load_api_key() -> AuthStatus | str:
    if not CONFIG_FILE.exists():
        return AuthStatus.UNAUTHENTICATED
    else:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        if (enc_token := data.get("api_key")) is not None:
            token = b64decode(enc_token).decode("utf-8")
            return token
        else:
            return AuthStatus.UNAUTHENTICATED
