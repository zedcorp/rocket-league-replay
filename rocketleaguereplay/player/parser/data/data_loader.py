data = None

data_start = 0


def load_data(filename):
    import json

    from player.parser.data.actor_data import parse_actor_data
    from player.parser.data.object_numbers import \
        parse_player_info, parse_game_event_num
    from player.parser.parser.frames import load_frames
    from player.parser.util.extra_info import parse_pressure, \
        parse_possession, fix_pressure_possession_values, parse_total_boost

    global data

    with open(filename) as data_file:
        data = json.load(data_file)

    parse_actor_data()
    parse_player_info()
    parse_game_event_num()

    load_frames()

    parse_pressure()
    parse_possession()
    parse_total_boost()

    fix_pressure_possession_values()


def get_data():
    return data
