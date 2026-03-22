import tkinter as tk
from tkinter import ttk
import random
import string


# --------------------------------------------------------
# Generate random password
# --------------------------------------------------------
def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%&?"
    password = "".join(random.choice(chars) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# --------------------------------------------------------
# Save password into the table
# --------------------------------------------------------
def save_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if website == "" or username == "" or password == "":
        status_label.config(text="⚠ Please fill all fields", fg="#ff5757")
        return

    tree.insert("", tk.END, values=(website, username, password))

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    status_label.config(text="✔ Saved successfully!", fg="#4CAF50")


# --------------------------------------------------------
# Hover effect for buttons
# --------------------------------------------------------
def on_enter(e):
    e.widget["background"] = "#3c8dbc"

def on_leave(e):
    e.widget["background"] = "#2c7abf"


# --------------------------------------------------------
# Main window
# --------------------------------------------------------
root = tk.Tk()
root.title("Password Manager")
root.geometry("600x520")
root.config(bg="#f2f2f2")
root.resizable(False, False)

title_label = tk.Label(root, text="Sin's Keylink", font=("Arial", 20, "bold"), bg="#f2f2f2", fg="#2c7abf")
title_label.pack(pady=13)


# --------------------------------------------------------
# Style for input frame
# --------------------------------------------------------
input_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
input_frame.pack(pady=10, padx=20, fill="x")

label_font = ("Arial", 12)
entry_font = ("Arial", 12)

# Website
tk.Label(input_frame, text="Website:", bg="#ffffff", font=label_font).grid(row=0, column=0, sticky="e", pady=8, padx=10)
website_entry = tk.Entry(input_frame, font=entry_font, width=30)
website_entry.grid(row=0, column=1, padx=10, pady=8)

# Username
tk.Label(input_frame, text="Username:", bg="#ffffff", font=label_font).grid(row=1, column=0, sticky="e", pady=8, padx=10)
username_entry = tk.Entry(input_frame, font=entry_font, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=8)

# Password
tk.Label(input_frame, text="Password:", bg="#ffffff", font=label_font).grid(row=2, column=0, sticky="e", pady=8, padx=10)
password_entry = tk.Entry(input_frame, font=entry_font, width=30)
password_entry.grid(row=2, column=1, padx=10, pady=8)


# --------------------------------------------------------
# Buttons
# --------------------------------------------------------
btn_style = {
    "font": ("Arial", 10, "bold"),
    "bg": "#2c7abf",
    "fg": "white",
    "activebackground": "#1b5c99",
    "activeforeground": "white",
    "bd": 0,
    "width": 18,
    "height": 1,
    "cursor": "hand2"
}

generate_btn = tk.Button(input_frame, text="Generate Password", command=generate_password, **btn_style)
generate_btn.grid(row=3, column=0, pady=15, padx=10)

save_btn = tk.Button(input_frame, text="Save", command=save_password, **btn_style)
save_btn.grid(row=3, column=1, pady=15, padx=10)

generate_btn.bind("<Enter>", on_enter)
generate_btn.bind("<Leave>", on_leave)
save_btn.bind("<Enter>", on_enter)
save_btn.bind("<Leave>", on_leave)


# --------------------------------------------------------
# Status Label
# --------------------------------------------------------
status_label = tk.Label(root, text="", font=("Arial", 12), bg="#f2f2f2")
status_label.pack()


# --------------------------------------------------------
# Saved passwords table
# --------------------------------------------------------
table_frame = tk.Frame(root, bg="#f2f2f2")
table_frame.pack(pady=10)

columns = ("website", "username", "password")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

# Column headings
tree.heading("website", text="Website")
tree.heading("username", text="Username")
tree.heading("password", text="Password")

# Column widths
tree.column("website", width=200)
tree.column("username", width=200)
tree.column("password", width=180)

tree.pack()

# Add style
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=30,
                fieldbackground="white")
style.configure("Treeview.Heading",
                font=("Arial", 12, "bold"),
                background="#2c7abf",
                foreground="white")
style.map("Treeview", background=[("selected", "#3c8dbc")])


# --------------------------------------------------------
# Run the app
# --------------------------------------------------------
root.mainloop()