import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

BOARD_LENGTH = 96


def main():
    df = pd.read_csv("tests/cuts.csv")
    # create list of cuts
    cut_list = createCutList(df)
    boards_df = createBoards(cut_list)
    plotCuts(boards_df)
    startStreamlit()


def startStreamlit(): ...


def createBoards(cut_list) -> pd.DataFrame:
    remaining_board_length = BOARD_LENGTH
    boards = []
    board = []
    while len(cut_list) > 0:
        if min(cut_list) > remaining_board_length:
            boards.append(board)
            board = []
            remaining_board_length = BOARD_LENGTH
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


def plotCuts(boards_df) -> None:
    st.write(boards_df)
    st.bar_chart(boards_df, x="board_id", y="length", color="cut_id", horizontal=True)


def createCutList(df) -> list:
    quantity_list = list(df["quantity"])
    length_list = list(df["length"])
    cut_list = []
    for i in range(len(quantity_list)):
        quantity = quantity_list[i]
        length = length_list[i]
        for _ in range(quantity):
            cut_list.append(length)
    cut_list.sort(reverse=True)
    return cut_list


if __name__ == "__main__":
    main()
