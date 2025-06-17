import pandas as pd
import matplotlib.pyplot as plt

BOARD_LENGTH = 96


def main():
    df = pd.read_csv("tests/cuts.csv")
    # create list of cuts
    cut_list = createCutList(df)
    print(cut_list)
    boards = createBoards(cut_list)
    print(boards)
    plotCuts()


def createBoards(cut_list) -> list:
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
    return boards


def plotCuts() -> None:

    data = {
        "Boards": ["Board 1", "Board 2", "Board 3"],
        "Data 1": [10, 20, 30],
        "Data 2": [15, 25, 35],
        "Data 3": [5, 10, 15],
    }

    data_df = pd.DataFrame(data)
    print(data_df)

    data_df.set_index("Boards", inplace=True)
    data_df.plot(kind="barh", stacked=True, figsize=(8, 6))

    plt.xlabel("Length")
    plt.title("Cut List")
    plt.legend()
    plt.show()


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
