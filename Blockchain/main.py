from customer import Customer
from merchant import Merchant
from minernode import MinerNode

import datetime
from dateutil.relativedelta import relativedelta
import random
import sys

def generate_datestring(date: datetime.date):
    datestring_month = str(date.month)
    if (len(datestring_month) == 1):
        datestring_month = "0" + datestring_month

    datestring_day = str(date.day)
    if (len(datestring_day) == 1):
        datestring_day = "0" + datestring_day

    return datestring_month + datestring_day + str(date.year)

def generate_transaction(customers: list, merchants: list, miner: MinerNode, curr_date: datetime.date) -> datetime.date:
    customer_id = random.randint(0, 4)
    merchant_id = random.randint(0, 1)

    curr_date = curr_date + relativedelta(days = random.randint(14, 30))
    datestring = generate_datestring(curr_date)

    amount = round(random.uniform(0.01, 999999.99), 2)

    signed_transaction = merchants[merchant_id].create_transaction(customers[customer_id], datestring, amount)

    miner.add_block(signed_transaction)

    return curr_date


if __name__ == "__main__":
    customers = [Customer() for i in range(5)]
    merchants = [Merchant() for i in range(2)]
    #miner = MinerNode(0)

    #for i in range(0, 25):
    #    curr_date = generate_transaction(customers, merchants, miner, curr_date)

    #if sys.argv[1] == '0':
    #    miner.display()
    #elif sys.argv[1] == '1':
    #    if miner.is_chain_valid():
    #        print("The Blockchain has not been tampered with!")
    #    else:
    #        print("The Blockchain HAS been tampered with!")
    #    miner.increment_fifteen()
    #    if miner.is_chain_valid():
    #        print("The Blockchain has not been tampered with!")
    #    else:
    #        print("The Blockchain HAS been tampered with!")
    #elif sys.argv[1] == '2':
    #    miner.print_customer_three(customers[2])
    #elif sys.argv[1] == '3':
    #    miner.print_merchant_two(merchants[1])

    #if sys.argv[1] == '0':
    #    pass
    #elif sys.argv[1] == '1':
    #    pass
    #elif sys.argv[1] == '2':
    #    pass

    miner_a = MinerNode(0)
    miner_b = MinerNode(5)
    miner_c = MinerNode(10)

    curr_date = datetime.date(2020, 1, 1)

    for i in range(0, 25):
        curr_date = generate_transaction(customers, merchants, miner_a, curr_date)

    curr_date = datetime.date(2020, 1, 1)

    for i in range(0, 25):
        curr_date = generate_transaction(customers, merchants, miner_b, curr_date)

    curr_date = datetime.date(2020, 1, 1)

    for i in range(0, 25):
        curr_date = generate_transaction(customers, merchants, miner_c, curr_date)

    miner_a.output_to_file("a.csv")
    miner_b.output_to_file("b.csv")
    miner_c.output_to_file("c.csv")