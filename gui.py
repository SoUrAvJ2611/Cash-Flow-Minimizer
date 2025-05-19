import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cashflow_logic import CashFlowMinimizer  # Ensure this file exists

class CashFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Cash Flow Minimizer")
        self.root.geometry("1024x768")
        self.root.configure(bg="black")

        # Background Setup
        self.original_bg = Image.open("background.jpg")
        self.bg_label = tk.Label(self.root, bd=0, highlightthickness=0)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.bind("<Configure>", self.update_background)

        # Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 14, "bold"), padding=12,
                        foreground="white", background="white", borderwidth=0)
        style.map("TButton", background=[("active", "#cccccc")])
        style.configure("TLabel", font=("Segoe UI", 18), background="black", foreground="white")
        style.configure("TEntry", font=("Segoe UI", 18), foreground="white", fieldbackground="#333333")

        self.num_people = 0
        self.names = []
        self.name_entries = []
        self.transaction_entries = []

        self.setup_login()

    def update_background(self, event=None):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        resized = self.original_bg.resize((width, height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg_image)
        self.bg_label.image = self.bg_image

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

    def setup_login(self):
        self.clear_widgets()

        tk.Label(self.root, text="🔐 Login Page", font=("Segoe UI Semibold", 40),
                 bg="black", fg="white").place(relx=0.5, rely=0.2, anchor="center")

        frame = tk.Frame(self.root, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Enter your Email ID:", font=("Segoe UI", 20),
                 bg="black", fg="cyan").pack(pady=(0, 10))

        self.email_entry = ttk.Entry(frame, font=("Segoe UI", 20), width=30, justify="center")
        self.email_entry.pack(pady=(0, 30))  # More space below the entry

        tk.Button(self.root, text="Next ➡️", command=self.validate_email,
                  font=("Segoe UI", 14, "bold"), bg="black", fg="#66ff66",
                  activebackground="black", activeforeground="#66ff66", bd=0).place(relx=0.5, rely=0.65, anchor="center")

    def validate_email(self):
        email = self.email_entry.get().strip()
        if not email or "@" not in email or "." not in email:
            messagebox.showerror("Login Error", "Please enter a valid email address.")
            return
        self.setup_step1()

    def setup_step1(self):
        self.clear_widgets()
        tk.Label(self.root, text="💸 Cash Flow Minimizer",
                 font=("Segoe UI Semibold", 40),
                 bg="black", fg="white").place(relx=0.5, rely=0.2, anchor="center")

        frame = tk.Frame(self.root, bg="black")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Number of People:", font=("Segoe UI", 20),
                 bg="black", fg="cyan").pack(side="left", padx=15, pady=10)

        self.num_entry = ttk.Entry(frame, font=("Segoe UI", 20), width=8, justify="center")
        self.num_entry.pack(side="left", padx=15, pady=10)

        tk.Button(self.root, text="Next ➡️", command=self.setup_step2,
                  font=("Segoe UI", 14, "bold"), bg="black", fg="#66ff66",
                  activebackground="black", activeforeground="#66ff66", bd=0).place(relx=0.5, rely=0.65, anchor="center")

    def setup_step2(self):
        try:
            self.num_people = int(self.num_entry.get())
            if self.num_people < 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number (at least 2).")
            return

        self.clear_widgets()

        tk.Label(self.root, text="🧑‍🤝‍🧑 Enter Participant Names",
                 font=("Segoe UI Semibold", 32),
                 bg="black", fg="white").place(relx=0.5, rely=0.15, anchor="center")

        names_frame = tk.Frame(self.root, bg="black")
        names_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.name_entries = []
        for i in range(self.num_people):
            tk.Label(names_frame, text=f"Person {i+1}:", font=("Segoe UI", 18),
                     bg="black", fg="cyan").grid(row=i, column=0, padx=20, pady=15, sticky="e")

            entry = ttk.Entry(names_frame, font=("Segoe UI", 18), width=25)
            entry.grid(row=i, column=1, padx=20, pady=15)
            self.name_entries.append(entry)

        tk.Button(self.root, text="Next ➡️", command=self.setup_matrix,
                  font=("Segoe UI", 14, "bold"), bg="black", fg="#66ff66",
                  activebackground="black", activeforeground="#66ff66", bd=0).place(relx=0.5, rely=0.85, anchor="center")

    def setup_matrix(self):
        self.names = [entry.get().strip() for entry in self.name_entries]
        if not all(self.names) or len(set(self.names)) != len(self.names):
            messagebox.showerror("Input Error", "Please enter unique, non-empty names.")
            return

        self.clear_widgets()

        tk.Label(self.root, text="💰 Enter Transaction Amounts",
                 font=("Segoe UI Semibold", 28), bg="black", fg="white").pack(pady=30)

        matrix_frame = tk.Frame(self.root, bg="black")
        matrix_frame.pack()

        self.transaction_entries = []

        tk.Label(matrix_frame, text="From \\ To", font=("Segoe UI", 14, "bold"),
                 bg="black", fg="#90ee90").grid(row=0, column=0, padx=10, pady=10)

        for j in range(self.num_people):
            tk.Label(matrix_frame, text=self.names[j], font=("Segoe UI", 12),
                     bg="black", fg="cyan", width=12).grid(row=0, column=j+1, padx=5, pady=5)

        for i in range(self.num_people):
            tk.Label(matrix_frame, text=self.names[i], font=("Segoe UI", 12),
                     bg="black", fg="cyan", width=12).grid(row=i+1, column=0, padx=5, pady=5)

            row = []
            for j in range(self.num_people):
                if i == j:
                    tk.Label(matrix_frame, text="--", width=10, bg="black", fg="white").grid(row=i+1, column=j+1, padx=2, pady=2)
                    row.append(None)
                else:
                    entry = ttk.Entry(matrix_frame, width=10, font=("Segoe UI", 12), justify="center")
                    entry.insert(0, "0")
                    entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                    row.append(entry)
            self.transaction_entries.append(row)

        tk.Button(self.root, text="✨ Simplify Transactions ✨", command=self.process_transactions,
                  font=("Segoe UI", 14, "bold"), bg="black", fg="#66ff66",
                  activebackground="black", activeforeground="#66ff66", bd=0).pack(pady=40)

        self.output_box = tk.Text(self.root, width=95, height=12, font=("Consolas", 12),
                                  bg="#111111", fg="white", relief="sunken", bd=2)
        self.output_box.pack(pady=20)

    def process_transactions(self):
        matrix = []
        for i in range(self.num_people):
            row = []
            for j in range(self.num_people):
                if i == j:
                    row.append(0)
                else:
                    try:
                        value = float(self.transaction_entries[i][j].get())
                    except ValueError:
                        messagebox.showerror("Input Error", "Invalid transaction amount.")
                        return
                    row.append(value)
            matrix.append(row)

        backend = CashFlowMinimizer(self.names, matrix)
        result = backend.minimize()

        self.output_box.delete(1.0, tk.END)
        self.output_box.tag_configure("result", foreground="#ABF2FF")

        if result:
            self.output_box.insert(tk.END, "Simplified Transactions:\n\n", "result")
            for transaction in result:
                self.output_box.insert(tk.END, f"➡️ {transaction}\n", "result")
        else:
            self.output_box.insert(tk.END, "🎉 No transactions needed! Everyone is settled up.", "result")

if __name__ == "__main__":
    root = tk.Tk()
    app = CashFlowApp(root)
    root.mainloop()
