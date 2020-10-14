import csv
import sys

import pandas
from datetime import datetime


def read_file_old():
    with open('customer_file.csv') as customer_file:
        csv_reader = csv.reader(customer_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            print(row)
            data.append(row)
            line_count += 1
    return data


def read_file():
    # data = pandas.read_csv('customer_file.csv', parse_dates=['Last Modified'])
    data = pandas.read_csv('customer_file.csv', index_col='Acc_No', parse_dates=['Last Modified'])

    return data


def last_account():
    with open('customer_file.csv') as customer_file:
        csv_reader = csv.reader(customer_file, delimiter=',')
        last_account_number = 0
        for row in csv_reader:
            last_account_number = row[0]
        return int(last_account_number)


def start():
    # print(last_account())
    print("Welcome! \n 1. Login \n 2. Create new account")
    choice = input("Enter your choice: ")

    if choice == '2':
        register()
    else:
        login()


def login():
    acc_no = input("Enter your Account Number: ")
    pin = input("Enter your Pin: ")
    data = read_file()
    # print(data)
    # print(data.loc[int(acc_no), 'Pin'])
    # print(data.get(acc_no))
    try:
        user = data.loc[int(acc_no), :]
    except KeyError:
        print("Invalid Account Number")
        sys.exit()
    # if acc_no in data.values:
    #     print("Account Valid")
    #     user = data.loc[int(acc_no), :]
    # else:
    #     print("Account invalid")

    # user = data.loc[int(acc_no), :]
    # print(user)
    pin_from_db = data.loc[int(acc_no), 'Pin']
    if pin == pin_from_db:
        print("Welcome " + user[0] + "\nYour Current Balance is " + str(user[2]))
        user_operations(acc_no)
    else:
        print("Incorrect Password")


def user_operations(acc_no):
    print("\n 1. Withdraw Money \n 2. Deposit Money\n 3. Send Money")
    choice = input("Enter your choice: ")
    data = read_file()

    if choice == '1':
        w_amount = input("Enter amount: ")
        balance = data.at[int(acc_no), 'Balance']
        if int(balance) >= int(w_amount):
            data.at[int(acc_no), 'Balance'] = int(balance) - int(w_amount)
            data.at[int(acc_no), 'Last Modified'] = datetime.now()
            print("Your remaining balance is " + str(data.at[int(acc_no), 'Balance']))
            data.to_csv('customer_file.csv')
        else:
            print("You do not have enough balance for this transaction")

    if choice == '2':
        d_amount = input("Enter amount: ")
        # data = read_file()
        balance = data.at[int(acc_no), 'Balance']
        data.at[int(acc_no), 'Balance'] = int(balance) + int(d_amount)
        data.at[int(acc_no), 'Last Modified'] = datetime.now()
        print("Your new balance is " + str(data.at[int(acc_no), 'Balance']))
        data.to_csv('customer_file.csv')

    if choice == '3':
        receiver_account = input("Enter account number: ")
        try:
            # receiver = data.loc[int(receiver_account), :]
            balance = data.at[int(acc_no), 'Balance']
            receiver_name = data.loc[int(receiver_account), 'Name']
            receiver_balance = int(data.loc[int(receiver_account), 'Balance'])
        except KeyError:
            print("Invalid Account Number")
            sys.exit()
        t_amount = input("Amount you want to send: ")
        print("Do you want to send " + t_amount + " to " + receiver_name + "?")
        input("Press Enter to continue...")
        if int(balance) >= int(t_amount):
            data.at[int(acc_no), 'Balance'] = int(balance) - int(t_amount)
            data.at[int(receiver_account), 'Balance'] = receiver_balance + int(t_amount)
            data.at[int(receiver_account), 'Last Modified'] = datetime.now()
            print("Your remaining balance is " + str(data.at[int(acc_no), 'Balance']))
            data.to_csv('customer_file.csv')
        else:
            print("You do not have enough balance for this transaction")

        # send_amount = input("Enter amount: ")
        # data = read_file()
        # balance = data.at[int(acc_no), 'Balance']
        # if int(balance) >= int(w_amount):
        #     data.at[int(acc_no), 'Balance'] = int(balance) - int(w_amount)
        #     data.at[int(acc_no), 'Last Modified'] = datetime.now()
        #     print("Your remaining balance is " + str(data.at[int(acc_no), 'Balance']))
        #     data.to_csv('customer_file.csv')
        # else:
        #     print("You do not have enough balance for this transaction")


def register():
    name = input("Enter your name: ")
    pin = input("Enter your pin: ")
    number = last_account() + 1
    balance = 0
    with open('customer_file.csv', mode='a') as customer_file:
        customer_writer = csv.writer(customer_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        customer_writer.writerow([number, name, pin, balance, datetime.now()])
    print("Your Account Number is: " + str(number))
    exit()


if __name__ == '__main__':
    start()
