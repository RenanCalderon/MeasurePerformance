
def add_camelot_key_column(df, field):
    key_map = camelot_key_mapping()
    camelot_keys = []

    for tonality in field:
        camelot_key = get_camelot_key_from_tonality(tonality)
        camelot_keys.append(camelot_key)

    df["Camelot"] = camelot_keys


def get_camelot_key_from_tonality(tonality):
    key_map = camelot_key_mapping()
    camelot_key = next((key for key, value in key_map.items() if value == tonality), None)
    return camelot_key


def camelot_key_mapping():
    key_map = {
        "1A": "Abm",
        "2A": "Ebm",
        "3A": "Bbm",
        "4A": "Fm",
        "5A": "Cm",
        "6A": "Gm",
        "7A": "Dm",
        "8A": "Am",
        "9A": "Em",
        "10A": "Bm",
        "11A": "F#m",
        "12A": "Dbm",
        "1B": "B",
        "2B": "F#",
        "3B": "Db",
        "4B": "Ab",
        "5B": "Eb",
        "6B": "Bb",
        "7B": "F",
        "8B": "C",
        "9B": "G",
        "10B": "D",
        "11B": "A",
        "12B": "E",
    }
    return key_map
