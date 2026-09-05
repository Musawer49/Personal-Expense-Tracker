import tkinter as tk
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
    font=("Arial", 14, "bold")
)
add_button.grid(row=4, column=0, columnspan=2, pady=20)

root.mainloop()