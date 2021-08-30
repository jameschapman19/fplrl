import numpy as np
from sklearn.preprocessing import OneHotEncoder

from fplrl.tools.squad import select_squad

n_clubs = 20
n_players_per_club = 21

club = np.random.randint(0, n_clubs, size=(n_clubs * n_players_per_club, 1))
OH_club = OneHotEncoder(sparse=False).fit_transform(club)
position = np.random.randint(0, 4, size=(n_clubs * n_players_per_club, 1))
OH_position = OneHotEncoder(sparse=False).fit_transform(position)
expected_points = np.random.normal(4, 2, size=(n_clubs * n_players_per_club, 1))
cost = np.random.uniform(4.0, 13.0, size=(n_clubs * n_players_per_club, 1))
value = 100

selections, subs, captain = select_squad(OH_club, OH_position, expected_points, cost, value)

print()
