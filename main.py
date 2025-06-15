import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("cuts.csv")    
    # create list of cuts
    cut_list = createCutList(df)
    print(cut_list)

def createCutList(df) -> list:
    quantity_list = list(df["quantity"])
    length_list = list(df["length"])
    cut_list = []
    for i in range(len(quantity_list)):
        quantity = quantity_list[i]
        length = length_list[i]
        for _ in range(quantity):
            cut_list.append(length)
    return cut_list


if __name__ == "__main__":
    main()
