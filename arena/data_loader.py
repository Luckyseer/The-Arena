import json

try:
    with open("data/items.json", "r") as items:
        item_data_shop = json.load(items)  # List of all shops and their items
        item_data = {"weapons": [], "armours": [], "accessories": [], "consumables": []}
        for shop in item_data_shop:
            item_data["weapons"].extend(item_data_shop[shop]["weapons"])
            item_data["armours"].extend(item_data_shop[shop]["armours"])
            item_data["accessories"].extend(item_data_shop[shop]["accessories"])
            item_data["consumables"].extend(item_data_shop[shop]["consumables"])
        weapons = item_data["weapons"]
    with open("data/monsters.json", "r") as monsters:
        monster_data = json.load(monsters)
    with open("data/soundeffects.json", "r") as sounds:
        sound_effects = json.load(sounds)
    with open("data/animations.json", "r") as anims:
        animations = json.load(anims)
    with open("data/skills.json", "r") as skills:
        skills = json.load(skills)
    with open("data/sequences.json", "r") as sequences:
        sequences = json.load(sequences)
    with open("data/dialogue.json", "r") as dialogue:
        dialogues = json.load(dialogue)
    try:
        with open("data/battles.json", "r") as battles_file:
            battles = json.load(battles_file)
    except FileNotFoundError:
        battles = {}
except EOFError or IOError:
    print(
        "Could not load item/monster/sound data, Make sure they are in the folder with the game"
    )
    raise FileNotFoundError


__all__ = [
    "item_data_shop",
    "item_data",
    "weapons",
    "monster_data",
    "sound_effects",
    "animations",
    "skills",
    "sequences",
    "dialogues",
    "battles",
]
