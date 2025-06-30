import pytest
import pandas as pd
from cutlist_app.cutlist import (
    addSomeNumbers,
    createBoards,
    createCutList,
)


# to run pytest:    uv run pytest
@pytest.fixture
def numbers():
    return [1, 2, 3]


@pytest.fixture
def expected_cutlist():
    return pd.DataFrame(
        {
            "length": [60.0, 15.0, 15.0, 60.0, 60.0, 45.0, 45.0],
            "board_id": [1, 1, 1, 2, 3, 4, 4],
            "cut_id": ["60.0", "15.0", "15.0", "60.0", "60.0", "45.0", "45.0"],
        }
    )


def test_addSomeNumbers(numbers):
    assert addSomeNumbers(numbers) == 6
    assert addSomeNumbers([2, 3, 4]) == 9


def test_createBoards(expected_cutlist):
    cut_list = [60.0, 60.0, 60.0, 45.0, 45.0, 15.0, 15.0]
    result_df = createBoards(cut_list, 96)
    pd.testing.assert_frame_equal(result_df, expected_cutlist)


def test_createCutList(expected_cutlist):
    df = pd.DataFrame(
        {
            "Description": ["example1", "example2", "example3"],
            "Quantity": [3, 2, 2],
            "Length": [60.0, 15.0, 45.0],
            "W x H": ["2x4", "2x4", "2x4"],
        }
    )
    result_df = createCutList(df, 96)
    pd.testing.assert_frame_equal(result_df, expected_cutlist)
