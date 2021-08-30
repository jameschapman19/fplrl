from fplrl.utils.collector import merge_gw
from fplrl.utils.getters import get_data
from fplrl.utils.global_merger import merge_data
from fplrl.utils.understat import parse_epl_data


def update_data():
    data = get_data()
    parse_epl_data('utils/2021-22/understat')
    merge_gw(3, 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
    merge_data()
