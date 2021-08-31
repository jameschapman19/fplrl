import json
from datetime import datetime

import requests

from fplrl.utils.collector import merge_gw, collect_gw
from fplrl.utils.getters import get_data
from fplrl.utils.global_scraper import parse_data


def get_recent_gameweek_id(data):
    """
    Get's the most recent gameweek's ID.
    """

    gameweeks = data['events']

    now = datetime.utcnow()
    for gameweek in gameweeks:
        next_deadline_date = datetime.strptime(gameweek['deadline_time'], '%Y-%m-%dT%H:%M:%SZ')
        if next_deadline_date > now:
            return gameweek['id'] - 1
        else:
            return gameweek['id']


def update_data():
    data = get_data()
    gw = get_recent_gameweek_id(data)
    parse_data()
    collect_gw(gw)
    merge_gw(gw, 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
