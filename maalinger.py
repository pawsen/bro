#!/usr/bin/env python3

import csv

# import numpy as np
from itertools import chain
import itertools
import re
from typing import TypedDict

DataInfo = TypedDict(
    "DataInfo", {"fname": str, "nmeas": int, "npasses": int, "meta": str}
)


def float_or_int_checker(el: str) -> bool:
    "Check if the string is a number"
    pattern = r"^[-+]?(\d+(\.\d*)?|\.\d+)$"
    if re.match(pattern, el):
        return True
    return False


def flatten(forest) -> list:
    "Flatten a list of list, but row-wise, so cannot be used here"
    return [leaf for tree in forest for leaf in tree]
    # return [x for xs in xss for x in xs]


def print_flat(val: list) -> None:
    "Print a list vertical. For easy copy-paste into excel"
    tmp = [str(x) for x in val]
    print("\n".join(tmp))


def load_data(fname: str) -> list:
    """read data from csv file and return a stacked 1d list.

    The measurements are saved column-wise, example
    "No", "A", "B", "C"
    "1" , "8", "4", "9"
    "2" , "6", "6", "5"
    "3" , "7", "5",

    The output is then
    [8,6,7,4,6,5,9,5]
    """

    val = []
    with open("data/" + fname, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for i, row in enumerate(spamreader):
            # discard first coloumn, it's only storing the row number
            val.append([r if float_or_int_checker(r) else None for r in row[1:] ])


        # transpose data
        val = itertools.zip_longest(*val)
        # flatten and remove None's
        val = list(
            float(x) for x in itertools.chain.from_iterable(val) if x is not None
        )
    return val


def format_data(d: DataInfo, val: list):
    total_rows = d["nmeas"] * d["npasses"]
    points_pr_row = len(val) / total_rows
    # did we get the correct number of measurents
    is_correct = len(val) % total_rows == 0

    print(f"fname: {d['fname']}")
    print(f"{d['meta']}")
    print(f"number of measurement per go: {d['nmeas']} ")
    print(f"total number of measurements: {len(val)}")
    print(f"number of measuments pr row {points_pr_row}")
    print()
    points_pr_row = int(points_pr_row)
    for j in range(d["npasses"]):
        for i in range(d["nmeas"]):
            print(f"pass {j}. Measurement {i}")
            # slice, eg. take every second if there are two meassurements per "go".
            # ex: starting from 1: val[1::2]
            x = val[i :: d["nmeas"]]
            if is_correct:
                print_flat(x[points_pr_row*j:points_pr_row*(j+1)])
            else:
                print("number of measurements does not add up. You're on your own")
                print_flat(x)
            print("###\n\n")


data: list[DataInfo] = [
    # west facing(A)
    # # south
    # {"fname": "001.csv", "nmeas": 2, "npasses": 2, "meta": "A, south"},
    # # middle
    # {"fname": "002.csv", "nmeas": 2, "npasses": 2, "meta": "A, middle"},
    # # north
    # {"fname": "003.csv", "nmeas": 2, "npasses": 2, "meta": "A, north"},

    # # under bridge, South-east
    # {
    #     "fname": "005.csv",
    #     "nmeas": 5,
    #     "npasses": 1,
    #     "meta": "Under bridge, South east. ie 1: under bride, 2: lowest C, 3: 2nd lowest C, 4: I beam transverse, 5: I beam upright",
    # },
    # # under bridge, North-east
    # {
    #     "fname": "006.csv",
    #     "nmeas": 5,
    #     "npasses": 1,
    #     "meta": "Under bridge, North east. ie 1: under bride, 2: lowest C, 3: 2nd lowest C, 4: I beam transverse, 5: I beam upright",
    # },

    # {"fname": "007.csv", "nmeas": 2, "npasses": 2, "meta": "A, north"},
    # {"fname": "008.csv", "nmeas": 3, "npasses": 1, "meta": "B: 2,1 and AB top"},
    {"fname": "009.csv", "nmeas": 3, "npasses": 1, "meta": "C: 2,1 and CD top"},
]

for d in data:
    val = load_data(d["fname"])
    # print(val)
    format_data(d, val)

# np.random.uniform(low=0, high=10, size=10)
# np.round(np.random.normal(loc=8,scale=0.1, size=10), decimals=2)
# print("\n".join([str(k) for k in x]))
