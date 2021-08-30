import cvxpy as cp
import numpy as np


def select_transfers(current_squad: np.ndarray, club: np.ndarray, position: np.ndarray, expected_points: np.ndarray,
                     purchase_value: float, sale_value: float, bank: float,
                     free_transfers_available=2):
    # Define optimisation variables
    selections = cp.Variable(club.shape[0], integer=True)
    subs = cp.Variable(club.shape[0], integer=True)
    captain = cp.Variable(club.shape[0], integer=True)
    transfers_in = cp.Variable(club.shape[0], integer=True)
    transfers_out = cp.Variable(club.shape[0], integer=True)
    hits = cp.Variable(1, integer=True)
    # Objective:maximise points
    objective = cp.Maximize(selections @ expected_points + 2 * captain @ expected_points - 4 * hits)
    # Constraints
    constraints = [
        (current_squad + transfers_in) - (captain + selections + subs) >= 0,
        (current_squad + transfers_out) - (captain + selections + subs) >= 0,
        cp.sum((current_squad + transfers_in) - (captain + selections + subs)) <= free_transfers_available + hits,
        cp.sum((current_squad + transfers_out) - (captain + selections + subs)) <= free_transfers_available + hits,
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
        # (captain + selections + subs) @ cost <= squad_value,
        current_squad @ purchase_value + transfers_in @ purchase_value - transfers_out @ sale_value <= current_squad @ sale_value + bank,
        # nonneg
        selections >= 0,
        subs >= 0,
        captain >= 0,
        transfers_in >= 0,
        transfers_out >= 0,
        hits >= 0
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    team_expected_points = selections.value @ expected_points + 2 * captain.value @ expected_points
    return np.round(selections.value), np.round(subs.value), np.round(
        captain.value), transfers_in.value, transfers_out.value, team_expected_points, np.round(hits.value)
