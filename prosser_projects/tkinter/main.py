"""
Prosser Group Project #1.

Idle Clicker Game by Jack, Dane, and Autum
"""

#       IMPORTS        #


# Import tkinter for windows GUI and tkk for additional widgets. Because we're
# making a small program we can import everything at the start. If it was
# bigger, it may be better to import them in parts throughout the code.


import tkinter
import tkinter.ttk as ttk

from random import randint
from time import sleep


#       CLASSES        #


# Create classes to be used for functions and data-saving.
# It's better to use classes than global variables because they only need to be
# referenced a single time instead of multiple. Imagine a calender instead of
# multiple sticky notes.


class EnemyValues(dict):
    """This class tracks all values and methods related to the ENEMY."""

    def __init__(self):
        """Initialize the ENEMY from scratch with starting values."""
        self.reset()

    def reset(self):
        """Reset the values of ENEMY."""
        self.randomize_name()
        self.randomize_health()

    def death(self):
        """Reset the values of ENEMY when killed."""
        self.randomize_name()

        # This code is for the health scaling of the ENEMY. Basically, the math
        # if a random number between 25 and 50 that gets multiplied by the
        # number of kills the player has divided by 10. To have scaling health
        # just the kill count could have been enough, but it would multiply
        # too quickly and feel terrible for the player, therefore we dilute
        # it by dividing the value by 10,
        self["health"] = round(randint(25, 50) * PLAYER['kill_count'] / 10)
        self["health_current"] = self["health"]

    def randomize_name(self):
        """Randomize the name value."""
        # Since I wanted it to be easy to input new names, I have the randint
        # look through the first value of the list to the last. Because the
        # last can now scale, we don't have to edit this code later. The len
        # function counts the total items in a list using human counting,
        # starting at 1. Because computers start with 0, we have to subtract
        # 1 to make sure the values stay valid.
        self["name"] = (f"{firstNames[randint(0, len(firstNames) - 1)]}"
                        + f" {lastNames[randint(0, len(lastNames) - 1)]}")

    def randomize_health(self):
        """Randomize the health value."""
        # Basically the same code above but used in initialization to make sure
        # the program doesn't crash by division by zero.
        self["health"] = round(randint(25, 50) * 1 / 10)
        self["health_current"] = self["health"]


class PlayerValues(dict):
    """This class tracks all values and methods realted to the PLAYER."""

    def __init__(self):
        """Initialize the PLAYER with a random name and starting values."""
        # Same name code for the PLAYER as the ENEMY.
        self["name"] = (f"{firstNames[randint(0, len(firstNames) - 1)]}"
                        + f" {lastNames[randint(0, len(lastNames) - 1)]}")

        self["strength"]: int = 1
        self["crit_chance"]: int = 5
        self["allies"]: int = 0
        self["gold"]: int = 0
        self["kill_count"]: int = 0

    def upgrade(self, value, quantity, cost):
        """Use for easily creating upgrades."""
        if self['gold'] < cost:
            print_console("Insufficient gold")
            return False
        self[value] += quantity
        self['gold'] -= cost
        return True


class ShopValues(dict):
    """This class tracks all values and methods related to the SHOP."""

    def __init__(self):
        """Initialize starting values for SHOP."""
        self["strength_cost"]: int = 10
        self["allies_cost"]: int = 25

    def cost_multiplier(self, cost, multiplier):
        """Multiply cost by multiplier."""
        self[cost] = round(self[cost] * multiplier)

    def buy(self, stat):
        """Input stat to upgrade to call method for upgrading."""
        method_name = 'upgrade_' + str(stat)
        method = getattr(self, method_name, lambda: "Invalid")
        print(method)
        return method()

    def upgrade_strength(self):
        """Increase strength value of PLAYER."""
        if not PLAYER.upgrade('strength', 1, self['strength_cost']):
            pass
        else:
            self.cost_multiplier('strength_cost', 1.25)

            goldLabel["text"] = f"Gold: {PLAYER['gold']}"
            upgradeStrengthCost["text"] = f"{SHOP['strength_cost']}"
            statsStrength["text"] = f"Strength: {PLAYER['strength']}"

            print_console("Strength upgraded.\n")

    def upgrade_allies(self):
        """Increase allies value of PLAYER."""
        if not PLAYER.upgrade('allies', 1, self['allies_cost']):
            pass
        else:
            self.cost_multiplier('allies_cost', 1.5)

            goldLabel["text"] = f"Gold: {PLAYER['gold']}"
            upgradeAlliesCost["text"] = f"{SHOP['allies_cost']}"
            statsAllies["text"] = f"Allies: {PLAYER['allies']}"

            print_console("Ally hired.\n")


#       VARIABLES      #


# We want to make variables that can be used to refer back to values we need.
# It's best to name commonly used variables either the full word or shorthand
# of the intended function or usage to that it's easier to understand later.


# This is a list of names that gets randomly selected from on ENEMY deaths and
# PLAYER creation. Simply add a name anywhere or change one for it to be used.
firstNames: list = ["Helga", "Bulgrif", "Fluffy", "Chad", "Karen"]
lastNames: list = ["Crusher", "Mallet", "Sjorborn", "Pancakes", "Smith"]


# Since we'll be using the classes a lot, we want to create variables that we
# can use as shorthand for the class names. For example, typing PLAYER is
# faster than typing PlayerValues(). The variables also "create" the classes.
# A class is like a blueprint while this turns it into an actual object.
ENEMY = EnemyValues()
PLAYER = PlayerValues()
SHOP = ShopValues()


#     ROOT CREATION    #


# The code here creates and modifies the root.


# This code creates the overall window and gives it a title. It is often
# refered to as the "root."
window = tkinter.Tk()
window.title("Clicker RPG")


# We can use the tkk package to import custom themes to our tkinter project.
# Because we're fighting an ENEMY, it wouldn't make sense for the health bar to
# be green, therefore, we change it to red here.
appTheme = ttk.Style()
appTheme.theme_use('winnative')
appTheme.configure("red.Horizontal.TProgressbar",
                   background='red', foreground='red')


#       FUNCTIONS      #


# Functions are the main math and logic behind the game, therefore they're
# often quite a large section of the overall code. It's best to define them
# in order of independence as well as dependency on one another and size.
# For example, I made the close() function first because it's small and doesn't
# depend on any other function. In a later place, I put kill() before
# allies_attack() and attack() because it's used in both of them.


def close():
    """Close the main window."""
    window.destroy()


def print_console(value):
    """Print value to the console."""
    consoleGUI.insert("end", f"{value}\n")
    consoleGUI.see("end")


def critical_hit():
    """Return true or false based on random chance."""
    crit: int = randint(1, 100)
    return bool(crit <= PLAYER['crit_chance'])


def kill():
    """Execute when the enemy is killed."""
    # Since this is an RPG, randomness is commmon. To add some more, I wanted
    # the gold gain to be random too. This code also lets the gold scale with
    # ENEMY health so that it doesn't have to be tweaked. The math is simply
    # ENEMY health divided by 5 multiplied by a random number between 1 and 3.
    random_multiplier = randint(1, 3)
    gold_gain = round((ENEMY['health'] / 5) * random_multiplier)
    PLAYER['gold'] += gold_gain
    PLAYER['kill_count'] += 1
    print_console(f"{ENEMY['name']} Killed\nReceived {gold_gain} Gold!\n")

    ENEMY.death()

    if not ENEMY['name'] == PLAYER['name']:
        pass
    else:
        print_console("You found yourself!\n")

    healthBar.config(maximum=ENEMY['health'],
                     value=ENEMY['health'])
    goldLabel["text"] = f"Gold: {PLAYER['gold']}"

    statsKillCount["text"] = f"Kills: {PLAYER['kill_count']}"


def allies_attack():
    """Ally damage loop."""
    ENEMY['health_current'] -= PLAYER['allies'] * PLAYER['strength']
    healthBar["value"] = ENEMY['health_current']

    if not healthBar["value"] <= 0:
        pass
    else:
        kill()

    healthNumber.config(text=f"{ENEMY['health_current']}/{ENEMY['health']}")
    # Continue the loop
    window.after(1000, allies_attack)


# Function to deal damage per click
def attack():
    """Player damage per click."""
    if not critical_hit():
        ENEMY['health_current'] -= PLAYER['strength']
    else:
        ENEMY['health_current'] -= PLAYER['strength'] * 2
        print_console(f"Critical hit on {ENEMY['name']}!\n")

    healthBar["value"] = ENEMY['health_current']

    if not ENEMY['health_current'] <= 0:
        pass
    else:
        kill()

    healthNumber.config(text=f"{ENEMY['health_current']}/{ENEMY['health']}")

    attackProc = tkinter.Frame(middlePanel,
                               width = 20, height = 20,
                               bg = "#ffffff")
    attackProc.place(relx=.5, rely=.5)
    sleep(0.2)
    attackProc.destroy()


#    PANEL CREATION    #


# Tkinter is very difficult to use to design nice looking forms. It's also
# difficult to add additional widgets where you want them. To fix this problem,
# I created a "base" to work from. You can configure the size of the rows and
# columns to create a certain width and height. THen I created 3 Frames to put
# into those columns. I call them "Panels." You can use them to easily place
# widgets where you want in the form.


# Config column and row size + sizing
window.columnconfigure([0, 1, 2],
                       weight=1,
                       minsize=285)

window.rowconfigure(0,
                    weight=1,
                    minsize=570)

# Add "Panels"
leftPanel = tkinter.Frame(window,
                          bg="#1e1e1e",
                          padx=5, pady=10)

leftPanel.grid(sticky="ns")

middlePanel = tkinter.Frame(window,
                            bg="#1e1e1e",
                            padx=5, pady=10)

middlePanel.grid(sticky="ns", column=1, row=0)

rightPanel = tkinter.Frame(window,
                           bg="#1e1e1e",
                           padx=5, pady=10)

rightPanel.grid(sticky="ns", column=2, row=0)


#   LEFT PANEL ASSETS  #


# All the assets that are placed on the left panel.
# This panel is mainly used for PLAYER related information.


# Title for PLAYER statistics
statsTitle = tkinter.Label(leftPanel,
                           text="Statistics",
                           bg="#1e1e1e", fg="#f1f1f1",
                           font=("System", 20))

statsTitle.grid(pady=(50, 20))

# PLAYER's randomized name
statsName = tkinter.Label(leftPanel,
                          text=PLAYER['name'],
                          bg="#1e1e1e", fg="#f1f1f1",
                          font="System")

statsName.grid(row=1, pady=(0, 30))

# PLAYERS current strength
statsStrength = tkinter.Label(leftPanel,
                              text=f"Strength: {PLAYER['strength']}",
                              bg="#1e1e1e", fg="#f1f1f1",
                              height=2, width=20,
                              font=("System", 12))

statsStrength.grid(row=2)

# PLAYERS current allies
statsAllies = tkinter.Label(leftPanel,
                            text=f"Allies: {PLAYER['allies']}",
                            bg="#1e1e1e", fg="#f1f1f1",
                            height=2, width=20,
                            font=("System", 12))

statsAllies.grid(row=3)

# PLAYERS current kill count
statsKillCount = tkinter.Label(leftPanel,
                               text=f"Kills: {PLAYER['kill_count']}",
                               bg="#1e1e1e", fg="#f1f1f1",
                               height=2, width=20,
                               font=("System", 12))

statsKillCount.grid(row=4)

# Frame to hold console wdigets
console = tkinter.Frame(leftPanel,
                        bg="#1e1e1e",
                        pady=30)

console.grid(row=10, column=0)

# Console for PLAYER feedback
consoleGUI = tkinter.Text(console,
                          bg="#0e0e0e", fg="#f1f1f1",
                          height=15, width=30,
                          font="System")

consoleGUI.grid(row=0, sticky="s")

# Scrollbar for the console
consoleScrollbar = tkinter.Scrollbar(console)
consoleScrollbar.grid(row=0, column=1, sticky='ns')

consoleGUI.config(yscrollcommand=consoleScrollbar.set)
consoleScrollbar.config(command=consoleGUI.yview)


#  MIDDLE PANEL ASSETS #


# All the assets that are placed on the middle panel.
# This panel is mainly used for ENEMY related information.


# Frame to hold ENEMY health widgets
healthFrame = tkinter.Frame(middlePanel, bg="#1e1e1e")
healthFrame.grid()

# ENEMY health bar
healthBar = ttk.Progressbar(healthFrame,
                            mode='determinate',
                            style="red.Horizontal.TProgressbar",
                            maximum=ENEMY['health'],
                            value=ENEMY['health'], length=200)

healthBar.grid(row=0)

# ENEMY precise health value
healthNumber = tkinter.Label(healthFrame,
                             text=f"{ENEMY['health_current']}"
                                  + f"/{ENEMY['health']}",
                             bg="#1e1e1e", fg="#f1f1f1",
                             width=5,
                             padx=10, pady=50,
                             font=("System", 20))
healthNumber.grid(row=0, column=1)

# ENEMY
enemy = tkinter.Button(middlePanel,
                       height=15, width=20,
                       pady=10,
                       command=attack)
enemy.grid(row=1)

# ENEMY randomized name
enemyName = tkinter.Label(middlePanel,
                          text=ENEMY['name'],
                          bg="#1e1e1e", fg="#f1f1f1",
                          font="System")
enemyName.grid(row=2, pady=(0, 30))


#  RIGHT PANEL ASSETS  #


# All the assets that are placed on the right panel.
# This panel is mainly used for SHOP related information.


# PLAYER gold count
goldLabel = tkinter.Label(rightPanel,
                          text=f"Gold: {PLAYER['gold']}",
                          bg="#1e1e1e", fg="#f1f1f1",
                          pady=50,
                          font=("System", 20))
goldLabel.grid(row=1)

# SHOP buy strength button
upgradeStrength = tkinter.Button(rightPanel,
                                 text="Upgrade your strength!",
                                 bg="#0e0e0e", fg="#f1f1f1",
                                 height=2, width=20,
                                 command=lambda: SHOP.buy('strength'),
                                 font=("System", 12))
upgradeStrength.grid(row=2)

# SHOP buy strength cost
upgradeStrengthCost = tkinter.Label(rightPanel,
                                    text=SHOP['strength_cost'],
                                    bg="#1e1e1e", fg="#f1f1f1",
                                    padx=10,
                                    font=("System", 12))
upgradeStrengthCost.grid(row=2, column=1)

# SHOP buy allies button
upgradeAllies = tkinter.Button(rightPanel,
                               text="Hire new allies!",
                               bg="#0e0e0e", fg="#f1f1f1",
                               height=2, width=20,
                               font=("System", 12),
                               command=lambda: SHOP.buy('allies'))
upgradeAllies.grid(row=3)

# SHOP buy allies cost
upgradeAlliesCost = tkinter.Label(rightPanel,
                                  text=SHOP['allies_cost'],
                                  bg="#1e1e1e", fg="#f1f1f1",
                                  padx=10,
                                  font=("System", 12))
upgradeAlliesCost.grid(row=3, column=1)


#     INITIATE ROOT    #


# This code configures the last bit of the root we need and runs the entire
# window, effectively starting the game. We also tell the code to start
# running our loop before it starts.


# Change window size and color
window.geometry("900x600")
window.config(bg='#1e1e1e')

# Start loop and initialize the window
window.after(1000, allies_attack)
window.mainloop()
