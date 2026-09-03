import tkinter as tk 
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("1000x650")
my_frame = tk.Frame(root, bg="Green", bd= 2, relief="sunken")
my_frame.pack(fill="both", expand=True, padx=5, pady=5)
my_label = tk.Label(my_frame, text="Personal Expense Tracker", font=("Arial", 24, "bold"))
my_label.pack(pady=10)
root.mainloop()