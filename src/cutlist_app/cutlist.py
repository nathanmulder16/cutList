import pandas as pd
import streamlit as st
import os

st.set_page_config(layout="wide", page_title="Cut List", page_icon=":material/carpenter:")
BOARD_LENGTH_TOTAL = 96


def main():
    df = pd.read_csv("tests/cuts.csv")
    # create list of cuts
    cut_list = createCutList(df)
    blank_cut_list_df = pd.DataFrame(columns=["description", "quantity", "length", "wxh"])
    startStreamlit(cut_list, blank_cut_list_df)


def startStreamlit(boards_df, blank_cut_list_df):
    # Logo and Title
    _ , col2, col3 = st.columns([1,1,3])
    with col2:
        st.image(os.path.join(os.getcwd(), "static", "logo.png"), use_container_width=False, width=200)
    with col3:   
        st.title("Cut List")
    st.divider()
    # Sidebar
    with st.sidebar:
        #TODO: add functionality to uploader
        st.file_uploader("Upload")
        with st.container(border=True):
            st.title("Settings")
            #TODO: Make kerf measurement work
            st.toggle("Include Kerf")

            #TODO: Make max length transfer to BOARD_LENGTH
            max_length = st.number_input("Max Length (in):", min_value=12, max_value=144, value=96, step=12)

        with st.container(border=True):
            st.title("Bill of Materials")
            # Inputs
            with st.form(key="user_input_form", clear_on_submit=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    description_input = st.text_input("Description:")
                    wxh_input = st.selectbox("Width x Height:", ["1x2", "1x4","2x2", "2x4", "2x6", "2x8", "2x12", "4x4"])
                with col2:
                    quantity_input = st.number_input("Qty:", min_value=1, max_value=1000, value=1, step=1)
                    length_input = st.number_input("Length (in):")

                user_input_df = pd.DataFrame({
                    "description": [description_input],
                    "quantity": [quantity_input],
                    "length": [length_input],
                    "wxh": [wxh_input]
                })
                st.dataframe(user_input_df, hide_index=True)

                

                with col3:
                    for _ in range(7):
                        st.write("")
                    st.form_submit_button("Add")
                    # st.form_submit_button("Add", on_click=addRowToDataframe(blank_cut_list_df, user_input_df))
            # Display Table
            counted_columns = boards_df.groupby("length")["length"].value_counts()
            st.dataframe(counted_columns)
            st.dataframe(blank_cut_list_df)
        #TODO: make this restart button reset everything
        st.button("Restart Cut List")

        #TODO: create button to export to save for later
    
    
    
    # Charts
    # create number of charts based on differing WxH
    for _ in range(2):
        with st.container(border=True):
            st.subheader("2x4")
            st.bar_chart(
                boards_df,
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

def addRowToDataframe(orig_df, user_input_df):
    if orig_df.empty:
        return user_input_df
    else:
        orig_df = pd.concat([orig_df, user_input_df], ignore_index=True)
    return orig_df
    
    
def createBoards(cut_list) -> pd.DataFrame:
    remaining_board_length = BOARD_LENGTH_TOTAL
    boards = []
    board = []
    while len(cut_list) > 0:
        if min(cut_list) > remaining_board_length:
            boards.append(board)
            board = []
            remaining_board_length = BOARD_LENGTH_TOTAL
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


def createCutList(df) -> pd.DataFrame:
    quantity_list = list(df["quantity"])
    length_list = list(df["length"])
    cut_list = []
    for i in range(len(quantity_list)):
        quantity = quantity_list[i]
        length = length_list[i]
        for _ in range(quantity):
            cut_list.append(length)
    cut_list.sort(reverse=True)
    cut_list = createBoards(cut_list)
    return cut_list


if __name__ == "__main__":
    main()
