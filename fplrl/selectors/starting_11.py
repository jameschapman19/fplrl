import numpy as np

from fplrl.selectors.squad import select_squad


def select_starting_11(squad: np.ndarray, club: np.ndarray, position: np.ndarray, expected_points: np.ndarray,
                      cost: np.ndarray):
    filter=np.nonzero(squad)
    return select_squad(club[filter], position[filter], expected_points[filter], cost[filter])
