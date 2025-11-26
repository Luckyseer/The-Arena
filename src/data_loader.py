import json
import os

def load_json(filename):
    # Assuming run from root directory
    path = os.path.join('data', filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find {path}")
    with open(path, 'r') as f:
        return json.load(f)

def load_game_data():
    try:
        items_shop = load_json('items.json')
        
        item_data = {
            "weapons": [],
            "armours": [],
            "accessories": [],
            "consumables": []
        }
        for shop in items_shop:
            item_data['weapons'].extend(items_shop[shop]['weapons'])
            item_data['armours'].extend(items_shop[shop]['armours'])
            item_data['accessories'].extend(items_shop[shop]['accessories'])
            item_data['consumables'].extend(items_shop[shop]['consumables'])
        
        monsters = load_json('monsters.json')
        sounds = load_json('soundeffects.json')
        animations = load_json('animations.json')
        skills = load_json('skills.json')
        sequences = load_json('sequences.json')
        dialogues = load_json('dialogue.json')
        
        return {
            'item_data': item_data,
            'monster_data': monsters,
            'sound_effects': sounds,
            'animations': animations,
            'skills': skills,
            'sequences': sequences,
            'dialogues': dialogues,
            'raw_item_data': items_shop
        }
    except (EOFError, IOError) as e:
        print('Could not load item/monster/sound data, Make sure they are in the folder with the game')
        raise e
