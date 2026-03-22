# sin wrote all of this btw
import datetime
import json
import os

def save_account(name, password, website, filename="accounts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            accounts = json.load(f)
    else:
        accounts = []

    account = {
        "name": name,
        "password": password,
        "website": website,
        "created": datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }

    accounts.append(account)

    with open(filename, "w") as f:
        json.dump(accounts, f, indent=4)

def load_accounts(filename="accounts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        with open(filename, "w") as f:
            json.dump([], f, indent=4)
            return json.load(f)
