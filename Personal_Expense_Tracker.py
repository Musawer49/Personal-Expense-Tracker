import tkinter as tk
import json

expenses = []
editing_expense = None

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

def display_expense(expense):
    expense_card = tk.Frame(
        expense_frame,
        bg="White",
        bd=1,
        relief="solid"
    )

    expense_card.pack(
        fill="x",
        padx=15,
        pady=8
    )

    expense_label = tk.Label(
        expense_card,
        text=(
            f"{expense['category']}: {expense['description']}\n"
            f"Rs: {expense['amount']}\n"
            f"Date: {expense['date']}"
        ),
        font=("Arial", 13),
        bg="White",
        anchor="w",
        justify="left"
    )

    expense_label.pack(
        fill="x",
        padx=15,
        pady=10
    )
    button_frame = tk.Frame(
    expense_card,
    bg="White"
    )

    button_frame.pack(
    padx=15,
    pady=5
    )


    edit_button = tk.Button(
    button_frame,
    text="Edit",
    command=lambda: edit_expense(expense, expense_card)
    )

    edit_button.pack(
    side="left",
    padx=5
    )


    delete_button = tk.Button(
    button_frame,
    text="Delete",
    command=lambda: delete_expense(expense, expense_card)
    )

    delete_button.pack(
    side="left",
    padx=5
    )

def add_expense():
    global editing_expense
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

    if editing_expense is not None:
        expense, expense_card = editing_expense

        expense["amount"] = amount
        expense["category"] = category
        expense["description"] = description
        expense["date"] = date
        expense_card.destroy()
        display_expense(expense)
        editing_expense = None
    else:
        expenses.append({
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
    })

    display_expense({
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    })

    save_expenses()

    display_expense({
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    })

    print(expenses)
    print("Amount:", amount)
    print("Category:", category)
    print("Description:", description)
    print("Date:", date)


def delete_expense(expense, expense_card):
    expenses.remove(expense)
    save_expenses()
    expense_card.destroy()

def edit_expense(expense, expense_card):
    global editing_expense

    editing_expense = (expense, expense_card)

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, expense["amount"])

    category_entry.delete(0, tk.END)
    category_entry.insert(0, expense["category"])

    description_entry.delete(0, tk.END)
    description_entry.insert(0, expense["description"])

    date_entry.delete(0, tk.END)
    date_entry.insert(0, expense["date"])

load_expenses()

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1000x600")

my_frame = tk.Frame(
    root,
    bg="LightGray",
    bd=2,
    relief="sunken"
)

my_frame.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)

my_label = tk.Label(
    my_frame,
    text="Personal Expense Tracker",
    font=("Arial", 24, "bold")
)

my_label.pack(pady=10)


inner_frame = tk.Frame(
    my_frame,
    bg="LightBlue",
    bd=2,
    relief="sunken"
)

inner_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


expense_container = tk.Frame(
    my_frame,
    bg="White",
    bd=2,
    relief="sunken"
)

expense_container.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

expense_canvas = tk.Canvas(
    expense_container,
    bg="White"
)

expense_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

expense_scrollbar = tk.Scrollbar(
    expense_container,
    orient="vertical",
    command=expense_canvas.yview
)

expense_scrollbar.pack(
    side="right",
    fill="y"
)

expense_canvas.configure(
    yscrollcommand=expense_scrollbar.set
)

expense_frame = tk.Frame(
    expense_canvas,
    bg="White"
)

expense_canvas.create_window(
    (0, 0),
    window=expense_frame,
    anchor="nw"
)

expense_frame.bind(
    "<Configure>",
    lambda event: expense_canvas.configure(
        scrollregion=expense_canvas.bbox("all")
    )
)


for expense in expenses:
    display_expense(expense)


# Amount
amount_label = tk.Label(
    inner_frame,
    text="Amount:",
    font=("Arial", 14),
    bg="LightBlue"
)

amount_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


amount_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)

amount_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Category
category_label = tk.Label(
    inner_frame,
    text="Category:",
    font=("Arial", 14),
    bg="LightBlue"
)

category_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


category_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)

category_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Description
description_label = tk.Label(
    inner_frame,
    text="Description:",
    font=("Arial", 14),
    bg="LightBlue"
)

description_label.grid(
    row=2,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


description_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)

description_entry.grid(
    row=2,
    column=1,
    padx=10,
    pady=10
)


# Date
date_label = tk.Label(
    inner_frame,
    text="Date:",
    font=("Arial", 14),
    bg="LightBlue"
)

date_label.grid(
    row=3,
    column=0,
    padx=10,
    pady=10,
    sticky="w"
)


date_entry = tk.Entry(
    inner_frame,
    font=("Arial", 14)
)

date_entry.grid(
    row=3,
    column=1,
    padx=10,
    pady=10
)


# Add Expense button
add_button = tk.Button(
    inner_frame,
    text="Add Expense",
    font=("Arial", 14, "bold"),
    command=add_expense
)

add_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)


root.mainloop()