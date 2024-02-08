

class Frame:
    def __init__(self, row):
        self.name = row['Name']
        self.size = row['Size']
        self.maneuv = row['Maneuverability']
        self.hp = row['HP']
        self.dt = row['DT']
        self.ct = row['CT']
        self.forward_arc = row['Forward Arc']
        self.port_arc = row['Port Arc']
        self.starboard_arc = row['Starboard Arc']
        self.aft_arc = row['Aft Arc']
        self.turret_arc = row['Turret Arc']
        self.expansion_bays = row['Expansion Bays']
        self.min_crew = row['Min Crew']
        self.max_crew = row['Max Crew']
        self.cost = row['Cost (in BP)']
        self.special = row['Special']




class Ship:
    def __init__(self, frame, systems, tier, max_bp):
        self.frame = frame
        self.tier = tier
        self.max_bp = max_bp
        self.power_core = None
        self.thrusters = None
        self.name = frame.name
        self.size = frame.size
        self.maneuv = frame.maneuv
        self.hp = frame.hp
        self.dt = frame.dt
        self.ct = frame.ct
        self.weapons = {
            'Forward Arc': [],
            'Port Arc': [],
            'Starboard Arc': [],
            'Aft Arc': [],
            'Turret Arc': []
        }
        if frame.forward_arc:
            for x in frame.forward_arc.split(','):
                self.weapons['Forward Arc'].append(Weapon('empty', x))
        self.port_arc = []
        if frame.port_arc:
            for x in frame.port_arc.split(','):
                self.weapons['Port Arc'].append(Weapon('empty', x))
        self.starboard_arc = []
        if frame.starboard_arc:
            for x in frame.starboard_arc.split(','):
                self.weapons['Starboard Arc'].append(Weapon('empty', x))
        self.aft_arc = []
        if frame.aft_arc:
            for x in frame.aft_arc.split(','):
                self.weapons['Aft Arc'].append(Weapon('empty', x))
        self.turret_arc = []
        if frame.turret_arc:
            for x in frame.turret_arc.split(','):
                self.weapons['Turret Arc'].append(Weapon('empty', x))
        self.expansion_bays = [ExpansionBay('Cargo Hold', 0, 0) for x in range(frame.expansion_bays)]
        self.min_crew = frame.min_crew
        self.max_crew = frame.max_crew
        self.bp = frame.cost
        self.special = frame.special
        self.systems = systems


    def __str__(self) -> str:
        print_str = ""
        print_str += f"Frame: {self.name}\n"
        print_str += f"Size: {self.size}\n"
        print_str += f"BP Cost: {self.bp}({int(self.bp * 0.8)}) -- Tier: {self.tier}\n"
        print_str += f"{self.power_core}\n"
        print_str += f"{self.thrusters} - Maneuver: {self.maneuv}\n"
        print_str += f"HP: {self.hp}\n"
        print_str += "Weapon Mounts:\n"
        for arc in self.weapons.keys():
            if self.weapons[arc]:
                arc_print = '\n\t\t'.join([str(weap) for weap in self.weapons[arc]])
                print_str += f"\t{arc}:\n\t\t{arc_print}\n"
        exp_print = '\n\t'.join([str(exp) for exp in self.expansion_bays])
        print_str += f"Expansion Bays--{len(self.expansion_bays)}:\n\t(Bonus) Cargo Hold\n\t{exp_print}\n"
        system_print = '\n\t'.join([str(sys) for sys in self.systems.values() if sys != None])
        print_str += f"Systems:\n\t{system_print}\n"

        return print_str

    def adjust_bp(self, bp_amount):
        self.bp += bp_amount

    def available_pcu(self):
        return self.power_core.pcu - self.power_core.pcu_spent
    
    def available_bp(self):
        return self.max_bp - self.bp




class Weapon:
    def __init__(self, name, type, pcu=0, bp=0):
        self.name = name
        self.type = type
        self.pcu = pcu
        self.bp = bp

    def __str__(self) -> str:
        print_str = f"{self.name} ({self.type})"
        return print_str



class PowerCore:
    def __init__(self, name, pcu, cost, pcu_spent=0):
        self.name = name
        self.pcu = pcu
        self.cost = cost
        self.pcu_spent = pcu_spent

    def __str__(self) -> str:
        return f"Power Core: {self.name} -- PCU: {self.pcu_spent}\{self.pcu}"

    def adjust_pcu_spent(self, pcu_amount):
        self.pcu_spent += pcu_amount



class Thruster:
    def __init__(self, name, speed, mod, pcu, cost):
        self.name = name
        self.speed = speed
        self.mod = mod
        self.pcu = pcu
        self.cost = cost

    def __str__(self) -> str:
        return f"Thrusters: {self.name} - Speed: {self.speed}"



class System:
    def __init__(self, name, type, pcu, cost):
        self.name = name
        self.type = type
        self.pcu = pcu
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"



class ExpansionBay:
    def __init__(self, name, pcu, cost):
        self.name = name
        self.pcu = pcu
        self.cost = cost

    def __str__(self) -> str:
        return f"{self.name}"