import asyncio

import aiohttp
import pandas as pd
import requests
from fpl import FPL
from sklearn.preprocessing import OneHotEncoder

from fplrl.tools.squad import select_squad
from fplrl.tools.transfers import select_transfers


async def my_team(user_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email='chapmajw@gmail.com', password='12Collingwood!')
        user = await fpl.get_user(user_id)
        team = await user.get_team()
        bank = await user.get_transfers_status()
    return team, bank


def main(team_id):
    team, transfer = asyncio.run(my_team(team_id))
    team_df = pd.DataFrame(team)
    team_df.rename(columns={'element': 'id'}, inplace=True)
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(url)
    json = r.json()
    elements_df = pd.DataFrame(json['elements'])
    elements_df.set_index('id', inplace=True)
    team_df.set_index('id', inplace=True)
    # Add a selection variable
    elements_df['selected'] = 0
    elements_df['selected'].loc[team_df.index] = 1
    # Add costs for your team
    elements_df['sell_cost'] = elements_df['now_cost'].copy()
    elements_df['now_cost'].loc[team_df.index] = team_df.purchase_price.values
    elements_df['sell_cost'].loc[team_df.index] = team_df.selling_price.values
    OH_club = OneHotEncoder(sparse=False).fit_transform(elements_df.team.values.astype(int).reshape((-1, 1)))
    OH_position = OneHotEncoder(sparse=False).fit_transform(
        elements_df.element_type.values.astype(int).reshape((-1, 1)))
    expected_points = elements_df.ep_next.values.astype(float).reshape((-1, 1))
    purchase_value = elements_df.now_cost.values
    sale_value = elements_df.sell_cost.values
    current_squad = elements_df.selected.values
    selections, subs, captain, team_expected_points = select_squad(
        OH_club,
        OH_position,
        expected_points,
        purchase_value,
        sale_value, current_squad=current_squad)
    print('starting XI: \n', elements_df[['first_name', 'second_name']][selections == 1])
    print('Captain: \n', elements_df[['first_name', 'second_name']][captain == 1])
    print('Subs: \n', elements_df[['first_name', 'second_name']][subs == 1])
    print(f'{team_expected_points} expected points')



if __name__ == '__main__':
    main(5697036)
