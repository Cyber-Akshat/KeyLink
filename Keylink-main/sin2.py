# sin wrote all of this too btw

import random
import secrets
import string

def sort_list(accounts, sort):
    if sort == "a":
        return sorted(accounts, key=lambda d: d["name"].lower())
    elif sort == "ar":
        return sorted(accounts, key=lambda d: d["name"].lower(), reverse=True)
    elif sort == "w":
        return sorted(accounts, key=lambda d: d["website"].lower().removeprefix("https://").removeprefix("http://"))
    elif sort == "wr":
        return sorted(accounts, key=lambda d: d["website"].lower().removeprefix("https://").removeprefix("http://"), reverse=True)
    elif sort == "r":
        return sorted(accounts, key=lambda d: d["created"])
    elif sort == "o":
        return sorted(accounts, key=lambda d: d["created"], reverse=True)
    else:
        return None

def generate_password():
    length = random.randint(13,20)
    password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
    return password