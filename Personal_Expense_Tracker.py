import tkinter as tk
import json 
expenses = []

def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

def load_expenses():
    global expenses

    try:
        with open("expenses.json", "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []

def add_expense():
    amount = amount_entry.get()
    try:
        amount = float(amount)
    except ValueError:
        print("Please enter a valid amount.")
        return
    if amount <= 0:
        print("Amount must be greater than 0.")
        return
    category = category_entry.get()
    if not category:
        print("Category cannot be empty.")
        return
    description = description_entry.get()
    date = date_entry.get()
    if not date:
        print("Date cannot be empty.")
        return

    expenses.append({
    "amount": amount,
    "category": category,
    "description": description,
    "date": date
})
    save_expenses()
    
    expense_label = tk.Label(
    expense_frame,
    text=f"{date} | {category} | {description} | Rs. {amount}",
    font=("Arial", 13),
    bg="White"
)
    expense_label.pack(anchor="w", padx=15, pady=8)

    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

    print(expenses)
    print("Amount:", amount)
    print("Category:", category)
    print("Description:", description)
    print("Date:", date)

load_expenses()
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1000x600")
my_frame = tk.Frame(root, bg="LightGray", bd=2, relief="sunken")
my_frame.pack(fill="both", expand=True, padx=5, pady=5)
my_label = tk.Label(
    my_frame,
    text="Personal Expense Tracker",
    font=("Arial", 24, "bold")
)
my_label.pack(pady=10)
inner_frame = tk.Frame(my_frame, bg="LightBlue", bd=2, relief="sunken")
inner_frame.pack(fill="both", expand=True, padx=20, pady=10)

expense_frame = tk.Frame(
    my_frame,
    bg="White",
    bd=2,
    relief="sunken"
)
expense_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Amount
amount_label = tk.Label(
    inner_frame,
    text="Amount:",
    font=("Arial", 14),
    bg="LightBlue"
)
amount_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
amount_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

# Category
category_label = tk.Label(
    inner_frame,
    text="Category:",
    font=("Arial", 14),
    bg="LightBlue"
)
category_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
category_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)
category_entry.grid(row=1, column=1, padx=10, pady=10)

# Description
description_label = tk.Label(
    inner_frame,
    text="Description:",
    font=("Arial", 14),
    bg="LightBlue"
)
description_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
description_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)
description_entry.grid(row=2, column=1, padx=10, pady=10)

# Date
date_label = tk.Label(
    inner_frame,
    text="Date:",
    font=("Arial", 14),
    bg="LightBlue"
)
date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

date_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)
date_entry.grid(row=3, column=1, padx=10, pady=10)

# Add Expense button
add_button = tk.Button(
    inner_frame,
    text="Add Expense",
    font=("Arial", 14, "bold"),
    command=add_expense,
)
add_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()
