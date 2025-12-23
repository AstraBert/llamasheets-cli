import os
import pytest
import pandas as pd

from llamasheets_cli.utils import (
    AuthStatus,
    save_api_key,
    load_api_key,
    CONFIG_FILE,
    parse_spreadsheet,
)


def test_save_api_key() -> None:
    if CONFIG_FILE.exists():
        os.remove(CONFIG_FILE)
    ret = save_api_key("hello")
    assert CONFIG_FILE.exists()
    assert ret.value == 1
    ret = save_api_key("hello")
    assert ret.value == 0
    ret = save_api_key("bye")
    assert ret.value == 2
    ret = save_api_key("bye", overwrite=True)
    assert ret.value == 1
    os.remove(CONFIG_FILE)


def test_load_api_key() -> None:
    if CONFIG_FILE.exists():
        os.remove(CONFIG_FILE)
    ret = load_api_key()
    assert isinstance(ret, AuthStatus)
    assert ret.value == 3
    save_api_key("hello")
    ret = load_api_key()
    assert isinstance(ret, str)
    assert ret == "hello"
    os.remove(CONFIG_FILE)


@pytest.mark.asyncio
@pytest.mark.skipif(
    condition=(os.getenv("LLAMA_CLOUD_API_KEY") is None),
    reason="LLAMA_CLOUD_API_KEY not available",
)
async def test_parse_spreadsheet() -> None:
    file = "tests/testfiles/toys.xlsx"
    try:
        result = await parse_spreadsheet(
            api_key=os.getenv("LLAMA_CLOUD_API_KEY", ""),
            file=file,
            sheets=None,
            generate_additional_metadata=True,
            include_hidden_cells=True,
            extraction_range=None,
            use_experimental_processing=False,
            flatten_hierarchical_tables=False,
            table_merge_sensitivity="strong",
            save_csv=True,
        )
    except Exception:
        result = None
    assert result is not None
    assert len(result) == 1
    assert not result[0].metadata["title"].startswith("untitled")
    assert result[0].metadata["description"] is not None
    assert os.path.exists(
        os.path.join(
            "./parsed", result[0].metadata["title"].lower().replace(" ", "_") + ".csv"
        )
    )
    df = pd.read_csv(
        os.path.join(
            "./parsed", result[0].metadata["title"].lower().replace(" ", "_") + ".csv"
        )
    )
    assert df.to_markdown() == result[0].table
