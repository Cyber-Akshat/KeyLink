import tkinter as tk
from tkinter import ttk
import random
import secrets
import string
import re
import os
import json
import datetime
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

ACCOUNTS_FILE = "accounts.json"
MASTER_FILE = "master.key"

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
        return accounts

def validate_key(key):
    if len(key) < 15:
        raise ValueError("Key must be at least 15 characters long")
    if not re.search(r"[A-Z]", key):
        raise ValueError("Key must be at least one uppercase letter")
    if not re.search(r"""[!@#$%^&*()-_=+{}[]|\\:;'",.?~]""", key):
        raise ValueError("Key must contain at least one special character")

def derive_key(password, salt):
    validate_key(password)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_data(data, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    return salt, Fernet(key).encrypt(data.encode())

def generate_password():
    length = random.randint(13, 20)
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            json.dump([], f)
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

def save_master_key(key):
    salt = os.urandom(16)
    hashed = derive_key(key, salt)
    with open(MASTER_FILE, "w") as f:
        json.dump({"salt": base64.b64encode(salt).decode(), "hash": hashed.decode()}, f)

def verify_master_key(key):
    with open(MASTER_FILE, "r") as f:
        data = json.load(f)
    salt = base64.b64decode(data["salt"])
    return derive_key(key, salt).decode() == data["hash"]

def refresh_table(accounts):
    tree.delete(*tree.get_children())
    for acc in accounts:
        tree.insert("", tk.END, values=(acc["website"], acc["name"], "Encrypted"))

def sort_and_refresh(code):
    global current_accounts
    current_accounts = sort_list(current_accounts, code)
    refresh_table(current_accounts)

def gui_generate_password():
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generate_password())

def save_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if not website or not username or not password:
        status_label.config(text="Fill all fields", fg="red")
        return
    salt, encrypted = encrypt_data(password, master_key)
    account = {
        "website": website,
        "name": username,
        "password": encrypted.decode(),
        "salt": base64.b64encode(salt).decode(),
        "created": datetime.datetime.now().isoformat()
    }
    current_accounts.append(account)
    save_accounts(current_accounts)
    refresh_table(current_accounts)
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    status_label.config(text="Saved", fg="green")

def open_manager(key):
    global master_key, tree, website_entry, username_entry, password_entry, status_label, current_accounts
    master_key = key
    login.destroy()

    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("700x600")

    current_accounts = load_accounts()

    top = tk.Frame(root)
    top.pack(pady=10)

    tk.Label(top, text="Website").grid(row=0, column=0)
    website_entry = tk.Entry(top, width=30)
    website_entry.grid(row=0, column=1)

    tk.Label(top, text="Username").grid(row=1, column=0)
    username_entry = tk.Entry(top, width=30)
    username_entry.grid(row=1, column=1)

    tk.Label(top, text="Password").grid(row=2, column=0)
    password_entry = tk.Entry(top, width=30)
    password_entry.grid(row=2, column=1)

    btns = tk.Frame(root)
    btns.pack(pady=10)

    tk.Button(btns, text="Generate Password", command=gui_generate_password, width=20).grid(row=0, column=0, padx=5)
    tk.Button(btns, text="Save", command=save_password, width=20).grid(row=0, column=1, padx=5)

    sort_btns = tk.Frame(root)
    sort_btns.pack(pady=5)

    tk.Button(sort_btns, text="Username A-Z", command=lambda: sort_and_refresh("a")).grid(row=0, column=0, padx=3)
    tk.Button(sort_btns, text="Username Z-A", command=lambda: sort_and_refresh("ar")).grid(row=0, column=1, padx=3)
    tk.Button(sort_btns, text="Website A-Z", command=lambda: sort_and_refresh("w")).grid(row=0, column=2, padx=3)
    tk.Button(sort_btns, text="Website Z-A", command=lambda: sort_and_refresh("wr")).grid(row=0, column=3, padx=3)

    status_label = tk.Label(root, text="")
    status_label.pack()

    table = tk.Frame(root)
    table.pack(pady=10)

    tree = ttk.Treeview(table, columns=("website", "username", "password"), show="headings", height=10)
    tree.heading("website", text="Website")
    tree.heading("username", text="Username")
    tree.heading("password", text="Password")
    tree.column("website", width=220)
    tree.column("username", width=220)
    tree.column("password", width=180)
    tree.pack()

    refresh_table(current_accounts)
    root.mainloop()

login = tk.Tk()
login.title("Login")
login.geometry("400x200")

tk.Label(login, text="Master Key").pack(pady=10)
key_entry = tk.Entry(login, show="*", width=30)
key_entry.pack()

msg = tk.Label(login, text="")
msg.pack()

def login_action():
    key = key_entry.get()
    if not os.path.exists(MASTER_FILE):
        try:
            validate_key(key)
            save_master_key(key)
            open_manager(key)
        except ValueError as e:
            msg.config(text=str(e))
    else:
        if verify_master_key(key):
            open_manager(key)
        else:
            msg.config(text="Invalid key")

tk.Button(login, text="Login", command=login_action).pack(pady=10)

login.mainloop()
