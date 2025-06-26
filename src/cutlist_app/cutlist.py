import pandas as pd
import streamlit as st
import os

st.set_page_config(
    layout="wide", page_title="Cut List", page_icon=":material/carpenter:"
)


def hideUploader():
    st.session_state.hide_uploader = True


def addRowToDataframe(user_input):
    if "pieces" not in st.session_state:
        st.session_state.pieces = user_input
    else:
        st.session_state.pieces = pd.concat(
            [st.session_state.pieces, user_input], ignore_index=True
        )
    st.success(f"Added {user_input["Description"][0]}")


# [ ]: add function to remove a row from table based on description
def removeRowFromDataframe(): ...


def reset_button_click():
    del st.session_state.pieces
    del st.session_state.hide_uploader


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def createBoards(cut_list, MAX_BOARD_LENGTH) -> pd.DataFrame:
    remaining_board_length = MAX_BOARD_LENGTH
    boards = []
    board = []
    while len(cut_list) > 0:
        if min(cut_list) > remaining_board_length:
            boards.append(board)
            board = []
            remaining_board_length = MAX_BOARD_LENGTH
        else:
            for i in range(len(cut_list)):
                if cut_list[i] <= remaining_board_length:
                    remaining_board_length -= cut_list[i]
                    board.append(cut_list.pop(i))
                    break
    if len(board) > 0:
        boards.append(board)
    boards_df = pd.DataFrame(columns=["length", "board_id", "cut_id"])
    for board_id, board_list in enumerate(boards):
        for board_len in board_list:
            boards_df.loc[len(boards_df)] = [board_len, board_id + 1, str(board_len)]
    return boards_df


def createCutList(df, MAX_BOARD_LENGTH) -> pd.DataFrame:
    quantity_list = list(df["Quantity"])
    length_list = list(df["Length"])
    cut_list = []
    for i in range(len(quantity_list)):
        quantity = quantity_list[i]
        length = length_list[i]
        for _ in range(quantity):
            cut_list.append(length)
    cut_list.sort(reverse=True)
    cut_list = createBoards(cut_list, MAX_BOARD_LENGTH)
    return cut_list


if "max_length" not in st.session_state:
    st.session_state.max_length = 96
    st.session_state.old_value = st.session_state.max_length


# Logo and Title
_, col2, col3 = st.columns([1, 1, 3])
with col2:
    st.image(
        os.path.join(os.getcwd(), "static", "logo.png"),
        use_container_width=False,
        width=200,
    )
with col3:
    st.title("Cut List")
st.divider()
# Sidebar
with st.sidebar:
    if "hide_uploader" not in st.session_state:
        uploaded_file = st.file_uploader("Upload", type="csv", key="file-uploaded")
        if uploaded_file is not None and "reset-btn" not in st.session_state:
            st.session_state.pieces = pd.read_csv(uploaded_file)
            st.session_state.hide_uploader = True
    with st.container(border=True):
        st.title("Settings")
        with st.form("settings_form"):
            col1, _, col3 = st.columns([0.4, 0.35, 0.25])
            with col1:
                # [ ]: Make kerf measurement work
                kerf_toggle = st.toggle("Include Kerf")
            with col3:
                update_button = st.form_submit_button("Update")
            max_length_input = st.number_input(
                "Max Length (in):",
                min_value=12,
                max_value=144,
                step=12,
                key="max_length",
            )
            # [ ]: add check to verify new length isn't shorter than longest piece
            if update_button:
                if st.session_state.max_length != st.session_state.old_value:
                    st.success(
                        f"Max length updated from {st.session_state.old_value} to {max_length_input}."
                    )
                    st.session_state.old_value = st.session_state.max_length
    with st.container(border=True):
        st.title("Bill of Materials")
        # Inputs
        with st.form(key="user_input_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                description_input = st.text_input("Description:")
                wxh_input = st.selectbox(
                    "Width x Height:",
                    ["1x2", "1x4", "2x2", "2x4", "2x6", "2x8", "2x12", "4x4"],
                )
            with col2:
                quantity_input = st.number_input(
                    "Qty:", min_value=1, max_value=1000, value=None, step=1
                )
                length_input = st.number_input(
                    "Length (in):",
                    min_value=0.016,
                    max_value=float(st.session_state.max_length),
                    value=None,
                )
            with col3:
                for _ in range(7):
                    st.write("")
                bom_add_button = st.form_submit_button("Add", on_click=hideUploader)
            if bom_add_button and length_input and description_input and quantity_input:
                user_input = pd.DataFrame(
                    {
                        "Description": [description_input],
                        "Quantity": [quantity_input],
                        "Length": [length_input],
                        "W x H": [wxh_input],
                    }
                )
                addRowToDataframe(user_input)
            else:
                st.warning("Please fill in all fields.")
        if "pieces" in st.session_state:
            st.dataframe(st.session_state.pieces, hide_index=True)
    if "pieces" in st.session_state:
        # [x]: fix: reset button won't clear displayed dataframe on reset when only adding csv
        reset_button = st.button(
            "Restart Cut List", on_click=reset_button_click, key="reset-btn"
        )
        csv = convert_df(st.session_state.pieces)
        st.download_button("Export BOM", csv, "bom.csv", "text/csv", key="download-csv")


# Charts
if "pieces" in st.session_state:
    for each_wxh in st.session_state.pieces["W x H"].unique():
        with st.container(border=True):
            relevant_pieces_df = st.session_state.pieces[
                st.session_state.pieces["W x H"] == each_wxh
            ]
            cut_list_per_wxh = createCutList(
                relevant_pieces_df, st.session_state.max_length
            )
            st.subheader(each_wxh)
            st.bar_chart(
                cut_list_per_wxh,
                x="board_id",
                y="length",
                color="cut_id",
                horizontal=True,
                x_label="Length (in)",
                y_label="Board",
                use_container_width=False,
                width=1000,
                height=400,
            )

else:
    _, col, _ = st.columns([2, 1, 2])
    with col:
        st.subheader("Create a BOM")
