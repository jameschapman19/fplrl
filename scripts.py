import numpy as np
from sklearn.preprocessing import OneHotEncoder

from fplrl.tools.squad import select_squad
from fplrl.tools.transfers import select_transfers

n_clubs = 20
n_players_per_club = 21

current_season = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/utils/2021-22/gws/merged_gw.csv')

club = np.random.randint(0, n_clubs, size=(n_clubs * n_players_per_club, 1))
OH_club = OneHotEncoder(sparse=False).fit_transform(club)
position = np.random.randint(0, 4, size=(n_clubs * n_players_per_club, 1))
OH_position = OneHotEncoder(sparse=False).fit_transform(position)
expected_points = np.random.normal(5, 4, size=(n_clubs * n_players_per_club, 1))
purchase_value = np.random.uniform(4.0, 13.0, size=(n_clubs * n_players_per_club, 1))
sale_value = purchase_value
value = 100.0
selections, subs, captain, team_expected_points_before = select_squad(OH_club, OH_position, expected_points,
                                                                      purchase_value, value, optimise='random')
current_squad = np.sum((selections, subs, captain), axis=0)
bank = 0.0
selections, subs, captain, transfers_in, transfers_out, team_expected_points_after, hits = select_transfers(
    current_squad, OH_club,
    OH_position,
    expected_points,
    purchase_value,
    sale_value, bank,
    free_transfers_available=2)
