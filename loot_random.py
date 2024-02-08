import pandas as pd
import random
import argparse


def constrain_levels(items, min_level, max_level):
    for key in items.keys():
        items[key] = items[key][items[key]['Level'] <= max_level]
        items[key] = items[key][items[key]['Level'] >= min_level]

def constrain_costs(items, max_val):
    for key in items.keys():
        items[key] = items[key][items[key]['Price'] <= max_val]

def pretty_print(loot_dict, maxlen):
    key_list = list(loot_dict.keys())
    key_list.sort()
    print()
    print(f"     {'NAME':<{maxlen+2}}{'ITEM WORTH'}")
    print()
    for key in key_list:
        print(f"{key}:")
        for item in loot_dict[key]:
            print(f"     {item['Name']:<{maxlen+2}}{item['Price']}")
        print()


def main(args):
    items_xls = pd.ExcelFile("data/sf_items.xlsx")
    wpe = pd.read_excel(items_xls, 'Wealth Per Encounter')
    wpe['Wealth Gain'].astype(int, copy=False)
    hybrid_items = pd.read_excel(items_xls, 'Hybrid')
    hybrid_items['Price'].astype(int, copy=False)
    hybrid_items['Name'] = hybrid_items['Name'].str.strip()
    magic_items = pd.read_excel(items_xls, 'Magic')
    magic_items['Price'].astype(int, copy=False)
    magic_items['Name'] = magic_items['Name'].str.strip()
    tech_items = pd.read_excel(items_xls, 'Technological')
    tech_items['Price'].astype(int, copy=False)
    tech_items['Name'] = tech_items['Name'].str.strip()
    armor_upgrades_items = pd.read_excel(items_xls, 'Armor Upgrades')
    armor_upgrades_items['Price'].astype(int, copy=False)
    armor_upgrades_items['Name'] = armor_upgrades_items['Name'].str.strip()
    fusion_costs_items = pd.read_excel(items_xls, 'Fusion Costs')
    fusion_costs_items['Price'].astype(int, copy=False)
    fusions_items = pd.read_excel(items_xls, 'Fusions')
    fusions_items['Name'] = fusions_items['Name'].str.strip()
    grenades_items = pd.read_excel(items_xls, 'Grenades')
    grenades_items['Price'].astype(int, copy=False)
    grenades_items['Name'] = grenades_items['Name'].str.strip()
    healing_items = pd.read_excel(items_xls, 'Healing Serums')
    healing_items['Price'].astype(int, copy=False)
    healing_items['Name'] = healing_items['Name'].str.strip()
    weapon_items = pd.read_excel(items_xls, 'Weapons')
    weapon_items['Price'].astype(int, copy=False)
    weapon_items['Name'] = weapon_items['Name'].str.strip()
    armor_items = pd.read_excel(items_xls, 'Armor')
    armor_items['Price'].astype(int, copy=False)
    armor_items['Name'] = armor_items['Name'].str.strip()
    

    items = {
        'Hybrid Items': hybrid_items,
        'Magic Items': magic_items,
        'Technological Items': tech_items,
        'Armor Upgrades': armor_upgrades_items,
        'Fusion Seals': fusion_costs_items,
        'Grenades': grenades_items,
        'Healing Serums': healing_items,
        'Weapons': weapon_items,
        'Armor': armor_items
    }

    loot_value = wpe.query("CR == @args.cr")['Wealth Gain'].values[0]
    percent_val = int(loot_value * 0.25)
    low_val = loot_value - percent_val
    high_val = loot_value + percent_val
    total_value = random.randint(low_val, high_val)
    total_value = int(total_value / 4 * args.player_count)
    max_val = int(total_value / 2)

    min_level = args.cr - 5
    max_level = args.cr + 3

    constrain_levels(items, min_level, max_level)

    loot_dict = {}
    maxlen = 0
    for i in range(10):
        if total_value <= 10:
            break
        constrain_costs(items, max_val)
        item_type = random.choices(list(items.keys()))[0]
        if items[item_type].shape[0] == 0:
            continue
        picked_item = items[item_type].sample().squeeze()
        if item_type == 'Fusion Seals':
            fusion_type = fusions_items['Name'].sample().values[0]
            picked_item['Name'] = f"{picked_item['Name']}, {fusion_type}"
        if len(picked_item['Name']) > maxlen:
            maxlen = len(picked_item['Name'])
        total_value -= picked_item['Price']
        if item_type == 'Weapons' or item_type == 'Armor':
            item_type = f"{item_type} ({picked_item['Type']})"
        if item_type not in loot_dict:
            loot_dict[item_type] = [picked_item]
        else:
            loot_dict[item_type].append(picked_item)
    pretty_print(loot_dict, maxlen)    

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cr', type=int)
    parser.add_argument('--player_count', type=int, default=7)
    args = parser.parse_args()
    main(args)