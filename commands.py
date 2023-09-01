from utility import *
from database import DB, update

# Every function is passed a list of args (user input minus the command)


def list_cmd(_):
    # ex: list
    # Assumes data is pre-sorted
    enchants = DB['enchants']
    if not enchants:
        refresh_display('There are no enchants')
        return
    refresh_display()
    for enchant_name in enchants:
        print_enchant(enchant_name, extra_newline=False)
    print()


def find_cmd(args):
    # ex: find ash destroyer
    if not args:
        refresh_display('Missing argument')
        return

    if not (enchant_name := get_enchant_name(args)):
        return
    refresh_display()
    enchants = DB['enchants']
    if enchant_name not in enchants:
        found = False
        for test_enchant_name in enchants:
            if test_enchant_name.startswith(enchant_name):
                enchant_name = test_enchant_name
                found = True
                break
        if not found:
            print('Nothing found\n')
            return
    print_enchant(enchant_name)


def check_cmd(args):
    # ex: check 10 fire aspect 2, 30 education 3
    enchants = DB['enchants']
    if len(args) < 2:
        refresh_display('Missing argument')
        return
    parsed = ' '.join(args).split(', ')
    if not (enchant_list := get_enchant_list(parsed)):
        return
    for enchant_data in enchant_list:
        enchant_name = enchant_data['name']
        level = enchant_data['level']
        cost = enchant_data['cost']
        refresh_display()
        if enchant_name not in enchants:
            print(f'{enchant_name.title()} {level} is a new enchant!\n')
            continue
        check_best_level(enchant_name, level, cost)
        check_best_rate(enchant_name, level, cost)
        print()


def villagers_cmd(_):
    # ex: villagers
    villagers = DB['villagers']
    used_villagers = []
    unused_villagers = []

    if not villagers:
        refresh_display('There are no villagers')
        return

    refresh_display()
    for villager_name in villagers:
        if check_villager(villager_name):
            used_villagers.append(villager_name)
        else:
            unused_villagers.append(villager_name)

    if unused_villagers:
        for villager_name in unused_villagers:
            print(f'{villager_name} does not contribute any bests!')
        print()

    for villager_name in used_villagers:
        data = villagers[villager_name]
        out = []
        print(f"{villager_name}: ", end='')
        for full_enchant_name in data:
            is_best_level = data[full_enchant_name]['is_best_level']
            is_best_rate = data[full_enchant_name]['is_best_rate']
            if not (is_best_level or is_best_rate):
                continue
            if is_best_level and is_best_rate:
                text = '(LEVEL/RATE)'
            elif is_best_level:
                text = '(LEVEL)'
            else:
                text = '(RATE)'
            out.append(f"[{full_enchant_name.title()}] @ {data[full_enchant_name]['cost']} ems {text}")
        print(', '.join(out))
    print()


def add_cmd(args):
    # ex: add bob, 10 ash destroyer, 5 mending, 7 supreme sharpness 5
    # Names are forced lowercase, enchant names are automatically adjusted during print

    # Process input
    if len(args) < 7:
        refresh_display('Missing arguments')
        return
    parsed = ' '.join(args).split(', ')  # ie [bob, 10 ash destroyer, 5 mending, 7 supreme sharpness 5]
    if len(parsed) != 4:
        refresh_display('Format args like: <name>, <cost1> <enchant1>, <cost2> <enchant2>, <cost3> <enchant3>')
        return
    villagers = DB['villagers']
    enchants = DB['enchants']
    villager_name = parsed[0]

    # Validate name
    if villager_name in villagers:
        refresh_display('Villager name already in use')
        return

    # Validate & format enchants
    if not (enchant_list := get_enchant_list(parsed[1:])):  # Get list of dicts representing enchants
        return

    # Iterate over enchants, perform comparisons, and update data
    refresh_display()
    villager = {}
    replaced_villagers = []  # To check for if still contributing a best after update
    new_enchant = False
    for enchant_data in enchant_list:
        enchant_name = enchant_data['name']
        level = enchant_data['level']
        cost = enchant_data['cost']
        full_enchant_name = f"{enchant_name} {level}"
        villager.update({full_enchant_name: {'is_best_level': False, 'is_best_rate': False, 'cost': cost}})
        # False is a default value

        # New enchant
        if enchant_name not in enchants:
            print(f"{enchant_name.title()} {level} is a new enchant!\n")
            new_enchant = True
            enchants.update({enchant_name: {
                'best_level': {'villager_name': villager_name, 'level': level, 'cost': cost},
                'best_rate': {'villager_name': villager_name, 'level': level, 'cost': cost}
            }})
            villager[full_enchant_name]['is_best_level'] = True
            villager[full_enchant_name]['is_best_rate'] = True
            continue

        if check_best_level(enchant_name, level, cost):
            villager[full_enchant_name]['is_best_level'] = True
            prev_villager = replace_best_level(villager_name, enchant_name, level, cost)
            if prev_villager not in replaced_villagers:
                replaced_villagers.append(prev_villager)
        if check_best_rate(enchant_name, level, cost):
            villager[full_enchant_name]['is_best_rate'] = True
            prev_villager = replace_best_rate(villager_name, enchant_name, level, cost)
            if prev_villager not in replaced_villagers:
                replaced_villagers.append(prev_villager)
        print()
    villagers.update({villager_name: villager})

    unused_villager = False
    for replaced_villager in replaced_villagers:
        if not check_villager(replaced_villager):
            unused_villager = True
            print(f'{replaced_villager} no longer contributes any bests')
    if unused_villager:
        print()

    if new_enchant:
        DB['enchants'] = sorted_dict(enchants)

    update()


def remove_cmd(args):
    villager_name = ' '.join(args)
    villagers = DB['villagers']
    if villager_name not in villagers:
        refresh_display('Villager not found')
        return
    other_villager_names = [x for x in villagers if x != villager_name]
    enchants = DB['enchants']
    if not check_villager(villager_name):  # If villager has no bests, it can be safely deleted without other updates
        villagers.pop(villager_name)
        refresh_display(f'Successfully deleted {villager_name}')
        update()
        return
    # Systematically find the replacement for each best the villager has
    refresh_display()
    for full_enchant_name, data in villagers[villager_name].items():
        enchant_name = get_enchant_name(full_enchant_name.split())
        if data['is_best_level']:
            if not (level_res := get_enchant_best_level(other_villager_names, enchant_name)):
                enchants.pop(enchant_name)  # No villager with this enchant is left
                print(f"Removed [{enchant_name.title()}] as no other villager found with it\n")
                continue
            enchants[enchant_name]['best_level'] = level_res
            new_villager_name = level_res['villager_name']
            new_full_enchant_name = f"{enchant_name} {level_res['level']}"
            villagers[new_villager_name][new_full_enchant_name]['is_best_level'] = True
            print(f"Replaced best level of [{full_enchant_name.title()}] with [{enchant_name.title()} "
                  f"{level_res['level']}] @ {level_res['cost']} ems --> {level_res['villager_name']}\n")
        if data['is_best_rate']:
            rate_res = get_enchant_best_rate(other_villager_names, enchant_name)
            new_villager_name = rate_res['villager_name']
            new_full_enchant_name = f"{enchant_name} {rate_res['level']}"
            villagers[new_villager_name][new_full_enchant_name]['is_best_rate'] = True
            enchants[enchant_name]['best_rate'] = rate_res
            print(f"Replaced best rate of [{enchant_name.title()}] with [{enchant_name.title()} "
                  f"{rate_res['level']}] @ {rate_res['cost']} ems --> {rate_res['villager_name']}\n")
    villagers.pop(villager_name)
    print(f'Successfully deleted {villager_name}\n')
    update()
