import pandas as pd
import matplotlib.pyplot as plt

BOARD_LENGTH = 96

def main():
    df = pd.read_csv("tests/cuts.csv")
    # create list of cuts
    cut_list = createCutList(df)
    print(cut_list)
    plotCuts()


def createBoards(cut_list) -> pd.DataFrame:
    ...

def plotCuts() -> None:

    data = {
        "Category": ["Cat A", "Cat B", "Cat C"],
        "Data 1": [10, 20, 30],
        "Data 2": [15, 25, 35],
        "Data 3": [5, 10, 15],
    }

    data_df = pd.DataFrame(data)

    data_df.set_index("Category", inplace=True)
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
