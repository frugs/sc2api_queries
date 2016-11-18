import os
import sc2gamedata

_access_token = os.environ["BATTLE_NET_ACCESS_TOKEN"]


def refresh_cache(access_token: str):
    ladder_data = sc2gamedata.download_ladder_data(access_token)
    sc2gamedata.save_to_cache(ladder_data)

if __name__ == '__main__':
    refresh_cache(_access_token)
