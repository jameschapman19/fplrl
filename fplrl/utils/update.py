from fplrl.utils.collector import merge_gw, collect_gw
from fplrl.utils.getters import get_data
from fplrl.utils.global_merger import merge_data
from fplrl.utils.understat import parse_epl_data


def update_data():
    collect_gw(3)
    merge_gw(3, 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
    merge_data()
