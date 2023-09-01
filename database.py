import json
from pathlib import Path

# Villagers are guaranteed exactly 3 enchants each
# villager = {'full_enchant_name': {'is_best_level': Bool, 'is_best_rate': Bool, 'cost': int}, ...}
# enchant = {'best_level': {'villager_name': str, 'level': int, 'cost': int},
#         'best_rate': {'villager_name': str, 'level': int, 'cost': int}}


def load_data():
    if not Path('data.json').is_file():
        template = {'enchants': {}, 'villagers': {}}
        with open('data.json', 'w') as file:
            json.dump(template, file, indent=4)
        return template
    with open('data.json', 'r') as file:
        return json.load(file)


def update():
    with open('data.json', 'w') as file:
        json.dump(DB, file, indent=4)


DB = load_data()
