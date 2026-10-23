import tkinter as tk
import json
from tkinter import ttk
from datetime import datetime
import csv
from tkinter import filedialog, messagebox

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
load_expenses()

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
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": date
        }

        expenses.append(expense)

        display_expense(expense)

    save_expenses()
    update_summary()
    update_budget_status()

def delete_expense(expense, expense_card):
    expenses.remove(expense)
    save_expenses()
    expense_card.destroy()
    update_summary()

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

def search_expenses():
    search_text = search_entry.get().lower()

    for widget in expense_frame.winfo_children():
        widget.destroy()

    for expense in expenses:
        if (
            search_text in expense["category"].lower()
            or search_text in expense["description"].lower()
            or search_text in expense["date"].lower()
        ):
            display_expense(expense)

def clear_search():
    search_entry.delete(0, tk.END)

    for widget in expense_frame.winfo_children():
        widget.destroy()

    for expense in expenses:
        display_expense(expense)

def calculate_monthly_expense(month, year):
    monthly_total = 0

    for expense in expenses:
        expense_date = datetime.strptime(
            expense["date"], "%d-%m-%Y"
        )

        if expense_date.month == month and expense_date.year == year:
            monthly_total += expense["amount"]

    return monthly_total

def show_monthly_chart():
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    monthly_totals = {}

    for expense in expenses:
        expense_date = datetime.strptime(
            expense["date"], "%d-%m-%Y"
        )

        month_year = expense_date.strftime("%b %Y")

        monthly_totals[month_year] = (
            monthly_totals.get(month_year, 0)
            + expense["amount"]
        )

    if not monthly_totals:
        print("No expenses available to display.")
        return

    sorted_months = sorted(
        monthly_totals,
        key=lambda month: datetime.strptime(month, "%b %Y")
    )

    totals = [monthly_totals[month] for month in sorted_months]

    # Create the chart
    fig, ax = plt.subplots(figsize=(11, 6))

    fig.patch.set_facecolor("#F4F7FB")
    ax.set_facecolor("#FFFFFF")

    bars = ax.bar(
        sorted_months,
        totals,
        color="#4285F4",
        width=0.55,
        edgecolor="none"
    )

    # Add expense amounts above each bar
    for bar, total in zip(bars, totals):
        ax.annotate(
            f"Rs. {total:,.0f}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#263238"
        )

    # Chart title and labels
    ax.set_title(
        "Monthly Expense Analysis",
        fontsize=18,
        fontweight="bold",
        color="#1F2937",
        pad=22
    )

    ax.set_xlabel(
        "Month",
        fontsize=11,
        color="#4B5563",
        labelpad=12
    )

    ax.set_ylabel(
        "Total Expenses (Rs.)",
        fontsize=11,
        color="#4B5563",
        labelpad=12
    )

    # Format the vertical axis
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda value, position: f"Rs. {value:,.0f}")
    )

    # Clean gridlines and borders
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#D1D5DB")

    ax.tick_params(axis="both", labelsize=10, colors="#4B5563")
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=0, pad=8)

    plt.xticks(rotation=30, ha="right")

    # Leave space for amounts above the bars
    maximum = max(totals)
    ax.set_ylim(0, maximum * 1.20 if maximum > 0 else 1)

    plt.tight_layout()
    plt.show()

def update_summary():
    total = sum(expense["amount"] for expense in expenses)
    count = len(expenses)
    average = total / count if count > 0 else 0

    if expenses:
        highest = max(expense["amount"] for expense in expenses)
    else:
        highest = 0

    total_label.config(
        text=f"Total Expenses\nRs. {total:.2f}"
    )
    count_label.config(
        text=f"Number of Expenses\n{count}"
    )
    highest_label.config(
        text=f"Highest Expense\nRs. {highest:.2f}"
    )
    average_label.config(
        text=f"Average Expense\nRS. {average:.2f}"
    )
    monthly_total = calculate_monthly_expense(10, 2026)

    monthly_label.config(
        text=f"October 2026 Expenses\nRs. {monthly_total:.2f}"
    )

def calculate_category_expenses():
    category_totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals

def show_category_analysis():
    category_totals = calculate_category_expenses()

    analysis_window = tk.Toplevel(root)
    analysis_window.title("Category-wise Expense Analysis")
    analysis_window.geometry("400x400")

    title_label = tk.Label(
        analysis_window,
        text="Category-wise Expenses",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=15)

    if not category_totals:
        tk.Label(
            analysis_window,
            text="No expenses available.",
            font=("Arial", 12)
        ).pack(pady=10)
        return

    for category, total in category_totals.items():
        tk.Label(
            analysis_window,
            text=f"{category}: Rs. {total:.2f}",
            font=("Arial", 13)
        ).pack(pady=5)

def export_expenses_to_csv():
    if not expenses:
        messagebox.showwarning(
            "No Expenses",
            "There are no expenses to export."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save Expense Report"
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["date", "category", "description", "amount"]
            )

            writer.writeheader()
            writer.writerows(expenses)

        messagebox.showinfo(
            "Export Successful",
            "Your expenses were exported successfully!"
        )

    except OSError as error:
        messagebox.showerror(
            "Export Failed",
            f"Could not save the file:\n{error}"
        )

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

summary_frame = tk.Frame(
    my_frame,
    bg="White",
    bd=2,
    relief="solid",
    width=250
)
summary_frame.pack(
    side="right",
    fill="both",
    padx=10,
    pady=10,
    expand=True
)

total_label = tk.Label(
    summary_frame,
    text="Total Expenses\nRs. 0",
    bg="White",
    font=("Arial", 14)
)
total_label.pack(
    padx=20,
    pady=5
)

count_label = tk.Label(
    summary_frame,
    text="Number of Expenses\n0",
    bg="White",
    font=("Arial", 14)
)
count_label.pack(
    padx=20,
    pady=8
)

highest_label = tk.Label(
    summary_frame,
    text="Highest Expense\nRs. 0.00",
    bg="White",
    font=("Arial", 14)
)
highest_label.pack(
    padx=20,
    pady=8
)

average_label = tk.Label(
    summary_frame,
    text="Average Expense\nRS. 0.00",
    bg="White",
    font=("Arial", 14)
)
average_label.pack(
    padx=20,
    pady=8
)

monthly_label = tk.Label(
    summary_frame,
    text="October 2026 Expenses\nRs. 0.00",
    bg="White",
    font=("Arial", 14)
)
monthly_label.pack(
    padx=20,
    pady=8
)

month_entry = tk.Entry(
    summary_frame,
    font=("Arial", 12),
    width=10
)
month_entry.pack(padx=20, pady=3)
month_entry.insert(0, "10")

year_entry = tk.Entry(
    summary_frame,
    font=("Arial", 12),
    width=10
)
year_entry.pack(padx=20, pady=3)
year_entry.insert(0, "2026")

def show_monthly_expenses():
    try:
        month = int(month_entry.get())
        year = int(year_entry.get())

        if month < 1 or month > 12:
            print("Month must be between 1 and 12.")
            return

        monthly_total = calculate_monthly_expense(month, year)

        monthly_label.config(
            text=f"{month:02d}/{year} Expenses\nRs. {monthly_total:.2f}"
        )

    except ValueError:
        print("Please enter a valid month and year.")

def calculate_remaining_budget(budget, month, year):
    monthly_total = calculate_monthly_expense(month, year)
    remaining = budget - monthly_total

    return remaining

def save_budget(budget):
    with open("budget.json", "w") as file:
        json.dump(budget, file)


def load_budget():
    try:
        with open("budget.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return 0

def set_monthly_budget():
    try:
        budget = float(budget_entry.get())

        if budget <= 0:
            messagebox.showwarning(
                "Invalid Budget",
                "Budget must be greater than 0."
            )
            return

        save_budget(budget)

        budget_entry.delete(0, tk.END)
        update_budget_status()

    except ValueError:
        messagebox.showwarning(
            "Invalid Input",
            "Please enter a valid budget amount."
        )


def update_budget_status():
    if "budget_status_label" not in globals():
        return

    budget = load_budget()

    if budget <= 0:
        budget_status_label.config(text="Budget not set")
        return

    today = datetime.today()
    spent = calculate_monthly_expense(today.month, today.year)
    remaining = budget - spent

    if remaining < 0:
        status = f"Budget exceeded by Rs. {abs(remaining):,.2f}"
    else:
        status = f"Remaining: Rs. {remaining:,.2f}"

    budget_status_label.config(
        text=(
            f"Monthly Budget: Rs. {budget:,.2f}\n"
            f"Spent: Rs. {spent:,.2f}\n"
            f"{status}"
        )
    )

    if remaining < 0:
        messagebox.showwarning(
            "Budget Exceeded",
            "Your expenses have exceeded the monthly budget!"
        )

def open_budget_window():
    global budget_entry, budget_status_label

    budget_window = tk.Toplevel(root)
    budget_window.title("Monthly Budget")
    budget_window.geometry("350x250")

    tk.Label(
        budget_window,
        text="Set Your Monthly Budget",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    budget_entry = tk.Entry(
        budget_window,
        font=("Arial", 12)
    )
    budget_entry.pack(pady=5)

    saved_budget = load_budget()
    if saved_budget > 0:
        budget_entry.insert(0, str(saved_budget))

    budget_status_label = tk.Label(
        budget_window,
        text="",
        font=("Arial", 11)
    )
    budget_status_label.pack(pady=5)
    update_budget_status()

    tk.Button(
        budget_window,
        text="Set Budget",
        command=set_monthly_budget
    ).pack(pady=10)

monthly_button = tk.Button(
    summary_frame,
    text="Calculate Monthly Expenses",
    command=show_monthly_expenses
)
monthly_button.pack(padx=20, pady=5)

export_button = tk.Button(
    summary_frame,
    text="Export to CSV",
    font=("Arial", 12),
    command=export_expenses_to_csv
)
export_button.pack(pady=5)

category_button = tk.Button(
    summary_frame,
    text="Category Analysis",
    font=("Arial", 12),
    command=show_category_analysis
)
category_button.pack(pady=5)

budget_window_button = tk.Button(
    summary_frame,
    text="Monthly Budget",
    font=("Arial", 12),
    command=open_budget_window
)
budget_window_button.pack(pady=5)

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

search_frame = tk.Frame(
    my_frame,
    bg="LightGray"
)
search_frame.pack(
    fill="x",
    padx=20,
    pady=5
)

search_entry = tk.Entry(
    search_frame,
    font=("Arial", 13)
)
search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

chart_button = tk.Button(
    summary_frame,
    text="Monthly Expense Chart",
    font=("Arial", 12),
    command=show_monthly_chart
)
chart_button.pack(pady=5)

search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_expenses
)
search_button.pack(
    side="left",
    padx=5
)

clear_button = tk.Button(
    search_frame,
    text="Clear",
    command=clear_search
)
clear_button.pack(
    side="left",
    padx=5
)

expense_container = tk.Frame(
    my_frame,
    bg="White",
    bd=2,
    relief="sunken"
)
expense_container.pack(
    side="left",
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

category_entry = ttk.Combobox(
    inner_frame,
    font=("Arial", 14),
    values=[
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Health",
        "Education",
        "Entertainment",
        "Other"
    ],
    state="readonly"
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