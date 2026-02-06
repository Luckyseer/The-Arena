from __future__ import print_function  # For compatibility with python 2.x

from math import floor

from .data_loader import item_data


class Player:
    """Hold all the player information"""

    def __init__(
        self,
        item_data=item_data,
        name="Zen",
        health=100,
        mana=50,
        strength=10,
        magic=20,
        defence=10,
        luck=2,
    ):
        self.name = name
        self.hp = health
        self.curhp = self.hp
        self.mp = mana
        self.curmp = self.mp
        self.cur_weapon = 0  # set the id of the item
        self.cur_armour = 0  # NOTE TO SELF: DON'T FORGET TO CHANGE DEFAULT ITEMS BACK!!
        self.cur_accessory = 0
        self.stre = strength  # Player's base stats
        self.defe = defence
        self.mag = magic
        self.luck = luck
        self.stat_points = 0
        self.expreq = 0
        # Player's stats from equipment
        self.add_stre = (
            item_data["weapons"][self.cur_weapon]["atk"]
            + item_data["armours"][self.cur_armour]["atk"]
            + item_data["accessories"][self.cur_accessory]["atk"]
        )
        self.add_defe = (
            item_data["weapons"][self.cur_weapon]["def"]
            + item_data["armours"][self.cur_armour]["def"]
            + item_data["accessories"][self.cur_accessory]["def"]
        )
        self.add_mag = (
            item_data["weapons"][self.cur_weapon]["mag"]
            + item_data["armours"][self.cur_armour]["mag"]
            + item_data["accessories"][self.cur_accessory]["mag"]
        )
        self.add_luck = luck
        self.progress = 1  # progress in game
        self.gold = 1500000
        self.level = 1
        self.hours = 6  # in-game clock values
        self.minutes = 0  # ^
        self.exp = 0
        self.inventory = []
        self.wep_owned = []  # Used to store ids of currently owned weapons
        self.arm_owned = []
        self.acc_owned = []
        self.pclass = "mage"
        self.fkills = 0  # Kills in floor
        self.tkills = 0  # Total Kills
        self.scene = "menu"
        # Flag to check if player visited town or not.
        self.town_first_flag = False
        # Flag for whether the player paid the girl during the town scene
        self.paid_girl_flag = False

    def xp_till_levelup(self, currentlevel):  # Experience needed to level up
        self.expreq = floor((currentlevel**4) / 5)
        return self.expreq

    def check_levelup(self):  # Check if player has leveled up
        self.xp_till_levelup(self.level)
        print(f"Exp:{self.exp}, to_lvl:{self.xp_till_levelup(self.level)}")
        if self.exp >= self.expreq:
            return True
        else:
            return False

    def update_stats(self):
        self.add_stre = (
            item_data["weapons"][self.cur_weapon]["atk"]
            + item_data["armours"][self.cur_armour]["atk"]
            + item_data["accessories"][self.cur_accessory]["atk"]
        )
        self.add_defe = (
            item_data["weapons"][self.cur_weapon]["def"]
            + item_data["armours"][self.cur_armour]["def"]
            + item_data["accessories"][self.cur_accessory]["def"]
        )
        self.add_mag = (
            item_data["weapons"][self.cur_weapon]["mag"]
            + item_data["armours"][self.cur_armour]["mag"]
            + item_data["accessories"][self.cur_accessory]["mag"]
        )

    def set_player_stats(self, **kwargs):
        """For debug purposes"""
        for stat, value in kwargs.items():
            if stat == "strength" or stat == "stre":
                self.stre = value
            elif stat == "defence" or stat == "defe":
                self.defe = value
            elif stat == "magic" or stat == "mag":
                self.mag = value
            elif stat == "luck" or stat == "luk":
                self.luck = value
            elif stat == "health":
                self.hp = self.curhp = value
            elif stat == "mana":
                self.mp = self.curmp = value
            elif stat == "level":
                self.level = value
