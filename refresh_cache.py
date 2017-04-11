import os
import pickle
import sc2gamedata

_access_token = os.environ["BATTLE_NET_ACCESS_TOKEN"]


def refresh_cache(access_token: str):
    for region in sc2gamedata.regions():
        game_data = sc2gamedata.get_game_data(access_token, region=region)
        with open("{}.data".format(region), "wb") as file:
            pickle.dump(game_data, file)

        if region == "us":
            sc2gamedata.save_to_cache(game_data)


if __name__ == '__main__':
    refresh_cache(_access_token)
