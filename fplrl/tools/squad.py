import cvxpy as cp
import numpy as np


def select_squad(club: np.ndarray, position: np.ndarray, expected_points: np.ndarray, purchase_value: np.ndarray,
                 squad_value=100000, optimise='points'):
    """
    Selects the best possible XI given one

    :param club: one-hot encoded club
    :param position: one-hot encoded club
    :param expected_points: expected points
    :param purchase_value: player cost
    :param squad_value: squad value
    :return: selections, subs, captain
    """

    # Define optimisation variables
    selections = cp.Variable(club.shape[0], integer=True)
    subs = cp.Variable(club.shape[0], integer=True)
    captain = cp.Variable(club.shape[0], integer=True)
    # Objective:maximise points
    if optimise == 'points':
        objective = cp.Maximize(selections @ expected_points + 2 * captain @ expected_points)
    # Objective:maximise points
    elif optimise == 'random':
        objective = cp.Maximize(0)
    else:
        raise ValueError('Choose points or random')
    # Constraints
    constraints = [
        # Captain, Selections and Subs need to be unique
        (captain + selections + subs) <= 1,
        # no more than 3 from each club
        (selections + subs) @ club <= 3,
        # no more than 1 starting and 1 sub keeper
        (captain + selections) @ position[:, 0] <= 1,
        subs @ position[:, 0] <= 1,
        # no more than 5 defenders, 5 midfielders, 3 forwards
        (captain + selections + subs) @ position[:, 1] <= 5,
        (captain + selections + subs) @ position[:, 2] <= 5,
        (captain + selections + subs) @ position[:, 3] <= 3,
        # starting no fewer than 3 defenders, 3 midfielders, 1 forwards
        (captain + selections) @ position[:, 1] >= 3,
        (captain + selections) @ position[:, 2] >= 3,
        (captain + selections) @ position[:, 3] >= 1,
        # no more than 1 captain, 10 starters
        cp.sum(captain) <= 1,
        cp.sum(selections) <= 10,
        # 15 in the squad
        cp.sum(captain + selections + subs) >= 15,
        # don't exceed budget
        (captain + selections + subs) @ purchase_value <= squad_value,
        # no 'negative' selections
        selections >= 0,
        subs >= 0,
        captain >= 0,
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    team_expected_points = selections.value @ expected_points + 2 * captain.value @ expected_points
    return np.round(selections.value), np.round(subs.value), np.round(captain.value), team_expected_points
