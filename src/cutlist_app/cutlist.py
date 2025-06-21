import pandas as pd
import streamlit as st

BOARD_LENGTH_TOTAL = 96


def main():
    df = pd.read_csv("tests/cuts.csv")
    # create list of cuts
    cut_list = createCutList(df)
    startStreamlit(cut_list)


def startStreamlit(boards_df):
    st.title("Cut List App")
    st.sidebar.title("Bill of Materials")
    counted_columns = boards_df.groupby("length")["length"].value_counts()
    st.sidebar.table(counted_columns)
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
        width=700,
        height=400,
    )


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
