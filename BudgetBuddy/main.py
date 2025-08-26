import os
import csv
import json
from datetime import datetime

# Files
CSV_FILE = "expenses.csv"
DEP_FILE = "deposits.csv"
BAL_FILE = "balances.json"

# Default storage
balances = {
    "Daily": 0,
    "Family": 0,
    "LongTerm": 0,
    "BankAccount": 0
}

# Percentages
percentages = {
    "Daily": 0.5,
    "Family": 0.2,
    "LongTerm": 0.3
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def ascii_banner():
    print(r"""
  ____        _        __  __                  
 |  _ \  __ _| |_ __ _|  \/  | ___ _ __  _   _ 
 | | | |/ _` | __/ _` | |\/| |/ _ \ '_ \| | | |
 | |_| | (_| | || (_| | |  | |  __/ | | | |_| |
 |____/ \__,_|\__\__,_|_|  |_|\___|_| |_|\__,_|
   SIMPLE MONEY MANAGER
    """)

def load_balances():
    global balances
    if os.path.exists(BAL_FILE):
        with open(BAL_FILE, "r", encoding="utf-8") as f:
            balances = json.load(f)

def save_balances():
    with open(BAL_FILE, "w", encoding="utf-8") as f:
        json.dump(balances, f, indent=4)

def display_balances():
    print("\n=== Current Balances ===")
    for k, v in balances.items():
        print(f"{k:<12}: {v} DA")
    print("========================\n")

def record_expense(category, amount, description):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), category, amount, description])

def record_deposit(amount, source, split_data):
    with open(DEP_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), amount, source, split_data])

# --- NEW helper: round to nearest 5
def round5(x):
    return int(round(x / 5.0) * 5)

def add_money(amount):
    source = input("Where did this money come from? (gift, pocket money, etc.): ")
    if amount <= 50:
        r = round5(amount)
        balances["Daily"] += r
        split_data = f"Daily={r}"
        print(f"{amount} DA added to Daily (rounded to {r}, too small to split).")
    else:
        d = amount * percentages["Daily"]
        f = amount * percentages["Family"]
        l = amount * percentages["LongTerm"]

        # round each to 5
        d_r, f_r, l_r = round5(d), round5(f), round5(l)

        # fix rounding error
        total = d_r + f_r + l_r
        diff = amount - total
        d_r += diff  # adjust Daily

        balances["Daily"] += d_r
        balances["Family"] += f_r
        balances["LongTerm"] += l_r

        split_data = f"Daily={d_r}, Family={f_r}, LongTerm={l_r}"
        print(f"{amount} DA split into {split_data} (rounded).")

    save_balances()
    record_deposit(amount, source, split_data)

def deposit_to_bank():
    if balances["LongTerm"] < 2000:
        print("⚠ You need at least 2000 DA in LongTerm to deposit to the bank.")
        return

    print(f"You have {balances['LongTerm']} DA in LongTerm.")
    try:
        amt = int(input("Enter amount to deposit into BankAccount (must be multiple of 5): "))
        amt = round5(amt)

        if amt > balances["LongTerm"]:
            print("⚠ Not enough in LongTerm.")
            return

        if amt < 2000:
            print("⚠ You can only deposit 2000 DA or more.")
            return

        balances["LongTerm"] -= amt
        balances["BankAccount"] += amt
        save_balances()

        # record the deposit
        record_deposit(amt, "LongTerm", "Deposit to BankAccount")

        print(f"✅ Deposited {amt} DA to BankAccount.")
    except:
        print("Invalid input!")

def take_money():
    display_balances()
    print("Choose a jar to take from:")
    print("1. Daily")
    print("2. Family")
    print("3. LongTerm")
    print("4. BankAccount")
    choice = input("Enter option: ")

    categories = {"1": "Daily", "2": "Family", "3": "LongTerm", "4": "BankAccount"}

    if choice not in categories:
        print("Invalid choice.")
        return

    category = categories[choice]
    try:
        amt = int(input(f"Enter amount to take from {category}: "))
        if amt > balances[category]:
            print("Not enough balance!")
            return
        desc = input("What did you spend it on? ")

        balances[category] -= amt
        record_expense(category, amt, desc)
        save_balances()
        print(f"{amt} DA taken from {category} for: {desc}")
    except:
        print("Invalid input!")

def menu():
    load_balances()

    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    if not os.path.exists(DEP_FILE):
        with open(DEP_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Amount", "Source", "Split"])

    while True:
        clear()
        ascii_banner()
        display_balances()
        print("1. Add Money")
        print("2. Take Money (Expense)")
        print("3. Deposit LongTerm to Bank")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            try:
                amt = int(input("Enter amount (DA): "))
                add_money(amt)
            except:
                print("Invalid input!")
            input("Press Enter to continue...")
        elif choice == "2":
            take_money()
            input("Press Enter to continue...")
        elif choice == "3":
            deposit_to_bank()
            input("Press Enter to continue...")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    menu()
