from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import random
import logging

DEPTH = 6

import math
# class Country:
import threading
#     name = country_list.

ELECTRICITY_PRICE = 0.20 # E / kWh
CO2_PRICE = 28 # E/ton
CLEANNESS = 0.0005  # must be muliplied by a random number (after) units: tonCO2eq./kWh  0.0005 stands for average of 500gCO2eq./kWh


class User:
    def __init__(self):
        self.id = id(self)
        self.country = "Italy"
        self.tot_impact = 0
        # self.criteria = {"GHG":9.1}
        self.consumption = 1
        self.tot_consumption = 0
        self.balance = 0
        self.wealth = 0
        self.ownership_value = 0
        # self.energy_per_material = np.random.random(1) # kWh/unit output
        self.energy_per_material = np.random.random() * self.consumption # ton CO2 / unit output
        self.impact_per_material = CLEANNESS * self.energy_per_material  # Must be multiplied by consumption ton CO2 / unit output and Kwh --> must be multiplied by a random nr
        self.impact = 0.2 # ton CO2
        self.extractor = False
        self.dependencies = {}

    # amount is in $
    def sell(self, buyer, amount, bank, rec):
        # for seller in self.dependencies:
        price_increase = 1 + random.random()
        buyer.balance -= amount * self.energy_per_material * ELECTRICITY_PRICE * price_increase
        self.balance += amount * self.energy_per_material * ELECTRICITY_PRICE * price_increase # users sell at a random increased price from the objective value it has spent for its production
        buyer.wealth += self.consumption * ELECTRICITY_PRICE - self.impact * CO2_PRICE
        self.wealth -= self.consumption * ELECTRICITY_PRICE - self.impact * CO2_PRICE
        print("Buyer {0} bought from seller {1}".format(buyer.id, self.id))
        if rec < DEPTH:
            buyer.produce(amount, bank, rec)
        else:
            logging.info("**** DID NOT HAVE MONEY TO BUY")
            pass


    # amount is assumed to be exactly the energy required to produce it minus its impacts
    def produce(self, amount, bank, rec):
        if True or amount * self.energy_per_material * ELECTRICITY_PRICE < self.balance or amount * self.energy_per_material * ELECTRICITY_PRICE < self.wealth:
            self.consumption = self.energy_per_material * amount
            self.tot_consumption += self.consumption
            self.impact = self.impact_per_material * amount * (np.random.random())
            self.tot_impact += self.impact
            self.balance -= self.consumption * ELECTRICITY_PRICE
            self.wealth += self.consumption * ELECTRICITY_PRICE - self.impact * CO2_PRICE
            lend = bank.lend(self.consumption * ELECTRICITY_PRICE, self.impact*CO2_PRICE)
            print("User {0} has produced buying from energy bank {1}".format(self.id, bank.id))
            # self.balance += lend REMOVED USER IS COMPENSATED IN OTHER CURRENCY RELATIVE TO WEALTH
            plt.scatter(rec, self.consumption, c='b', marker='x', label='1')
            plt.scatter(rec, self.wealth, c='y', marker='x', label='3')
            # plt.scatter(rec, self.balance, c='g', marker='o', label='0')
            plt.scatter(rec, self.impact, c='r', marker='s', label='2')

            rec += 1
            if rec < DEPTH:
                for relative_user in self.dependencies.values():
                    self.sell(relative_user, amount=amount / 3, bank=bank, rec=rec)
            else:
                logging.info("**** DID NOT HAVE MONEY TO PRODUCE")
                pass
        else:
            print("User {0} could not buy because did not have enough money for pay electricity {1}".format(self.id,
                                                                                                            self.energy_per_material * amount * ELECTRICITY_PRICE))

    def get_balance(self):
        return self.balance

    def get_tot_impact(self):
        return self.tot_impact

    def get_ownership(self):
        return self.ownership_value

    def get_tot_consumption(self):
        return self.tot_consumption


class Bank:

    def __init__(self):
        self.id = id(self)
        self.name = "Vattenfall"
        self.balance = 1000000
        self.total_lend = 0

    def lend(self, amount, impact):
        # lend = math.log(amount)/math.log(impact) if amount/impact > 0 else -math.log10(amount)/ math.log10(impact)
        lend = amount /impact if amount / impact > 0 else amount / impact
        self.balance -= lend
        self.total_lend += lend
        return lend


class Reservoir:
    def __init__(self):
        self.country = "Italy"
        self.id = id(self)
        self.amount = 1000000
        self.price = 3 # $/unit
        self.value = self.amount * self.price

    def get_amount(self):
        return self.amount

    def get_value(self):
        return self.value

    def withdraw(self, amount):
        if amount > self.amount:
            print("Finished the resource {}".format(self.id))
            return False
        else:
            self.amount -= amount
            return True


# class Extractor(User):
#
#     def super__init__(self, reservoir):
#         # self.reservoir_id = reservoir.id
#         self.extractor = True
#
#     def extract(self, reservoir, amount, bank):
#         if reservoir.withdraw(amount):
#             self.consumption = self.energy_per_material * amount
#             self.tot_consumption += self.consumption
#             self.impact = self.impact_per_material * amount
#             self.tot_impact += self.impact
#             self.balance -= self.consumption * ELECTRICITY_PRICE
#             bank.lend(self.consumption * ELECTRICITY_PRICE, self.impact * CO2_PRICE )
#             self.balance += (self.consumption * ELECTRICITY_PRICE) / (self.impact*CO2_PRICE) if (self.consumption * ELECTRICITY_PRICE)/(self.impact*CO2_PRICE) > 0 else -(self.consumption * ELECTRICITY_PRICE)/(self.impact*CO2_PRICE)
#             self.wealth = self.consumption * ELECTRICITY_PRICE - self.impact * CO2_PRICE
#             self.consumption = 0
#             self.impact = 0





