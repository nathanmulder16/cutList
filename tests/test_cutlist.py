import pytest
import pandas as pd
import streamlit as st
from cutlist_app.cutlist import (
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


def test_createBoards(expected_cutlist):
    st.session_state.kerf_toggle = False
    cut_list = [60.0, 60.0, 60.0, 45.0, 45.0, 15.0, 15.0]
    result_df = createBoards(cut_list, 96)
    pd.testing.assert_frame_equal(result_df, expected_cutlist)


def test_createBoards_1():
    st.session_state.kerf_toggle = True
    cut_list = [60.0, 36.0]
    purchased_length = 96
    result_df = createBoards(cut_list, purchased_length)
    expected_cutlist = pd.DataFrame(
        {
            "length": [60.0, 0.125, 36.0, 0.125],
            "board_id": [1, 1, 2, 2],
            "cut_id": ["60.0", "kerf", "36.0", "kerf"],
        }
    )
    pd.testing.assert_frame_equal(result_df, expected_cutlist)


def test_createCutList(expected_cutlist):
    st.session_state.kerf_toggle = False
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
