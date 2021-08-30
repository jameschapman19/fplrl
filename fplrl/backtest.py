import pandas as pd
from fplrl.data_utils.collector import merge_all_gws
from fplrl.utils import update_data

CURRENT_SEASON = 21
PREDICTIONS = ['total_points', 'bps']
FEATURES = ['position', 'assists',
            'bonus', 'bps', 'clean_sheets', 'creativity', 'element',
            'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes',
            'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards',
            'saves', 'selected', 'team_a_score', 'team_h_score', 'threat',
            'total_points', 'transfers_balance', 'transfers_in', 'transfers_out',
            'was_home', 'yellow_cards', 'GW']


def get_data_at_time(season=16, gw=2):
    seasons = [f'20{s}-{s + 1}' for s in range(16, season + 1)]
    all_data = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/cleaned_merged_seasons.csv').iloc[:, 1:]
    old_data = all_data[all_data.season_x.isin(seasons[:-1])]
    current_data = all_data[all_data.season_x == seasons[-1]]
    current_data = current_data[current_data.GW < gw]
    return pd.concat([old_data, current_data])[FEATURES]


def get_data_next_gw(season=16, gw=2):
    all_data = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/cleaned_merged_seasons.csv')
    next_gw_data = all_data[all_data.season_x == f'20{season}-{season + 1}']
    next_gw_data = next_gw_data[next_gw_data.GW == gw]
    return next_gw_data[PREDICTIONS]


def main():
    update_data()
    features = get_data_at_time(21, 3)
    pred_features = get_data_next_gw(21, 3)
    print(pred_features)
    print()


if __name__ == '__main__':
    main()
