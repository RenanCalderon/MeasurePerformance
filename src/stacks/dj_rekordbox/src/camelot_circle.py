
def add_camelot_key_column(df, field):
    camelot_keys = []
    for tonality in field:
        camelot_key = get_camelot_key_from_tonality(tonality)
        camelot_keys.append(camelot_key)

    df["camelot"] = camelot_keys


def get_camelot_key_from_tonality(tonality):
    key_map = camelot_key_mapping()
    camelot_key = next((key for key, value in key_map.items() if tonality in value), None)
    return camelot_key


def camelot_key_mapping():
    key_map = {
        "1A": ["Abm", "G#m"],
        "2A": ["Ebm", "D#m"],
        "3A": ["Bbm", "A#m"],
        "4A": ["Fm"],
        "5A": ["Cm"],
        "6A": ["Gm"],
        "7A": ["Dm"],
        "8A": ["Am"],
        "9A": ["Em"],
        "10A": ["Bm"],
        "11A": ["F#m", "Gbm"],
        "12A": ["Dbm", "C#m"],
        "1B": ["B"],
        "2B": ["F#", "Gb"],
        "3B": ["Db", "C#"],
        "4B": ["Ab", "G#"],
        "5B": ["Eb", "D#"],
        "6B": ["Bb", "A#"],
        "7B": ["F"],
        "8B": ["C"],
        "9B": ["G"],
        "10B": ["D"],
        "11B": ["A"],
        "12B": ["E"],
    }
    return key_map
