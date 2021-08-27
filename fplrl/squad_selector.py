import cvxpy as cp
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def select_squad(club, position, expected_points, cost, value, discount_factor, squad=True):
    if squad:
        n_players = 15
        keepers = 2
    else:
        n_players = 11
        keepers = 1
    selection = cp.Variable(club.shape[0])
    captain = cp.Variable(club.shape[0])
    objective = cp.Maximize(selection @ expected_points + captain @ expected_points)
    constraints = [
        selection @ club <= 3,
        selection @ position[:, 0] <= keepers,
        selection @ position[:, 1] <= 5,
        selection @ position[:, 2] <= 5,
        selection @ position[:, 3] <= 3,
        cp.sum(selection) <= n_players,
        selection @ cost <= value,
        selection <= 1,
        selection >= 0,
        captain <= 1,
        captain >= 0,
        cp.sum(captain) <= 1,
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return selection.value, captain.value


n_clubs = 20
n_players_per_club = 21

club = np.random.randint(0, n_clubs, size=(n_clubs * n_players_per_club, 1))
OH_club = OneHotEncoder(sparse=False).fit_transform(club)
position = np.random.randint(0, 4, size=(n_clubs * n_players_per_club, 1))
OH_position = OneHotEncoder(sparse=False).fit_transform(position)
expected_points = np.random.normal(4, 2, size=(n_clubs * n_players_per_club, 1))
cost = np.random.uniform(4.0, 13.0, size=(n_clubs * n_players_per_club, 1))
value = 100

squad, captain = select_squad(OH_club, OH_position, expected_points, cost, value)

print()
