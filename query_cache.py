import bisect
import pprint
import sc2gamedata

_league_names = [
    "bronze",
    "silver",
    "gold",
    "platinum",
    "diamond",
    "master"
]

_tier_names = [
    "bronze 3",
    "bronze 2",
    "bronze 1",
    "silver 3",
    "silver 2",
    "silver 1",
    "gold 3",
    "gold 2",
    "gold 1",
    "platinum 3",
    "platinum 2",
    "platinum 1",
    "diamond 3",
    "diamond 2",
    "diamond 1",
    "master 3",
    "master 2",
    "master 1"
]


def _distribution_to_proportion(distribution: list) -> list:
    total = sum(distribution)
    return [pop / total for pop in distribution]


def _group_tiers_by_leagues(tiers: list) -> list:
    return [
        sum((pop for i, pop in enumerate(tiers) if _tier_names[i].startswith(league_name)))
        for league_name
        in _league_names]


def _readable_proportions(proportions: list) -> list:
    return ["{0:.2f}%".format(proportion * 100) for proportion in proportions]


def print_mmr_proportions(game_data: sc2gamedata.GameData):
    tier_bounds = [tier["max_rating"] for tier in game_data.tiers()]

    mmr_distribution = [0] * len(game_data.tiers())
    for team in game_data.teams():
        mmr_tier_id = min(bisect.bisect_left(tier_bounds, team["rating"]), len(tier_bounds) - 1)
        mmr_distribution[mmr_tier_id] += 1
    mmr_proportions_by_tier = _distribution_to_proportion(mmr_distribution)
    mmr_proportions_by_league = _group_tiers_by_leagues(mmr_proportions_by_tier)
    readable_mmr_proportions_by_league = _readable_proportions(mmr_proportions_by_league)
    print("mmr proportions")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(list(zip(_league_names, readable_mmr_proportions_by_league)))
    print("\n")


def print_league_proportions(game_data: sc2gamedata.GameData):
    pp = pprint.PrettyPrinter(indent=4)
    tier_distribution = [0] * len(game_data.tiers())
    for ladder in game_data.ladders():
        division = game_data.divisions()[ladder["division_index"]]
        tier_distribution[division["tier_id"]] += len(ladder["team"])
    tier_proportions = _distribution_to_proportion(tier_distribution)
    league_proportions = _group_tiers_by_leagues(tier_proportions)
    readable_league_proportions = _readable_proportions(league_proportions)
    print("league proportions:")
    pp.pprint(list(zip(_league_names, readable_league_proportions)))
    print("\n")


def print_all_inspiration_mmr(game_data: sc2gamedata.GameData, clan_name: str):
    pp = pprint.PrettyPrinter(indent=4)

    all_mmrs = sorted([team['rating'] for team in game_data.teams()])

    clan_members = [
        team
        for team
        in game_data.teams()
        if "clan_link" in team["member"][0] and team["member"][0]["clan_link"]["clan_name"] == clan_name]

    sorted_clan_members = sorted(clan_members, key=lambda team: team['rating'], reverse=True)

    member_battle_tags = (team["member"][0]["character_link"]["battle_tag"]
                          for team
                          in sorted_clan_members
                          if "character_link" in team["member"][0])
    member_races = (team["member"][0]["played_race_count"][0]["race"]["en_US"] for team in sorted_clan_members)
    member_mmrs = (team["rating"] for team in sorted_clan_members)
    member_percentiles = (1 - bisect.bisect(all_mmrs, team["rating"]) / len(all_mmrs) for team in sorted_clan_members)
    pretty_member_percentiles = ("{0:.2f}%".format(percentile * 100) for percentile in member_percentiles)

    print("All Inspiration MMRs")
    pp.pprint(list(zip(member_battle_tags, member_races, member_mmrs, pretty_member_percentiles)))
    print("\n")


def query_cache():
    game_data = sc2gamedata.load_cache()

    print_league_proportions(game_data)
    print_mmr_proportions(game_data)
    print_all_inspiration_mmr(game_data, "All Inspiration")


if __name__ == '__main__':
    query_cache()
