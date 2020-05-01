import os
import numpy as np
import pandas as pd


def read_csv(name):
    try:
        solar = pd.read_excel(os.path.join(os.getcwd(), name), sheet_name=0, dtype='float64')
    except:
        solar = pd.read_csv(os.path.join(os.getcwd(), name), sheet_name=0, dtype='float64')
    length = len(solar)
    data = np.array(solar, 'float32')
    return data, length


def write_excel(data, name):
    temp = pd.DataFrame(data)
    temp.to_excel(name, index=False)


def main():
    data, nos = read_csv("Sample.xlsx")
    # data - dataset as an array, nos - number of space objects


    # Logical Modules


    write_excel(data, "xyz.xlsx")


if __name__ == '__main__':
    main()

