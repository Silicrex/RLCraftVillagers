import os
from database import DB


def refresh_display(msg=''):
    os.system('cls')
    print('Commands: '
          'list; '
          'find <enchant>; '
          'check <cost> <enchant>, ..; '
          'villagers; '
          'add <villager name>, <cost1 enchant1>, <c2 e2>, <c3 e3>; '
          'remove <villager name>\n')  # Header
    if msg:
        print(msg + '\n')


def get_enchant_name(enchant_input: list):
    if enchant_input[-1].isnumeric():
        if len(enchant_input) == 1:
            refresh_display('Invalid enchant')
            return False
        return ' '.join(enchant_input[:-1])
    else:
        return ' '.join(enchant_input)


def get_enchant_level(enchant_input: list):
    if enchant_input[-1].isnumeric():
        if len(enchant_input) == 1:
            refresh_display('Invalid enchant')
            return False
        return int(enchant_input[-1])
    else:
        return 1


def get_enchant_list(input_list):
    # Takes list of string inputs '{cost} {enchant_name}' and returns a list of each item turned into a dict
    enchant_list = []
    for split in [x.split() for x in input_list]:
        if len(split) < 2:
            refresh_display('Be sure to include all costs and enchant names')
            return False
        if not split[0].isnumeric():
            refresh_display('Be sure to include cost first')
            return False
        cost = int(split[0])
        enchant_name = get_enchant_name(split[1:])
        level = get_enchant_level(split[1:])
        enchant_list.append({'name': enchant_name, 'level': level, 'cost': cost})
    return enchant_list


def print_enchant(enchant_name, *, extra_newline=True):
    enchants = DB['enchants']
    enchant = enchants[enchant_name]
    best_level = enchant['best_level']
    best_rate = enchant['best_rate']
    print(f"[{enchant_name.title()} {best_level['level']}] @"
          f" {best_level['cost']} ems --> {best_level['villager_name']}", end='')
    if enchant['best_level']['level'] == enchant['best_rate']['level']:  # The highest-level enchant is also best rate
        print()
    else:
        scaled_cost = int(get_rate(best_rate['level'], best_rate['cost']) * get_lv1(best_level['level']))
        print(f" || best rate: [{enchant_name.title()} {best_rate['level']}] @ "
              f"{best_rate['cost']} ems <Scaled {scaled_cost} ems> --> {best_rate['villager_name']}")

    if extra_newline:
        print()


def check_best_level(enchant_name, level, cost, *, print_mode=True):
    enchants = DB['enchants']
    best_level = enchants[enchant_name]['best_level']
    if level > best_level['level']:
        if print_mode:
            print(f"! [{enchant_name.title()} {level}] is a new highest level! "
                  f"(prev: [{enchant_name.title()} {best_level['level']}])")
        return True
    elif level == best_level['level'] and get_rate(level, cost) < get_rate(best_level['level'], best_level['cost']):
        if print_mode:
            print(f"~! [{enchant_name.title()} {level}] is not a higher level but is a "
                  f"better rate for the best level @ {cost} ems compared to prev @ {best_level['cost']} ems")
        return True
    else:
        if print_mode:
            print(f"[{enchant_name.title()} {level}] is not a higher level "
                  f"(cur: [{enchant_name.title()} {best_level['level']}])")
        return False


def check_best_rate(enchant_name, level, cost, *, print_mode=True):
    enchants = DB['enchants']
    best_rate = enchants[enchant_name]['best_rate']
    highest_level = max(level, enchants[enchant_name]['best_level']['level'])
    cur_cost = int(get_lv1(highest_level) * get_rate(best_rate['level'], best_rate['cost']))
    new_cost = int(get_lv1(highest_level) * get_rate(level, cost))
    scaling = highest_level > enchants[enchant_name]['best_level']['level'] or highest_level > level
    if new_cost < cur_cost:
        if print_mode:
            print(f"! [{enchant_name.title()} {level}] @ {cost} ems is a new best rate! "
                  f"(prev: [{enchant_name.title()} {best_rate['level']}] @ {best_rate['cost']} ems)", end='')
            if not scaling:
                print()
            else:
                print(f" <Scaled> (prev {cur_cost} ems) vs (new {new_cost} ems) for "
                      f"[{enchant_name.title()} {highest_level}]")
        return True
    elif new_cost == cur_cost and level > best_rate['level']:
        if print_mode:
            print(f"~! [{enchant_name.title()} {level}] @ {cost} ems is not a better rate but is a "
                  f"better level for the best rate compared to prev of [{enchant_name.title()} {best_rate['level']}]")
        return True
    else:
        if print_mode:
            print(f"[{enchant_name.title()} {level}] @ {cost} ems is not a better rate "
                  f"(cur: [{enchant_name.title()} {best_rate['level']}] @ {best_rate['cost']} ems)", end='')
            if not scaling:
                print()
            else:
                print(f" <Scaled> (cur {cur_cost} ems) vs (new {new_cost} ems) for "
                      f"[{enchant_name.title()} {highest_level}]")
        return False


def check_villager(villager_name):
    villagers = DB['villagers']
    villager_data = villagers[villager_name]
    for value in villager_data.values():
        if value['is_best_level'] or value['is_best_rate']:
            return True
    return False


def get_villagers_with_enchant(enchant_name):
    res = set()
    for villager_name, value in DB['villagers'].items():
        for full_enchant_name in value:
            test_enchant_name = get_enchant_name(full_enchant_name.split())
            if test_enchant_name == enchant_name:
                res.add(villager_name)
    return res


def get_enchant_best_level(villager_list, enchant_name):
    # Returns None or a replacement best_level dict
    villagers = DB['villagers']
    new_level = 0
    new_cost = float('inf')
    new_villager_name = None
    for villager_name in villager_list:
        villager_data = villagers[villager_name]
        for full_enchant_name in villager_data:
            test_enchant_name = get_enchant_name(full_enchant_name.split())
            test_level = get_enchant_level(full_enchant_name.split())
            test_cost = villager_data[full_enchant_name]['cost']
            if test_enchant_name != enchant_name:
                continue
            if test_level > new_level or test_level == new_level and test_cost < new_cost:
                new_level = test_level
                new_cost = test_cost
                new_villager_name = villager_name
    if new_villager_name is None:
        return None
    else:
        return {'villager_name': new_villager_name, 'level': new_level, 'cost': new_cost}


def get_enchant_best_rate(villager_list, enchant_name):
    # Returns None or a replacement best_rate dict
    villagers = DB['villagers']
    new_level = 0
    new_cost = float('inf')
    new_villager_name = None
    new_rate = float('inf')
    for villager_name in villager_list:
        villager_data = villagers[villager_name]
        for full_enchant_name in villager_data:
            test_enchant_name = get_enchant_name(full_enchant_name.split())
            test_level = get_enchant_level(full_enchant_name.split())
            test_cost = villager_data[full_enchant_name]['cost']
            if test_enchant_name != enchant_name:
                continue
            test_rate = get_rate(test_level, test_cost)
            if not new_villager_name or test_rate < new_rate or test_rate == new_rate and test_level > new_level:
                new_level = test_level
                new_cost = test_cost
                new_villager_name = villager_name
    if new_villager_name is None:
        return None
    else:
        return {'villager_name': new_villager_name, 'level': new_level, 'cost': new_cost}


def get_rate(level, cost):
    # cost per lvl 1
    return cost / 2**(level-1)


def get_lv1(level):
    return 2**(level-1)


def replace_best_level(villager_name, enchant_name, level, cost):
    # Returns previous villager name
    return replace('best_level', villager_name, enchant_name, level, cost)


def replace_best_rate(villager_name, enchant_name, level, cost):
    # Returns previous villager name
    return replace('best_rate', villager_name, enchant_name, level, cost)


def replace(dict_name, villager_name, enchant_name, level, cost):
    # Returns previous villager name
    enchants = DB['enchants']
    villagers = DB['villagers']
    best_dict = enchants[enchant_name][dict_name]

    # Set new values
    prev_level = best_dict['level']
    prev_full_enchant_name = f"{enchant_name} {prev_level}"
    best_dict['level'] = level
    best_dict['cost'] = cost
    prev_villager = best_dict['villager_name']
    if villager_name != prev_villager:
        best_dict['villager_name'] = villager_name
        for enchant, value in villagers[prev_villager].items():  # Unset previous villager's 'best' bool
            if enchant == prev_full_enchant_name:
                value[f"is_{dict_name}"] = False  # ie is_best_level or is_best_rate
                break
    return prev_villager


def sorted_dict(dictionary):
    return dict(sorted(dictionary.items()))
