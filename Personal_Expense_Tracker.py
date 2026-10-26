import csv
import json
import os
import shutil
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, simpledialog, ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # folder this script lives in
EXPENSE_FILE = os.path.join(BASE_DIR, "expenses.json")   # your existing list of expenses
BUDGET_FILE = os.path.join(BASE_DIR, "budget.json")     # your existing budget (a number)
DATE_FMT = "%d-%m-%Y"
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health",
              "Entertainment", "Education", "Personal Item", "Office Item", "Other"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

# ---- Palette -------------------------------------------------------------
BG = "#F3F4F8"
CARD = "#FFFFFF"
HEADER = "#1E1B4B"
PRIMARY = "#4F46E5"
PRIMARY_DARK = "#4338CA"
SUCCESS = "#10B981"
DANGER = "#EF4444"
DANGER_DARK = "#DC2626"
TEXT = "#1F2937"
MUTED = "#6B7280"
BORDER = "#E5E7EB"
BAR_COLORS = ["#4F46E5", "#10B981", "#F59E0B", "#EF4444", "#06B6D4",
              "#8B5CF6", "#EC4899", "#84CC16", "#64748B"]
FONT = "Segoe UI"


def parse_date(s):
    try:
        return datetime.strptime(s, DATE_FMT)
    except (ValueError, TypeError):
        return None


class ExpenseTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Expense Tracker")
        self.geometry("1200x720")
        self.minsize(1050, 650)
        self.configure(bg=BG)

        self.expenses, self.budget = [], 0.0
        self.editing_id = None
        self.sort_col, self.sort_rev = "date", True
        self.load()

        self.setup_styles()
        self.build_header()
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=(16, 20))
        body.columnconfigure(0, weight=0, minsize=340)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self.build_form(body)
        self.build_main(body)
        self.refresh()
        if self.load_warning:
            self.after(300, lambda: messagebox.showwarning("Load problem", self.load_warning))

    # ------------------------------------------------------------ storage
    def load(self):
        self.load_warning = ""
        # expense.json is a plain list; ids are created in memory only
        if os.path.exists(EXPENSE_FILE):
            try:
                with open(EXPENSE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.expenses = [
                    dict(amount=float(e["amount"]), category=e["category"],
                         description=e.get("description", "").strip(),
                         date=e["date"], id=i + 1)
                    for i, e in enumerate(data)]
            except (json.JSONDecodeError, OSError, KeyError, ValueError, TypeError) as err:
                self.expenses = []
                try:
                    shutil.copy(EXPENSE_FILE, EXPENSE_FILE + ".bak")
                except OSError:
                    pass
                self.load_warning = (f"Could not read:\n{EXPENSE_FILE}\n\n{err}\n\n"
                                     "A backup copy was saved as expense.json.bak.")
        # budget.json holds just a number, e.g. 50000.0
        if os.path.exists(BUDGET_FILE):
            try:
                with open(BUDGET_FILE, "r", encoding="utf-8") as f:
                    self.budget = float(json.load(f))
            except (json.JSONDecodeError, OSError, ValueError, TypeError):
                pass

    def save(self):
        keys = ("amount", "category", "description", "date")
        with open(EXPENSE_FILE, "w", encoding="utf-8") as f:
            json.dump([{k: e[k] for k in keys} for e in self.expenses], f, indent=4)
        with open(BUDGET_FILE, "w", encoding="utf-8") as f:
            json.dump(self.budget, f)

    # ------------------------------------------------------------- styles
    def setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", font=(FONT, 10), background=CARD, foreground=TEXT)
        s.configure("TFrame", background=CARD)
        s.configure("TLabel", background=CARD, foreground=TEXT)
        s.configure("Muted.TLabel", foreground=MUTED, font=(FONT, 9))
        s.configure("TEntry", fieldbackground="#F9FAFB", bordercolor=BORDER,
                    lightcolor=BORDER, darkcolor=BORDER, padding=7)
        s.map("TEntry", bordercolor=[("focus", PRIMARY)], lightcolor=[("focus", PRIMARY)],
              darkcolor=[("focus", PRIMARY)])
        s.configure("TCombobox", fieldbackground="#F9FAFB", bordercolor=BORDER,
                    lightcolor=BORDER, darkcolor=BORDER, padding=6, arrowcolor=MUTED)
        s.map("TCombobox", fieldbackground=[("readonly", "#F9FAFB")])

        def button(name, bg, hover, fg="white"):
            s.configure(name, background=bg, foreground=fg, borderwidth=0,
                        focusthickness=0, padding=(14, 9), font=(FONT, 10, "bold"))
            s.map(name, background=[("active", hover)])

        button("Primary.TButton", PRIMARY, PRIMARY_DARK)
        button("Danger.TButton", DANGER, DANGER_DARK)
        button("Ghost.TButton", "#EEF2FF", "#E0E7FF", PRIMARY)
        button("Gray.TButton", "#F3F4F6", "#E5E7EB", TEXT)

        s.configure("Treeview", background=CARD, fieldbackground=CARD, rowheight=34,
                    borderwidth=0, font=(FONT, 10))
        s.configure("Treeview.Heading", background="#F9FAFB", foreground=MUTED,
                    font=(FONT, 9, "bold"), padding=8, borderwidth=0, relief="flat")
        s.map("Treeview", background=[("selected", "#E0E7FF")],
              foreground=[("selected", TEXT)])
        s.map("Treeview.Heading", background=[("active", "#F3F4F6")])
        for name, col in (("Green", SUCCESS), ("Red", DANGER)):
            s.configure(f"{name}.Horizontal.TProgressbar", background=col,
                        troughcolor="#E5E7EB", borderwidth=0, thickness=8)

    # ------------------------------------------------------------- layout
    def build_header(self):
        bar = tk.Frame(self, bg=HEADER)
        bar.pack(fill="x")
        tk.Label(bar, text="💰  Personal Expense Tracker", bg=HEADER, fg="white",
                 font=(FONT, 18, "bold")).pack(side="left", padx=24, pady=16)
        tk.Label(bar, text=datetime.now().strftime("%A, %d %B %Y"), bg=HEADER,
                 fg="#A5B4FC", font=(FONT, 10)).pack(side="right", padx=24)

    def card(self, parent):
        return tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)

    def build_form(self, parent):
        wrap = self.card(parent)
        wrap.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        inner = ttk.Frame(wrap, padding=22)
        inner.pack(fill="both", expand=True)

        self.form_title = ttk.Label(inner, text="Add New Expense", font=(FONT, 14, "bold"))
        self.form_title.pack(anchor="w", pady=(0, 16))

        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime(DATE_FMT))

        def field(label, widget):
            ttk.Label(inner, text=label, style="Muted.TLabel").pack(anchor="w", pady=(8, 3))
            widget.pack(fill="x")

        field("AMOUNT (Rs.)", ttk.Entry(inner, textvariable=self.amount_var))
        field("CATEGORY", ttk.Combobox(inner, textvariable=self.category_var,
                                       values=CATEGORIES, state="readonly"))
        field("DESCRIPTION", ttk.Entry(inner, textvariable=self.desc_var))
        field("DATE (DD-MM-YYYY)", ttk.Entry(inner, textvariable=self.date_var))

        self.submit_btn = ttk.Button(inner, text="＋  Add Expense", style="Primary.TButton",
                                     command=self.submit)
        self.submit_btn.pack(fill="x", pady=(24, 6))
        self.cancel_btn = ttk.Button(inner, text="Cancel Edit", style="Gray.TButton",
                                     command=self.reset_form)

    def build_main(self, parent):
        main = tk.Frame(parent, bg=BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        # --- stat cards
        stats = tk.Frame(main, bg=BG)
        stats.grid(row=0, column=0, sticky="ew")
        self.stat_vars = {}
        items = [("total", "Total Expenses", PRIMARY), ("count", "Transactions", "#06B6D4"),
                 ("high", "Highest Expense", DANGER), ("avg", "Average Expense", SUCCESS)]
        for i, (key, title, color) in enumerate(items):
            stats.columnconfigure(i, weight=1, uniform="s")
            c = self.card(stats)
            c.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 10, 0))
            tk.Frame(c, bg=color, height=4).pack(fill="x")
            tk.Label(c, text=title.upper(), bg=CARD, fg=MUTED,
                     font=(FONT, 8, "bold")).pack(anchor="w", padx=14, pady=(10, 0))
            v = tk.StringVar()
            tk.Label(c, textvariable=v, bg=CARD, fg=TEXT,
                     font=(FONT, 16, "bold")).pack(anchor="w", padx=14, pady=(0, 12))
            self.stat_vars[key] = v

        # --- monthly summary + budget
        mc = self.card(main)
        mc.grid(row=1, column=0, sticky="ew", pady=12)
        row = ttk.Frame(mc, padding=(16, 12))
        row.pack(fill="x")
        left = ttk.Frame(row)
        left.pack(side="left", fill="x", expand=True)
        self.month_title = ttk.Label(left, text="", style="Muted.TLabel")
        self.month_title.pack(anchor="w")
        self.month_total = ttk.Label(left, text="", font=(FONT, 15, "bold"))
        self.month_total.pack(anchor="w")
        self.budget_lbl = ttk.Label(left, text="", style="Muted.TLabel")
        self.budget_lbl.pack(anchor="w", pady=(2, 4))
        self.budget_bar = ttk.Progressbar(left, maximum=100, length=320,
                                          style="Green.Horizontal.TProgressbar")
        self.budget_bar.pack(anchor="w")

        right = ttk.Frame(row)
        right.pack(side="right")
        now = datetime.now()
        self.month_var = tk.StringVar(value=MONTHS[now.month - 1])
        self.year_var = tk.StringVar(value=str(now.year))
        mcb = ttk.Combobox(right, textvariable=self.month_var, values=MONTHS,
                           state="readonly", width=11)
        mcb.grid(row=0, column=0, padx=4)
        ycb = ttk.Spinbox(right, from_=2000, to=2100, textvariable=self.year_var, width=6,
                          command=self.refresh)
        ycb.grid(row=0, column=1, padx=4)
        mcb.bind("<<ComboboxSelected>>", lambda e: self.refresh())
        ycb.bind("<Return>", lambda e: self.refresh())
        ycb.bind("<FocusOut>", lambda e: self.refresh())

        # --- table card
        tc = self.card(main)
        tc.grid(row=2, column=0, sticky="nsew")
        tc.columnconfigure(0, weight=1)
        tc.rowconfigure(1, weight=1)

        top = ttk.Frame(tc, padding=(16, 14, 16, 8))
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="Expenses", font=(FONT, 13, "bold")).pack(side="left")
        ttk.Button(top, text="Clear", style="Gray.TButton",
                   command=lambda: self.search_var.set("")).pack(side="right")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh_table())
        ttk.Entry(top, textvariable=self.search_var, width=28).pack(side="right", padx=8)
        ttk.Label(top, text="🔍", font=(FONT, 11)).pack(side="right")

        cols = ("date", "category", "description", "amount")
        self.tree = ttk.Treeview(tc, columns=cols, show="headings", selectmode="browse")
        for c, t, w, a in (("date", "DATE", 110, "w"), ("category", "CATEGORY", 140, "w"),
                           ("description", "DESCRIPTION", 260, "w"),
                           ("amount", "AMOUNT", 110, "e")):
            self.tree.heading(c, text=t, anchor=a, command=lambda c=c: self.sort_by(c))
            self.tree.column(c, width=w, anchor=a, stretch=(c == "description"))
        self.tree.tag_configure("odd", background="#FAFAFB")
        sb = ttk.Scrollbar(tc, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(8, 0))
        sb.grid(row=1, column=1, sticky="ns")
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())
        self.tree.bind("<Delete>", lambda e: self.delete_selected())

        bottom = ttk.Frame(tc, padding=(12, 10))
        bottom.grid(row=2, column=0, columnspan=2, sticky="ew")
        ttk.Button(bottom, text="✏  Edit", style="Ghost.TButton",
                   command=self.edit_selected).pack(side="left", padx=4)
        ttk.Button(bottom, text="🗑  Delete", style="Danger.TButton",
                   command=self.delete_selected).pack(side="left", padx=4)
        for text, cmd in (("📈 Monthly Chart", self.show_monthly_chart),
                          ("📊 Category Analysis", self.show_category_analysis),
                          ("🎯 Monthly Budget", self.set_budget),
                          ("⬇ Export CSV", self.export_csv)):
            ttk.Button(bottom, text=text, style="Gray.TButton",
                       command=cmd).pack(side="right", padx=4)

    # ------------------------------------------------------------ actions
    def submit(self):
        try:
            amount = float(self.amount_var.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            return messagebox.showerror("Invalid amount", "Enter a positive number.")
        cat = self.category_var.get()
        if not cat:
            return messagebox.showerror("Missing category", "Please choose a category.")
        date = self.date_var.get().strip()
        if not parse_date(date):
            return messagebox.showerror("Invalid date", "Use the format DD-MM-YYYY.")
        desc = self.desc_var.get().strip()

        if self.editing_id is not None:
            for e in self.expenses:
                if e["id"] == self.editing_id:
                    e.update(amount=amount, category=cat, description=desc, date=date)
        else:
            nid = max((e["id"] for e in self.expenses), default=0) + 1
            self.expenses.append(dict(id=nid, amount=amount, category=cat,
                                      description=desc, date=date))
        self.save()
        self.reset_form()
        self.refresh()

    def reset_form(self):
        self.editing_id = None
        self.amount_var.set("")
        self.category_var.set("")
        self.desc_var.set("")
        self.date_var.set(datetime.now().strftime(DATE_FMT))
        self.form_title.config(text="Add New Expense")
        self.submit_btn.config(text="＋  Add Expense")
        self.cancel_btn.pack_forget()

    def selected_id(self):
        sel = self.tree.selection()
        return int(sel[0]) if sel else None

    def edit_selected(self):
        eid = self.selected_id()
        if eid is None:
            return messagebox.showinfo("Edit", "Select an expense first.")
        e = next(x for x in self.expenses if x["id"] == eid)
        self.editing_id = eid
        self.amount_var.set(e["amount"])
        self.category_var.set(e["category"])
        self.desc_var.set(e["description"])
        self.date_var.set(e["date"])
        self.form_title.config(text="Edit Expense")
        self.submit_btn.config(text="💾  Save Changes")
        self.cancel_btn.pack(fill="x")

    def delete_selected(self):
        eid = self.selected_id()
        if eid is None:
            return messagebox.showinfo("Delete", "Select an expense first.")
        if messagebox.askyesno("Delete", "Delete this expense?"):
            self.expenses = [e for e in self.expenses if e["id"] != eid]
            self.save()
            self.refresh()

    def set_budget(self):
        v = simpledialog.askfloat("Monthly Budget", "Set monthly budget (Rs.):",
                                  initialvalue=self.budget or None, minvalue=0, parent=self)
        if v is not None:
            self.budget = v
            self.save()
            self.refresh()

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV", "*.csv")],
                                            initialfile="expenses.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Date", "Category", "Description", "Amount"])
            for e in self.sorted_expenses():
                w.writerow([e["date"], e["category"], e["description"], e["amount"]])
        messagebox.showinfo("Exported", f"Saved to:\n{path}")

    # ------------------------------------------------------------ refresh
    def sorted_expenses(self):
        def key(e):
            if self.sort_col == "date":
                return parse_date(e["date"]) or datetime.min
            if self.sort_col == "amount":
                return e["amount"]
            return str(e[self.sort_col]).lower()
        return sorted(self.expenses, key=key, reverse=self.sort_rev)

    def sort_by(self, col):
        self.sort_rev = not self.sort_rev if self.sort_col == col else False
        self.sort_col = col
        self.refresh_table()

    def selected_month_year(self):
        try:
            return MONTHS.index(self.month_var.get()) + 1, int(self.year_var.get())
        except ValueError:
            n = datetime.now()
            return n.month, n.year

    def refresh(self):
        amounts = [e["amount"] for e in self.expenses]
        self.stat_vars["total"].set(f"Rs. {sum(amounts):,.0f}")
        self.stat_vars["count"].set(str(len(amounts)))
        self.stat_vars["high"].set(f"Rs. {max(amounts, default=0):,.0f}")
        self.stat_vars["avg"].set(f"Rs. {sum(amounts) / len(amounts) if amounts else 0:,.0f}")

        m, y = self.selected_month_year()
        month_sum = sum(e["amount"] for e in self.expenses
                        if (d := parse_date(e["date"])) and d.month == m and d.year == y)
        self.month_title.config(text=f"{MONTHS[m - 1].upper()} {y}")
        self.month_total.config(text=f"Rs. {month_sum:,.0f}")
        if self.budget > 0:
            pct = month_sum / self.budget * 100
            self.budget_lbl.config(
                text=f"{pct:.0f}% of Rs. {self.budget:,.0f} budget used"
                     f"  •  Rs. {max(self.budget - month_sum, 0):,.0f} left")
            self.budget_bar.config(value=min(pct, 100),
                                   style=("Red" if pct >= 90 else "Green")
                                         + ".Horizontal.TProgressbar")
        else:
            self.budget_lbl.config(text="No budget set — click “Monthly Budget”")
            self.budget_bar.config(value=0)
        self.refresh_table()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        q = self.search_var.get().strip().lower()
        i = 0
        for e in self.sorted_expenses():
            hay = f"{e['category']} {e['description']} {e['date']} {e['amount']}".lower()
            if q and q not in hay:
                continue
            self.tree.insert("", "end", iid=str(e["id"]),
                             values=(e["date"], e["category"], e["description"],
                                     f"Rs. {e['amount']:,.0f}"),
                             tags=("odd",) if i % 2 else ())
            i += 1

    # ------------------------------------------------------------- charts
    def popup(self, title, w, h):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg=CARD)
        win.geometry(f"{w}x{h}")
        win.transient(self)
        tk.Label(win, text=title, bg=CARD, fg=TEXT,
                 font=(FONT, 15, "bold")).pack(anchor="w", padx=24, pady=(20, 4))
        return win

    def show_category_analysis(self):
        totals = {}
        for e in self.expenses:
            totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
        win = self.popup("Category Analysis", 560, 420)
        if not totals:
            tk.Label(win, text="No expenses yet.", bg=CARD, fg=MUTED).pack(pady=40)
            return
        grand = sum(totals.values())
        frame = tk.Frame(win, bg=CARD)
        frame.pack(fill="both", expand=True, padx=24, pady=10)
        top = max(totals.values())
        for i, (cat, val) in enumerate(sorted(totals.items(), key=lambda x: -x[1])):
            r = tk.Frame(frame, bg=CARD)
            r.pack(fill="x", pady=6)
            tk.Label(r, text=cat, bg=CARD, fg=TEXT, width=14, anchor="w",
                     font=(FONT, 10)).pack(side="left")
            cv = tk.Canvas(r, width=250, height=16, bg="#F3F4F6", highlightthickness=0)
            cv.pack(side="left", padx=8)
            cv.create_rectangle(0, 0, 250 * val / top, 16, fill=BAR_COLORS[i % 9], width=0)
            tk.Label(r, text=f"Rs. {val:,.0f}  ({val / grand * 100:.0f}%)", bg=CARD,
                     fg=MUTED, font=(FONT, 9)).pack(side="left")

    def show_monthly_chart(self):
        m, year = self.selected_month_year()
        sums = [0.0] * 12
        for e in self.expenses:
            d = parse_date(e["date"])
            if d and d.year == year:
                sums[d.month - 1] += e["amount"]
        win = self.popup(f"Monthly Expenses — {year}", 720, 440)
        W, H, pad = 680, 320, 40
        cv = tk.Canvas(win, width=W, height=H, bg=CARD, highlightthickness=0)
        cv.pack(padx=20, pady=10)
        top = max(sums) or 1
        slot = (W - 2 * pad) / 12
        for i, v in enumerate(sums):
            x0 = pad + i * slot + 8
            x1 = pad + (i + 1) * slot - 8
            h = (H - 2 * pad) * v / top
            cv.create_rectangle(x0, H - pad - h, x1, H - pad, fill=PRIMARY if v else "#E5E7EB",
                                width=0)
            if v:
                cv.create_text((x0 + x1) / 2, H - pad - h - 10, text=f"{v:,.0f}",
                               font=(FONT, 8), fill=MUTED)
            cv.create_text((x0 + x1) / 2, H - pad + 16, text=MONTHS[i][:3],
                           font=(FONT, 9), fill=TEXT)
        cv.create_line(pad, H - pad, W - pad, H - pad, fill=BORDER)


if __name__ == "__main__":
    ExpenseTracker().mainloop()