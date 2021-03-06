"""
Idle Clicker Remastered.

By Jack, Dane, and Autum
"""


# IMPORTS #


import tkinter
import tkinter.ttk as ttk

import datetime
from random import randint
import pytz

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

time = datetime.datetime
timezone = pytz.timezone('Egypt')


def nighttime():
    """Detect nightime."""
    if time.now(timezone).hour < 6 or time.now(timezone).hour > 20:
        return True
    return False

# CLASSES #


# Create classes to store information. Object-orientated programming.
# Using these, we can ditch global variables and easily create fuctions that
# acton itself as well as create multiple of them without much issue.
class Graph():
    def __init__(self, master):
        self.top = tkinter.Toplevel(master)
        self.top.title = "Damage Graph"
        self.graph = Figure(figsize=(5, 4), dpi=100, facecolor='#1e1e1e')

        self.values: list = []

        for x in range(30):
            self.values.append(0)
        self.dps = 0

        self.graph_config = self.graph.add_subplot(111)
        self.graph_config.tick_params(axis='y', colors='#f1f1f1')
        self.graph_config.tick_params(axis='x', colors='#f1f1f1')
        self.graph_config.plot(self.values)

        self.canvas = FigureCanvasTkAgg(self.graph, self.top)
        self.canvas.get_tk_widget().configure(bg="black")
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, expand=0)

    def update(self):
        self.values.append(self.dps)
        del self.values[0]
        self.dps = 0

        self.graph_config.clear()
        self.graph_config.plot(self.values)
        self.canvas.draw()

class PlayerValues(dict):
    """Define values and modules for the PLAYER object."""

    def __init__(self):
        """Initialize PLAYER with a random name and starting values."""
        self.random_name()
        # self['name'] = "Belle Delphine"

        self["gold"] = 0

        self["strength"] = 1
        self["crit_chance"] = 5

        self["peasants"] = 0
        self["knights"] = 0
        self["adventurers"] = 0
        self["heroes"] = 0

        self["skill_one"] = False
        self["skill_two"] = False
        self["skill_three"] = False

        self["skill_one_level"] = 0
        self["skill_two_level"] = 0
        self["skill_three_level"] = 0

        self["skill_one_cooldown"] = 0
        self["skill_two_cooldown"] = 0
        self["skill_three_cooldown"] = 0

        self["stage"] = 1

    def random_name(self):
        """Give PLAYER a random name."""
        self["name"] = (f"{first_name[randint(0, len(first_name) - 1)]}"
                        + f" {last_name[randint(0, len(last_name) - 1)]}")

    def critical_hit(self):
        """Return value for critical hits."""
        _crit = randint(1, 100)
        if _crit <= self["crit_chance"]:
            return True
        return False

    def attack(self):
        """Return damage values."""
        if not self["skill_one"]:
            if not self.critical_hit():
                return self["strength"]
            print_console(crit_message(PLAYER["name"]))
            return self["strength"] * 2

        if not self.critical_hit():
            return self["strength"] * 2 * self["skill_one_level"]
        return self["strength"] * 3 * self["skill_one_level"]

    def allies_attack(self):
        """Return allies damage values."""
        _damage: int = 0
        _damage += self["peasants"] * 2
        _damage += self["knights"] * 10
        _damage += self["adventurers"] * 25
        _damage += self["heroes"] * 100
        if self['name'] == "Jotaro Kujo":
            _damage += self["strength"]
        return _damage

    def gold_increase(self, health):
        """Increase player's gold depending on enemy health."""
        _gold_gain = round((health / 5) * 2)
        self['gold'] += _gold_gain

        return str(_gold_gain)
    def upgrade_stat(self, value, quantity, cost):
        if self['gold'] < cost:
            print_console("Insufficient Gold.\n")
            return False
        self['gold'] -= cost
        self[value] = self[value] + quantity
        return True


class EnemyValues(dict):
    """Define values and modules for the ENEMY object."""

    def __init__(self):
        """Initialize ENEMY with a random name."""
        self.random_name()
        self.random_health()


    def random_name(self):
        """Give ENEMY a random name."""
        self["name"] = (f"{first_name[randint(0, len(first_name) - 1)]}"
                        + f" {last_name[randint(0, len(last_name) - 1)]}")

        # self['name'] = "Dio Brando"

        if self['name'] == 'Dio Brando' and nighttime():
            self['name'] = 'DIO'

    def random_health(self):
        """Give ENEMY a random health value."""
        rand_health = randint(40, 50)
        if PLAYER['stage'] % 50 == 0:
            rand_health *= 4
            print_console("A boss has appeared!\n")
        elif PLAYER['stage'] % 10 == 0:
            rand_health *= 1.5
            print_console("A miniboss has appeared!\n")

        self["health_max"] = round(rand_health * PLAYER["stage"] / 10)
        self["health"] = self["health_max"]


class ShopValues(dict):
    """Definte values and modules for the SHOP object."""

    def __init__(self):
        self['strength_cost'] = 10
        self['dexterity_cost'] = 10

        self['peasants_cost'] = 10
        self['knights_cost'] = 10
        self['adventurers_cost'] = 10
        self['heroes_cost'] = 10

        self.update_skill()

    def update_cost(self, cost, multiplier):
        self[cost] = round(self[cost] * multiplier)

    def update_skill(self):
        self['skill_one_cost'] = 100 + PLAYER['skill_one_level'] * 100
        self['skill_two_cost'] = 250 + PLAYER['skill_two_level'] * 250
        self['skill_three_cost'] = 500 + PLAYER['skill_three_level'] * 500

# VARIABLES #


first_name: list = ["Jack", "Dane", "Autum", "Jotaro", "Belle", "Dio"]
last_name: list = ["Kiv", "Claus", "San", "Kujo", "Delphine", "Brando"]

PLAYER = PlayerValues()
ENEMY = EnemyValues()
SHOP = ShopValues()



SECONDS: float = 0


# FUNCTIONS #


# Add functions for game logic
def print_console(value):
    """Print value to the console."""
    console_window.insert("end", f"{value}\n")
    console_window.see("end")


def crit_message(name):
    """Switch critical hit message depending on name."""
    switcher = {
        'Jotaro Kujo': "Star Platinum, Za Warudo! Critical hit!\n"
    }
    return switcher.get(name, "Critical hit!\n")



def enemy_update():
    """Update ENEMY screen values."""
    enemy_name['text'] = ENEMY['name']

    enemy_health_bar['max'] = ENEMY['health_max']
    enemy_health_bar['value'] = ENEMY['health']
    enemy_health_number['text'] = (f"{ENEMY['health']}"
                                   + f"/{ENEMY['health_max']}")


def player_update():
    """Update PLAYER screen values."""
    player_name['text'] = PLAYER['name']

    player_stage_value['text'] = PLAYER['stage']

    player_gold_value['text'] = PLAYER['gold']

    player_strength_value['text'] = PLAYER['strength']
    player_dexterity_value['text'] = PLAYER['crit_chance']

    player_peasants_value['text'] = PLAYER['peasants']
    player_knights_value['text'] = PLAYER['knights']
    player_adventurers_value['text'] = PLAYER['adventurers']
    player_heroes_value['text'] = PLAYER['heroes']

    player_skill_one_level_value['text'] = PLAYER['skill_one_level']
    player_skill_two_level_value['text'] = PLAYER['skill_two_level']
    player_skill_three_level_value['text'] = PLAYER['skill_three_level']

    player_skill_one_bar['value'] = PLAYER['skill_one_cooldown']
    player_skill_two_bar['value'] = PLAYER['skill_two_cooldown']
    player_skill_three_bar['value'] = PLAYER['skill_three_cooldown']


def shop_update():
    """Update SHOP screen values."""
    shop_stats_strength_value['text'] = SHOP['strength_cost']
    shop_stats_dexterity_value['text'] = SHOP['dexterity_cost']

    shop_allies_peasants_value['text'] = SHOP['peasants_cost']
    shop_allies_knights_value['text'] = SHOP['knights_cost']
    shop_allies_adventurers_value['text'] = SHOP['adventurers_cost']
    shop_allies_heroes_value['text'] = SHOP['heroes_cost']

    shop_skills_one['max'] = SHOP['skill_one_cost']
    shop_skills_two['max'] = SHOP['skill_two_cost']
    shop_skills_three['max'] = SHOP['skill_three_cost']
    shop_skills_one['value'] = PLAYER['stage']
    shop_skills_two['value'] = PLAYER['stage']
    shop_skills_three['value'] = PLAYER['stage']
    shop_skills_one_value['text'] = SHOP['skill_one_cost']
    shop_skills_two_value['text'] = SHOP['skill_two_cost']
    shop_skills_three_value['text'] = SHOP['skill_three_cost']


def kill_message(name):
    """Return kill message."""
    if name == 'Jotaro Kujo':
        _kill_word: list = ["ORA ORA ORA!", "ORA!", "ORA ORA!"]
        _rand_num: int = randint(0, len(_kill_word) - 1)

        return _kill_word[_rand_num]

    else:
        _kill_word: list = ["slain", "killed", "crushed", "destroyed"]
        _rand_num: int = randint(0, len(_kill_word) - 1)

        return _kill_word[_rand_num]


def death():
    """Activate when enemy dies to reset values."""
    if ENEMY['health'] > 0:
        pass

    elif ENEMY['name'] == 'DIO':
        ENEMY['health'] = ENEMY['health_max']
        enemy_update()
        _quote: dict = {0: "Oh? You're approaching, me?",
                        1: "MUDA MUDA!",
                        2: "ZA WARUDO!"}
        print_console(_quote[randint(0, len(_quote)-1)])
    else:
        # TODO: add function instead
        print_console(f"{ENEMY['name']} has been {kill_message(PLAYER['name'])}!\n"
                      + PLAYER.gold_increase(ENEMY['health_max'])
                      + " Gold Received.\n")

        PLAYER['stage'] += 1
        ENEMY.random_name()
        ENEMY.random_health()
        enemy_update()
        upgrade_skill()
    shop_update()
    player_update()


def upgrade_skill():
    if shop_skills_one['value'] == shop_skills_one['max']:
        PLAYER['skill_one_level'] += 1
        if PLAYER['skill_one_level'] == 1:
            PLAYER['skill_one_cooldown'] = 60
    if shop_skills_two['value'] == shop_skills_two['max']:
        PLAYER['skill_two_level'] += 1
        if PLAYER['skill_two_level'] == 1:
            PLAYER['skill_one_cooldown'] = 60
    if shop_skills_three['value'] == shop_skills_three['max']:
        PLAYER['skill_three_level'] += 1
        if PLAYER['skill_three_level'] == 1:
            PLAYER['skill_one_cooldown'] = 60
    SHOP.update_skill()

def upgrade_strength():
    if PLAYER.upgrade_stat('strength', 5, SHOP['strength_cost']):
        SHOP.update_cost('strength_cost', 1.8)
        print_console("Strength upgraded")
    player_update()
    shop_update()

def upgrade_dexerity():
    if PLAYER.upgrade_stat('crit_chance', 1, SHOP['dexterity_cost']):
        SHOP.update_cost('dexterity_cost', 1.5)
        print_console("Dexterity upgraded")
    player_update()
    shop_update()

def upgrade_peasants():
    if PLAYER.upgrade_stat('peasants', 1, SHOP['peasants_cost']):
        SHOP.update_cost('peasants_cost', 1.2)
        print_console("Peasant hired.\n")
    player_update()
    shop_update()

def upgrade_knights():
    if PLAYER.upgrade_stat('knights', 1, SHOP['knights_cost']):
        SHOP.update_cost('knights_cost', 1.5)
        print_console("Knight hired.\n")
    player_update()
    shop_update()

def upgrade_adventurers():
    if PLAYER.upgrade_stat('adventurers', 1, SHOP['adventurers_cost']):
        SHOP.update_cost('adventurers_cost', 1.6)
        print_console("Adventurer hired.\n")
    player_update()
    shop_update()

def upgrade_heroes():
    if PLAYER.upgrade_stat('heroes', 1, SHOP['heroes_cost']):
        SHOP.update_cost('heroes_cost', 1.8)
        print_console("Hero hired.\n")
    player_update()
    shop_update()

def attack(event):
    """Activate when PLAYER clicks to damage ENEMY."""
    _damage = PLAYER.attack()
    ENEMY['health'] -= _damage
    if PLAYER['skill_two']:
        PLAYER['gold'] += round(ENEMY['health_max'] / 10
                                * PLAYER["skill_three_level"])
    DPS.dps += _damage

    death()
    enemy_update()


def skill_switch(skill):
    PLAYER[skill] = not PLAYER[skill]


def skill_locked(skill):
    return bool(PLAYER[skill + '_level'] == 0)


def skill_cooldown():
    _skills = ['skill_one', 'skill_two', 'skill_three']
    for _skill in _skills:
        _skill_cooldown = _skill + "_cooldown"

        if skill_locked(_skill):
            pass
        elif PLAYER[_skill] and PLAYER[_skill_cooldown] > 0:
            PLAYER[_skill_cooldown] -= 2
        elif PLAYER[_skill] and PLAYER[_skill_cooldown] == 0:
            skill_switch(_skill)
        elif PLAYER[_skill_cooldown] < 60:
            PLAYER[_skill_cooldown] += 1


def skill_unavailable(skill):
    return bool(PLAYER[skill] or PLAYER[skill + "_cooldown"] != 60)


def skill_use(skill):
    if skill_locked(skill):
        print_console("Skill is locked.\n")
    elif skill_unavailable(skill):
        print_console("Skill is unavailable.\n")
    else:
        skill_switch(skill)


def skill_one_use():
    skill_use("skill_one")

def skill_two_use():
    skill_use("skill_two")

def skill_three_use():
    skill_use("skill_three")


def game_tick():
    """Store all loops."""
    global SECONDS
    SECONDS += 0.5
    if SECONDS > 3600:
        SECONDS = 0

    # Every minute
    if PLAYER['name'] == 'Belle Delphine' and SECONDS % 60 == 0:
        _gold_gain = round(PLAYER['gold'] * .5)
        PLAYER['gold'] += _gold_gain
        print_console(f"Your OnlyFans paid {_gold_gain} Gold!")

    # Every second
    if SECONDS % 1 == 0:
        ENEMY['health'] -= PLAYER.allies_attack()
        DPS.dps += PLAYER.allies_attack()
        skill_cooldown()
        DPS.update()
    elif PLAYER['skill_three']:
        ENEMY['health'] -= PLAYER.allies_attack() * PLAYER["skill_two_level"]
        DPS.dps += PLAYER.allies_attack()

    death()
    enemy_update()
    root.after(500, game_tick)


# ROOT CREATION #


root = tkinter.Tk()
root.title("Endless Expansion V1.0")

root.grid_columnconfigure([0, 2],
                          weight=225,
                          minsize=225)
root.grid_columnconfigure(1,
                          weight=350,
                          minsize=350)
root.grid_rowconfigure(0,
                       weight=600,
                       minsize=600)

DPS = Graph(root)


# CREATE PANELS #


left_panel = tkinter.Frame(root,
                           bg="#1e1e1e")
left_panel.grid(row=0, column=0,
                sticky="nsew")

middle_panel = tkinter.Frame(root,
                             bg="#1e1e1e")
middle_panel.grid(row=0, column=1,
                  sticky="nsew")

right_panel = tkinter.Frame(root,
                            bg="#1e1e1e")
right_panel.grid(row=0, column=2,
                 sticky="nsew")


# LEFT PANEL ASSETS #


left_panel.grid_columnconfigure(0,
                                weight=225,
                                minsize=225)
left_panel.grid_rowconfigure(0,
                             weight=75,
                             minsize=75)
left_panel.grid_rowconfigure(1,
                             weight=425,
                             minsize=425)
left_panel.grid_rowconfigure(2,
                             weight=100,
                             minsize=100)

player_name = tkinter.Label(left_panel,
                            bg="#1e1e1e",
                            fg="#f1f1f1",
                            text=PLAYER["name"],
                            font=("System", 18))
player_name.grid(row=0, column=0,
                 sticky="nsew")


player_stats = tkinter.Frame(left_panel,
                             bg="#2e2e2e")
player_stats.grid(row=1, column=0,
                  padx=20, pady=10,
                  sticky="nsew")

player_stats.grid_columnconfigure(0,
                                  weight=125,
                                  minsize=125)
player_stats.grid_columnconfigure(1,
                                  weight=100,
                                  minsize=100)

player_stage = tkinter.Label(player_stats,
                             bg="#2e2e2e",
                             fg="#f1f1f1",
                             text="Stage",
                             font=("System", 16))
player_stage.grid(row=0, column=0,
                  padx=10, pady=(20, 10),
                  sticky="w")
player_stage_value = tkinter.Label(player_stats,
                                   bg="#2e2e2e",
                                   fg="#f1f1f1",
                                   text=PLAYER['stage'],
                                   font=("System", 12))
player_stage_value.grid(row=0, column=1,
                        padx=0, pady=(20, 10),
                        sticky="w")

player_gold = tkinter.Label(player_stats,
                            bg="#2e2e2e",
                            fg="#f1f1f1",
                            text="Gold",
                            font=("System", 16))
player_gold.grid(row=1, column=0,
                 padx=10, pady=10,
                 sticky="w")
player_gold_value = tkinter.Label(player_stats,
                                  bg="#2e2e2e",
                                  fg="#f1f1f1",
                                  text=PLAYER['gold'],
                                  font=("System", 12))
player_gold_value.grid(row=1, column=1,
                       padx=0, pady=10,
                       sticky="w")

player_strength = tkinter.Label(player_stats,
                                bg="#2e2e2e",
                                fg="#f1f1f1",
                                text="Strength",
                                font=("System", 16))
player_strength.grid(row=2, column=0,
                     padx=10, pady=(10, 5),
                     sticky="w")
player_strength_value = tkinter.Label(player_stats,
                                      bg="#2e2e2e",
                                      fg="#f1f1f1",
                                      text=PLAYER['strength'],
                                      font=("System", 12))
player_strength_value.grid(row=2, column=1,
                           padx=0, pady=(10, 5),
                           sticky="w")

player_dexterity = tkinter.Label(player_stats,
                                 bg="#2e2e2e",
                                 fg="#f1f1f1",
                                 text="Dexterity",
                                 font=("System", 16))
player_dexterity.grid(row=3, column=0,
                      padx=10, pady=(5, 10),
                      sticky="w")
player_dexterity_value = tkinter.Label(player_stats,
                                       bg="#2e2e2e",
                                       fg="#f1f1f1",
                                       text=PLAYER['crit_chance'],
                                       font=("System", 12))
player_dexterity_value.grid(row=3, column=1,
                            padx=0, pady=(5, 10),
                            sticky="w")


player_peasants = tkinter.Label(player_stats,
                                bg="#2e2e2e",
                                fg="#f1f1f1",
                                text="Peasants",
                                font=("System", 16))
player_peasants.grid(row=4, column=0,
                     padx=10, pady=(10, 5),
                     sticky="w")
player_peasants_value = tkinter.Label(player_stats,
                                      bg="#2e2e2e",
                                      fg="#f1f1f1",
                                      text=PLAYER['peasants'],
                                      font=("System", 12))
player_peasants_value.grid(row=4, column=1,
                           padx=0, pady=(10, 5),
                           sticky="w")


player_knights = tkinter.Label(player_stats,
                               bg="#2e2e2e",
                               fg="#f1f1f1",
                               text="Knights",
                               font=("System", 16))
player_knights.grid(row=5, column=0,
                    padx=10, pady=5,
                    sticky="w")
player_knights_value = tkinter.Label(player_stats,
                                     bg="#2e2e2e",
                                     fg="#f1f1f1",
                                     text=PLAYER['knights'],
                                     font=("System", 12))
player_knights_value.grid(row=5, column=1,
                          padx=0, pady=5,
                          sticky="w")


player_adventurers = tkinter.Label(player_stats,
                                   bg="#2e2e2e",
                                   fg="#f1f1f1",
                                   text="Adventurers",
                                   font=("System", 16))
player_adventurers.grid(row=6, column=0,
                        padx=10, pady=5,
                        sticky="w")
player_adventurers_value = tkinter.Label(player_stats,
                                         bg="#2e2e2e",
                                         fg="#f1f1f1",
                                         text=PLAYER['adventurers'],
                                         font=("System", 12))
player_adventurers_value.grid(row=6, column=1,
                              padx=0, pady=5,
                              sticky="w")


player_heroes = tkinter.Label(player_stats,
                              bg="#2e2e2e",
                              fg="#f1f1f1",
                              text="Heroes",
                              font=("System", 16))
player_heroes.grid(row=7, column=0,
                   padx=10, pady=(5, 10),
                   sticky="w")
player_heroes_value = tkinter.Label(player_stats,
                                    bg="#2e2e2e",
                                    fg="#f1f1f1",
                                    text=PLAYER['heroes'],
                                    font=("System", 12))
player_heroes_value.grid(row=7, column=1,
                         padx=0, pady=(5, 10),
                         sticky="w")


player_skill_one_level = tkinter.Label(player_stats,
                                bg="#2e2e2e",
                                fg="#f1f1f1",
                                text="Critical Level",
                                font=("System", 16))
player_skill_one_level.grid(row=8, column=0,
                     padx=10, pady=(10, 5),
                     sticky="w")
player_skill_one_level_value = tkinter.Label(player_stats,
                                      bg="#2e2e2e",
                                      fg="#f1f1f1",
                                      font=("System", 12))
player_skill_one_level_value.grid(row=8, column=1,
                           padx=0, pady=(10, 5),
                           sticky="w")

player_skill_two_level = tkinter.Label(player_stats,
                                bg="#2e2e2e",
                                fg="#f1f1f1",
                                text="Midas Level",
                                font=("System", 16))
player_skill_two_level.grid(row=9, column=0,
                     padx=10, pady=5,
                     sticky="w")
player_skill_two_level_value = tkinter.Label(player_stats,
                                      bg="#2e2e2e",
                                      fg="#f1f1f1",
                                      font=("System", 12))
player_skill_two_level_value.grid(row=9, column=1,
                           padx=0, pady=5,
                           sticky="w")

player_skill_three_level = tkinter.Label(player_stats,
                                bg="#2e2e2e",
                                fg="#f1f1f1",
                                text="War Cry Level",
                                font=("System", 16))
player_skill_three_level.grid(row=10, column=0,
                     padx=10, pady=5,
                     sticky="w")
player_skill_three_level_value = tkinter.Label(player_stats,
                                      bg="#2e2e2e",
                                      fg="#f1f1f1",
                                      font=("System", 12))
player_skill_three_level_value.grid(row=10, column=1,
                           padx=0, pady=(5, 10),
                           sticky="w")



player_skills = tkinter.Frame(left_panel,
                              bg="#1e1e1e")
player_skills.grid(row=2, column=0,
                   sticky="nsew", padx=15)

player_skills.grid_columnconfigure([0, 1, 2],
                                   weight=25,
                                   minsize=25)
player_skills.grid_rowconfigure(0,
                                weight=0)
player_skills.grid_rowconfigure(1,
                                weight=1)
player_skill_one_bar = ttk.Progressbar(player_skills,
                                       mode="determinate",
                                       max=60,
                                       value=0,
                                       length=40)
player_skill_one_bar.grid(row=0, column=0,
                          padx=5, pady=5, sticky='ew')

player_skill_one = tkinter.Button(player_skills,
                                  width=5, height=2,
                                  bg="#2e1e1e", fg="#f1f1f1",
                                  text="Critical",
                                  font="System",
                                  command=skill_one_use)
player_skill_one.grid(row=1, column=0,
                      padx=5, pady=(5, 20), sticky='nsew')

player_skill_two = tkinter.Button(player_skills,
                                  width=5, height=2,
                                  bg="#2e1e1e", fg="#f1f1f1",
                                  text="Midas",
                                  font="System",
                                  command=skill_two_use)
player_skill_two.grid(row=1, column=1,
                      padx=5, pady=(5, 20), sticky='nsew')

player_skill_three = tkinter.Button(player_skills,
                                    width=5, height=2,
                                    bg="#2e1e1e", fg="#f1f1f1",
                                    text="War Cry",
                                    font="System",
                                    command=skill_three_use)
player_skill_three.grid(row=1, column=2,
                        padx=5, pady=(5, 20),
                        sticky='nsew')

player_skill_two_bar = ttk.Progressbar(player_skills,
                                       mode="determinate",
                                       max=60,
                                       value=0,
                                       length=40)
player_skill_two_bar.grid(row=0, column=1,
                          padx=5, pady=5, sticky='ew')

player_skill_three_bar = ttk.Progressbar(player_skills,
                                         mode="determinate",
                                         max=60,
                                         value=0,
                                         length=40)
player_skill_three_bar.grid(row=0, column=2,
                            padx=5, pady=5, sticky='ew')


# MIDDLE PANEL ASSETS #


middle_panel.grid_columnconfigure(0,
                                  weight=225,
                                  minsize=225)
middle_panel.grid_rowconfigure(0,
                               weight=75,
                               minsize=75)
middle_panel.grid_rowconfigure(1,
                               weight=300,
                               minsize=300)
middle_panel.grid_rowconfigure(2,
                               weight=225,
                               minsize=225)
enemy_health = tkinter.Frame(middle_panel,
                             bg="#1e1e1e")
enemy_health.grid(row=0, column=0)


enemy_health_bar = ttk.Progressbar(enemy_health,
                                   mode="determinate",
                                   length=300)
enemy_health_bar.grid(row=0, column=0)


enemy_health_number = tkinter.Label(enemy_health,
                                    bg="#1e1e1e",
                                    fg="#f1f1f1",
                                    font=("System", 20))
enemy_health_number.grid(row=1, column=0)
enemy_health.lower(belowThis=enemy_health_bar)

enemy = tkinter.Frame(middle_panel,
                      bg="#1e1e1e",
                      width=300)

enemy.grid(row=1, column=0)
enemy.grid_rowconfigure(0,
                        weight=0)
enemy.grid_rowconfigure(1,
                        weight=1)

enemy_name = tkinter.Label(enemy,
                           bg="#1e1e1e",
                           fg="#f1f1f1",
                           text=ENEMY["name"],
                           font=("System", 18))
enemy_name.grid(row=0, column=0)
enemy_body = tkinter.Frame(enemy,
                           bg="#2e1e1e",
                           width=200,
                           height=300)
enemy_body.grid(row=1, column=0)

middle_panel.bind("<Button-1>", attack)
enemy.bind("<Button-1>", attack)
enemy_name.bind("<Button-1>", attack)
enemy_body.bind("<Button-1>", attack)

console = tkinter.Frame(middle_panel,
                        bg="#1e1e1e")
console.grid(row=2, column=0, sticky='nesw', pady=20)
console.grid_columnconfigure(0, weight=1)
console.grid_columnconfigure(1, weight=0)
console.grid_rowconfigure(0, weight=1)

console_window = tkinter.Text(console,
                              bg="#1e1e1e", fg="#f1f1f1",
                              width=1, height=1,
                              font="System")
console_window.grid(row=0, column=0, sticky='nsew')

console_scrollbar = tkinter.Scrollbar(console)
console_scrollbar.grid(row=0, column=1, sticky="nsew")

console_window.config(yscrollcommand=console_scrollbar.set)
console_scrollbar.config(command=console_window.yview)


# RIGHT PANEL ASSETS #


right_panel.grid_columnconfigure(0,
                                 weight=225,
                                 minsize=225)
right_panel.grid_rowconfigure(0,
                              weight=75,
                              minsize=75)
right_panel.grid_rowconfigure(1,
                              weight=116,
                              minsize=116)
right_panel.grid_rowconfigure(2,
                              weight=232,
                              minsize=232)
right_panel.grid_rowconfigure(3,
                              weight=175,
                              minsize=175)


shop_name = tkinter.Label(right_panel,
                          bg="#1e1e1e",
                          fg="#f1f1f1",
                          text="Shop",
                          font=("System", 18))
shop_name.grid(row=0, column=0,
               sticky="nsew")

shop_stats = tkinter.Frame(right_panel,
                           bg="#2e2e2e")
shop_stats.grid(row=1, column=0,
                padx=20, pady=10,
                sticky="nsew")

shop_stats.grid_columnconfigure(0,
                                weight=125,
                                minsize=125)

shop_stats.grid_columnconfigure(1,
                                weight=100,
                                minsize=100)

shop_stats.grid_rowconfigure([0, 1],
                             weight=1)

shop_stats_strength = tkinter.Button(shop_stats,
                                     bg="#2e1e1e", fg="#f1f1f1",
                                     text="Upgrade Strength",
                                     command=upgrade_strength)
shop_stats_strength.grid(row=0, column=0,
                         padx=10, pady=(10, 5),
                         sticky="nsew")

shop_stats_dexterity = tkinter.Button(shop_stats,
                                      bg="#2e1e1e", fg="#f1f1f1",
                                      text="Upgrade Dexterity",
                                      command=upgrade_dexerity)
shop_stats_dexterity.grid(row=1, column=0,
                          padx=10, pady=(5, 10),
                          sticky="nsew")

shop_stats_strength_value = tkinter.Label(shop_stats,
                                          bg="#2e2e2e", fg="#f1f1f1",
                                          font="System")
shop_stats_strength_value.grid(row=0, column=1,
                               padx=0, pady=(10, 5),
                               sticky='w')

shop_stats_dexterity_value = tkinter.Label(shop_stats,
                                           bg="#2e2e2e", fg="#f1f1f1",
                                           font="System")
shop_stats_dexterity_value.grid(row=1, column=1,
                                padx=0, pady=(5, 10),
                                sticky='w')

shop_allies = tkinter.Frame(right_panel,
                            bg="#2e2e2e")
shop_allies.grid(row=2, column=0,
                 padx=20, pady=10,
                 sticky="nsew")

shop_allies.grid_columnconfigure(0,
                                weight=125,
                                minsize=125)

shop_allies.grid_columnconfigure(1,
                                weight=100,
                                minsize=100)

shop_allies.grid_rowconfigure([0, 1, 2, 3],
                             weight=1)

shop_allies_peasants = tkinter.Button(shop_allies,
                                     bg="#2e1e1e", fg="#f1f1f1",
                                     text="Hire peasant",
                                     command=upgrade_peasants)
shop_allies_peasants.grid(row=0, column=0,
                         padx=10, pady=(10, 5),
                         sticky="nsew")

shop_allies_knights = tkinter.Button(shop_allies,
                                     bg="#2e1e1e", fg="#f1f1f1",
                                     text="Hire knight",
                                     command=upgrade_knights)
shop_allies_knights.grid(row=1, column=0,
                         padx=10, pady=5,
                         sticky="nsew")

shop_allies_adventurers = tkinter.Button(shop_allies,
                                     bg="#2e1e1e", fg="#f1f1f1",
                                     text="Hire adventurer",
                                     command=upgrade_adventurers)
shop_allies_adventurers.grid(row=2, column=0,
                         padx=10, pady=5,
                         sticky="nsew")

shop_allies_heroes = tkinter.Button(shop_allies,
                                     bg="#2e1e1e", fg="#f1f1f1",
                                     text="Hire hero",
                                     command=upgrade_heroes)
shop_allies_heroes.grid(row=3, column=0,
                         padx=10, pady=(5, 10),
                         sticky="nsew")

shop_allies_peasants_value = tkinter.Label(shop_allies,
                                          bg="#2e2e2e", fg="#f1f1f1",
                                          font="System")
shop_allies_peasants_value.grid(row=0, column=1,
                               padx=0, pady=(10, 5),
                               sticky='w')

shop_allies_knights_value = tkinter.Label(shop_allies,
                                          bg="#2e2e2e", fg="#f1f1f1",
                                          font="System")
shop_allies_knights_value.grid(row=1, column=1,
                               padx=0, pady=5,
                               sticky='w')

shop_allies_adventurers_value = tkinter.Label(shop_allies,
                                          bg="#2e2e2e", fg="#f1f1f1",
                                          font="System")
shop_allies_adventurers_value.grid(row=2, column=1,
                               padx=0, pady=5,
                               sticky='w')

shop_allies_heroes_value = tkinter.Label(shop_allies,
                                          bg="#2e2e2e", fg="#f1f1f1",
                                          font="System")
shop_allies_heroes_value.grid(row=3, column=1,
                               padx=0, pady=(5, 10),
                               sticky='w')

shop_skills = tkinter.Frame(right_panel,
                            bg="#2e2e2e")
shop_skills.grid(row=3, column=0,
                 padx=20, pady=(10, 20),
                 sticky="nsew")

shop_skills.grid_columnconfigure(0,
                                 weight=125,
                                 minsize=125)

shop_skills.grid_columnconfigure(1,
                                 weight=100,
                                 minsize=100)

shop_skills.grid_rowconfigure([0, 1, 2],
                              weight=1)


shop_skills_one = ttk.Progressbar(shop_skills,
                                  mode="determinate")

shop_skills_one.grid(row=0, column=0,
                     padx=20, pady=(20, 10),
                     sticky='nsew')

shop_skills_two = ttk.Progressbar(shop_skills,
                                  mode="determinate")

shop_skills_two.grid(row=1, column=0,
                     padx=20, pady=10,
                     sticky='nsew')

shop_skills_three = ttk.Progressbar(shop_skills,
                                    mode="determinate")

shop_skills_three.grid(row=2, column=0,
                       padx=20, pady=(10, 20),
                       sticky='nsew')

shop_skills_one_value = tkinter.Label(shop_skills,
                                      bg="#2e2e2e", fg="#f1f1f1",
                                      font="System")
shop_skills_one_value.grid(row=0, column=1,
                           padx=0, pady=(20, 10),
                           sticky='w')

shop_skills_two_value = tkinter.Label(shop_skills,
                                      bg="#2e2e2e", fg="#f1f1f1",
                                      font="System")
shop_skills_two_value.grid(row=1, column=1,
                           padx=0, pady=10,
                           sticky='w')

shop_skills_three_value = tkinter.Label(shop_skills,
                                        bg="#2e2e2e", fg="#f1f1f1",
                                        font="System")
shop_skills_three_value.grid(row=2, column=1,
                             padx=0, pady=(10, 20),
                             sticky='w')
# INITIATE ROOT #
enemy_update()
player_update()
shop_update()

root.geometry("800x600")
root.minsize(800, 600)
root.after(500, game_tick)
root.mainloop()
