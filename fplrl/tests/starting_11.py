import numpy as np
from sklearn.preprocessing import OneHotEncoder

from fplrl.selectors.squad import select_squad
from fplrl.selectors.starting_11 import select_starting_11

n_clubs = 20
n_players_per_club = 21

club = np.random.randint(0, n_clubs, size=(n_clubs * n_players_per_club, 1))
OH_club = OneHotEncoder(sparse=False).fit_transform(club)
position = np.random.randint(0, 4, size=(n_clubs * n_players_per_club, 1))
OH_position = OneHotEncoder(sparse=False).fit_transform(position)
expected_points = np.random.normal(4, 2, size=(n_clubs * n_players_per_club, 1))
cost = np.random.uniform(4.0, 13.0, size=(n_clubs * n_players_per_club, 1))
value = 100
current_squad = np.sum(select_squad(OH_club, OH_position, expected_points, cost, value), axis=0)
selections, subs, captain = select_starting_11(current_squad, OH_club, OH_position, expected_points, cost)

print()
