import pandas as pd
from fplrl.data_utils.collector import merge_all_gws, merge_gw
from fplrl.data_utils.global_merger import merge_data


def update_data():
    # merge_all_gws(3, 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
    merge_gw(3, 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
    merge_data()


def main():
    update_data()


if __name__ == '__main__':
    main()
