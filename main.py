
import numpy as np
import random
from classes import User, CO2_PRICE, ELECTRICITY_PRICE, Reservoir, Bank
from collections import OrderedDict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter
import threading
NUMBER_OF_SALES = 2
NUMBER_OF_USERS = 6
NUMBER_OF_REPEATS = 1

# el = []
# for num in range(1000):
#     print(e for e in el)
# a = np.random.binomial(1000000, 0.9, (1,1000,10000))
# b = np.random.binomial(10000, 0.6, (1,1000,10000))
# c = np.random.binomial(100, 0.3, (1,1000,10000))
# d = np.random.binomial(10, 0.1, (1,1000,10000))


def generate_users():
    users = OrderedDict()
    for i in range(NUMBER_OF_USERS):
        user = User()
        users[str(user.id)] = user
    return users

# def generate_extractors():
#     extractors = OrderedDict
#     for i in range(3):
#         extractor = Extractor()
#         extractors[str(extractor.id)] = extractor


def generate_dependencies(users):
    temp_users = users.copy()
    for user in users.values():
        for i in range(NUMBER_OF_SALES):
            relative_user = random.choice(list(temp_users.values()))
            del temp_users[str(relative_user.id)]
            user.dependencies[str(relative_user.id)] = relative_user
        temp_users = users.copy()
    return users


users = generate_dependencies(generate_users())

bank = Bank()
count = 0

for i in range(NUMBER_OF_REPEATS):
    tot_wealth = 0
    tot_balance = 0
    # for user in users.values():
    user = users.popitem()[1]
    amount = 5
    user.produce(amount=amount, bank=bank, rec=count)
    count += 1
    # plt.scatter(count, tot_balance, c='k', marker='s', label='2')
    # plt.scatter(i, user.wealth, c='y', marker='x', label='3')
    # plt.scatter(i, user.balance, c='g', marker='o', label='0')
    # plt.scatter(i, user.tot_impact, c='r', marker='s', label='2')
    plt.savefig(
            str(CO2_PRICE).replace(".", "") + "_" + str(ELECTRICITY_PRICE).replace(".", "") + "_" + str(NUMBER_OF_USERS) + "_" + str(NUMBER_OF_REPEATS) + ".png")

    plt.show()


i = 0
for user in users.values():
    tot_wealth += user.wealth
    tot_balance += user.balance
    plt.scatter(i, tot_wealth, c='k', marker='x')
    plt.scatter(i, tot_balance, c='m', marker='x')
    plt.savefig(
        "tot_consumption_" + str(CO2_PRICE).replace(".", "") + "_" + str(ELECTRICITY_PRICE).replace(".", "") + "_" + str(
            NUMBER_OF_USERS) + "_" + str(NUMBER_OF_REPEATS) + ".png")
    i += 1
plt.show()

#np.random.lognormal(1, 0.5, 10)












