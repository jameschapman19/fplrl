import pandas as pd

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
    previous_seasons = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/cleaned_merged_seasons.csv',
                                   encoding='cp1252').iloc[:, 1:]
    current_season = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws/merged_gw.csv')
    current_season['season_x'] = '2021-22'
    all_data = pd.concat([previous_seasons, current_season])
    old_data = all_data[all_data.season_x.isin(seasons[:-1])]
    current_data = all_data[all_data.season_x == seasons[-1]]
    current_data = current_data[current_data.GW < gw]
    return pd.concat([old_data, current_data])[FEATURES]


def get_data_next_gw(season=16, gw=2):
    previous_seasons = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/cleaned_merged_seasons.csv',
                                   encoding='cp1252').iloc[:, 1:]
    current_season = pd.read_csv('C:/Users/chapm/PycharmProjects/fplrl/data/2021-22/gws/merged_gw.csv')
    current_season['season_x'] = '2021-22'
    all_data = pd.concat([previous_seasons, current_season])
    next_gw_data = all_data[all_data.season_x == f'20{season}-{season + 1}']
    next_gw_data = next_gw_data[next_gw_data.GW == gw]
    return next_gw_data[PREDICTIONS]


def main():
    features = get_data_at_time(21, 3)
    pred_features = get_data_next_gw(21, 3)
    print()


if __name__ == '__main__':
    main()
