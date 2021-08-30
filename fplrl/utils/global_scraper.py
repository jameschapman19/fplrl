from fplrl.utils.cleaners import *
from fplrl.utils.collector import collect_gw, merge_gw
from fplrl.utils.getters import *
from fplrl.utils.parsers import *
from fplrl.utils.understat import parse_epl_data


def parse_data():
    """ Parse and store all the utils
    """
    season = '2021-22'
    base_filename = 'C:/Users/chapm/PycharmProjects/fplrl/data/' + season + '/'
    print("Getting utils")
    data = get_data()
    print("Parsing summary utils")
    parse_players(data["elements"], base_filename)
    xPoints = []
    for e in data["elements"]:
        xPoint = {}
        xPoint['id'] = e['id']
        xPoint['xP'] = e['ep_this']
        xPoints += [xPoint]
    gw_num = 0
    events = data["events"]
    for event in events:
        if event["is_current"] == True:
            gw_num = event["id"]
    print("Cleaning summary utils")
    clean_players(base_filename + 'players_raw.csv', base_filename)
    print("Getting fixtures utils")
    fixtures(base_filename)
    print("Getting teams utils")
    parse_team_data(data["teams"], base_filename)
    print("Extracting player ids")
    id_players(base_filename + 'players_raw.csv', base_filename)
    player_ids = get_player_ids(base_filename)
    num_players = len(data["elements"])
    player_base_filename = base_filename + 'players/'
    gw_base_filename = base_filename + 'gws/'
    print("Extracting player specific utils")
    for i, name in player_ids.items():
        player_data = get_individual_player_data(i)
        parse_player_history(player_data["history_past"], player_base_filename, name, i)
        parse_player_gw_history(player_data["history"], player_base_filename, name, i)
    if gw_num > 0:
        print("Writing expected points")
        with open(os.path.join(gw_base_filename, 'xP' + str(gw_num) + '.csv'), 'w+') as outf:
            w = csv.DictWriter(outf, ['id', 'xP'])
            w.writeheader()
            for xp in xPoints:
                w.writerow(xp)
        print("Collecting gw scores")
        collect_gw(gw_num, player_base_filename, gw_base_filename, base_filename)
        print("Merging gw scores")
        merge_gw(gw_num, gw_base_filename)
    understat_filename = base_filename + 'understat'
    parse_epl_data(understat_filename)


def fixtures(base_filename):
    data = get_fixtures_data()
    parse_fixtures(data, base_filename)
