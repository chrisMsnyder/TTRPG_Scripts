import pandas as pd
from classes import *
import random
import argparse

MAX_ATTEMPTS = 10
CARGO_CHANCE = 70

systems = {
    'armor': None,
    'armor ablative': None,
    'armor bulkheads': None,
    'armor hulls': None,
    'computers': None,
    'crew quarters': None,
    'defensive countermeasures': None,
    'drift engines': None,
    'interdiction modules': None,
    'other systems': None,
    'security': None,
    'sensors': None,
    'shields': None
}

size_map = {
    'T': 1,
    'S': 2,
    'M': 3,
    'L': 4,
    'H': 5,
    'G': 6,
    'C': 7,
    'D': 8
}



def main(args):
    components_xls = pd.ExcelFile("data/ship_components.xlsx")
    power_cores = pd.read_excel(components_xls, 'power cores')
    thrusters = pd.read_excel(components_xls, 'thrusters')
    frames_xls = pd.ExcelFile("data/frames.xlsx")
    frames = pd.read_excel(frames_xls, 'frames')
    tiers = pd.read_excel(frames_xls, 'tiers')
    tiers['BP'] = tiers['BP'].apply(lambda x: int(x * 1.05) )
    tier = args.max_tier
    print('\n')
    bp_max = tiers.loc[tiers['Tier'] == tier, 'BP'].values[0] - 1

    components_dfs = {}
    for x in components_xls.sheet_names:
        components_dfs[x] = pd.read_excel(components_xls, x)
    if args.exclude:
        excluded_sizes = args.exclude.upper().split(',')
        for size in excluded_sizes:
            frames = frames[frames['Size'] != size]
    row = frames[frames['Cost (in BP)'] <= bp_max / 5].sample().iloc[0]
    row  = row.where(pd.notnull(row), None).to_dict()


    frame = Frame(row)
    ship = Ship(frame, systems, tier, bp_max)
    add_power_core(ship, power_cores)
    add_thrusters(ship, thrusters)
    attempts = 0
    retry = False
    while attempts < MAX_ATTEMPTS:
        if retry == True:
            result = add_power_core(ship, power_cores)
            retry = False
        type_choice = random.choice(['System', 'Weapon', 'Bay', 'Thrusters'])
        if type_choice == 'System':
            result = add_system(ship, components_xls)
        elif type_choice == 'Weapon':
            result = add_weapon(ship, components_xls)
        elif type_choice == 'Bay':
            result = add_expansion_bay(ship, components_xls)
        elif type_choice == 'Thrusters':
            result = add_thrusters(ship, thrusters)

        if result == False:
            retry = True
            attempts += 1
        #print(ship)

    reset_tier(ship, tiers)
    print(ship)



def components_in_budget(ship, df, is_power_core=False):
    if 'PCU' in df.columns.values and not is_power_core:
        df = df[df['PCU'] <= ship.available_pcu()]
    if 'Cost (in BP)' in df.columns.values:
        df = df[df['Cost (in BP)'] <= ship.available_bp()]
    return df



def clean_pcu_bp_columns(ship, df):
    if 'PCU' in df.columns.values:
        df['PCU'] = df['PCU'].astype(str)
        df['PCU'] = df['PCU'].apply(lambda x: str(x) if x != '—' else str(0))
        df['PCU'] = df['PCU'].str.replace('size category', str(size_map[ship.size]))
        df['PCU'] = df['PCU'].apply(lambda x: eval(x))
    if 'Cost (in BP)' in df.columns.values:
        df['Cost (in BP)'] = df['Cost (in BP)'].astype(str)
        df['Cost (in BP)'] = df['Cost (in BP)'].str.replace('size category', str(size_map[ship.size]))
        df['Cost (in BP)'] = df['Cost (in BP)'].apply(lambda x: eval(x))
    return df



def add_power_core(ship, power_cores):
    valid_cores = power_cores[power_cores['Size'].str.contains(ship.size)]
    if ship.power_core != None:
       valid_cores = components_in_budget(ship, valid_cores, is_power_core=True)
       if valid_cores.empty:
           return False
    chosen = valid_cores.sample().iloc[0]
    pcu_spent = 0
    if ship.power_core:
        pcu_spent = ship.power_core.pcu_spent
    power_core = PowerCore(chosen['Name'].strip(), chosen['PCU'], chosen['Cost (in BP)'], pcu_spent)
    if ship.power_core == None or power_core.pcu >= ship.power_core.pcu:
        if ship.power_core:
            ship.adjust_bp(-ship.power_core.cost)
        ship.power_core = power_core
        ship.adjust_bp(power_core.cost)
        return True
    return False



def add_thrusters(ship, thrusters):
    valid_thrusters = thrusters[thrusters['Size'].str.contains(ship.size)]
    valid_thrusters = components_in_budget(ship, valid_thrusters)
    if valid_thrusters.empty:
        return False
    chosen = valid_thrusters.sample().iloc[0]
    thruster = Thruster(chosen['Name'].strip(), chosen['Speed (in Hexes)'], chosen['Piloting Modifier'], chosen['PCU'], chosen['Cost (in BP)'])
    if ship.thrusters == None or thruster.speed >= ship.thrusters.speed:
        if ship.thrusters:
            ship.adjust_bp(-ship.thrusters.cost)
            ship.power_core.adjust_pcu_spent(-ship.thrusters.pcu)
        ship.thrusters = thruster
        ship.adjust_bp(thruster.cost)
        ship.power_core.adjust_pcu_spent(thruster.pcu)
        return True
    return False



def add_system(ship, components_xls):
    open_systems = [k for k,v in ship.systems.items() if v == None]
    if len(open_systems) == 0:
        return False
    random_system = random.choice(open_systems)
    system = pd.read_excel(components_xls, random_system)
    system = clean_pcu_bp_columns(ship, system)
    purchasable_components = components_in_budget(ship, system)
    if purchasable_components.empty:
        return False
    component = purchasable_components.sample().iloc[0]
    if 'PCU' in component.index.to_list():
        comp_pcu = component['PCU']
    else:
        comp_pcu = 0
    if 'Cost (in BP)' in component.index.to_list():
        comp_bp = component['Cost (in BP)']
    else:
        comp_bp = 0
    ship.systems[random_system] = System(component['Name'].strip(), random_system, comp_pcu, comp_bp)
    ship.adjust_bp(comp_bp)
    ship.power_core.adjust_pcu_spent(comp_pcu)
    return True



def add_weapon(ship, components_xls):
    open_arcs = [k for k,v in ship.weapons.items() if v != []]
    if len(open_arcs) == 0:
        return False
    chosen_arc = random.choice(open_arcs)
    open_slots = [x for x in ship.weapons[chosen_arc] if x.name == 'empty']
    if len(open_slots) == 0:
        return False
    chosen_slot = random.choice(open_slots)
    slot_size = chosen_slot.type
    if slot_size == 'L':
        weapons = pd.read_excel(components_xls, 'weapons-light')
    elif slot_size == 'H':
        weapons = pd.read_excel(components_xls, 'weapons-heavy')
    elif slot_size == 'C':
        weapons = pd.read_excel(components_xls, 'weapons-capital')
    weapons = clean_pcu_bp_columns(ship, weapons)
    purchasable_weapons = components_in_budget(ship, weapons)
    if purchasable_weapons.empty:
        return False 
    weapon = purchasable_weapons.sample().iloc[0]
    for i,slot in enumerate(ship.weapons[chosen_arc]):
        if slot.name == 'empty' and slot.type == slot_size:
            ship.weapons[chosen_arc][i] = Weapon(weapon['Name'].strip(), slot_size, weapon['PCU'], weapon['Cost (in BP)'])
            ship.adjust_bp(weapon['Cost (in BP)'])
            ship.power_core.adjust_pcu_spent(weapon['PCU'])
            return True
    return False



def add_expansion_bay(ship, components_xls):
    for i,bay in enumerate(ship.expansion_bays):
        if bay.name == 'Cargo Hold':
            #Buy a Cargo Hold anyway
            if random.randint(1, 100) <= CARGO_CHANCE:
                return True
            exp_bays = pd.read_excel(components_xls, 'expansion bays')
            exp_bays = clean_pcu_bp_columns(ship, exp_bays)
            purchasable_bays = components_in_budget(ship, exp_bays)
            if purchasable_bays.empty:
                return False
            bay = purchasable_bays.sample().iloc[0]
            ship.expansion_bays[i] = ExpansionBay(bay['Name'].strip(), bay['PCU'], bay['Cost (in BP)'])
            ship.adjust_bp(bay['Cost (in BP)'])
            ship.power_core.adjust_pcu_spent(bay['PCU'])
            return True
    return False



def reset_tier(ship, tiers):
    bp = ship.bp

    actual_tier = tiers[tiers['BP'] >= bp].iloc[0]
    ship.tier = int(actual_tier['Tier'])





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_tier', type=int)
    parser.add_argument('--exclude', type=str, default=None)
    args = parser.parse_args()
    main(args)



