from fplrl.utils.collector import merge_gw, collect_gw
from fplrl.utils.getters import get_data
from fplrl.utils.global_merger import merge_data
from fplrl.utils.global_scraper import parse_data
from fplrl.utils.understat import parse_epl_data
import json
import requests
import datetime

def get_recent_gameweek_id():
    """
    Get's the most recent gameweek's ID.
    """

    data = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/')
    data = json.loads(data.content)

    gameweeks = data['events']

    now = datetime.utcnow()
    for gameweek in gameweeks:
        next_deadline_date = datetime.strptime(gameweek['deadline_time'], '%Y-%m-%dT%H:%M:%SZ')
        if next_deadline_date > now:
            return gameweek['id'] - 1

def update_data():
    data = get_data()
    with open('raw.json', 'w') as outf:
        json.dump(data, outf)
    parse_data()
    collect_gw(get_recent_gameweek_id())
    merge_gw(get_recent_gameweek_id(), 'C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws')
