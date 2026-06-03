import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import mysql.connector


class BudgetTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Budget Tracker")
        self.master.geometry("700x600")
        self.master.configure(bg="skyblue")

        self.transaction_history = ""
        self.total_cash = 0

        # MySQL Connection
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="lekha",          # Change if needed
                password="Chandralekha@13",  # Change if needed
                database="budget"
            )

            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    timestamp DATETIME,
                    type VARCHAR(20),
                    amount DECIMAL(10,2),
                    reason VARCHAR(255)
                )
            """)

            self.conn.commit()

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Database Error",
                f"MySQL Connection Failed:\n{err}"
            )
            master.destroy()
            return

        # History Button
        self.history_button = tk.Button(
            master,
            text="History",
            command=self.show_database_history
        )
        self.history_button.place(x=20, y=20)

        # Amount
        tk.Label(
            master,
            text="Enter Amount:",
            bg="skyblue",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        self.amount_entry = tk.Entry(master, width=20, font=("Arial", 12))
        self.amount_entry.pack()

        # Reason
        tk.Label(
            master,
            text="Enter Reason:",
            bg="skyblue",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        self.notes_entry = tk.Entry(master, width=25, font=("Arial", 12))
        self.notes_entry.pack()

        # Buttons
        tk.Button(
            master,
            text="Cash In",
            width=12,
            command=self.cash_in
        ).pack(pady=10)

        tk.Button(
            master,
            text="Cash Out",
            width=12,
            command=self.cash_out
        ).pack(pady=10)

        # Transaction Area
        self.transaction_text = tk.Text(
            master,
            height=12,
            width=70,
            font=("Courier", 10)
        )
        self.transaction_text.pack(pady=20)

        # Balance Label
        self.present_amount_label = tk.Label(
            master,
            text="Present Amount: ₹0.00",
            bg="white",
            fg="green",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=10
        )
        self.present_amount_label.pack()

        self.load_history()

        self.master.protocol(
            "WM_DELETE_WINDOW",
            self.close_connection
        )

    def cash_in(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        reason = self.notes_entry.get()

        self.save_to_database(
            "Cash In",
            amount,
            reason
        )

        self.load_history()

        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

    def cash_out(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid amount")
            return

        reason = self.notes_entry.get()

        self.save_to_database(
            "Cash Out",
            amount,
            reason
        )

        self.load_history()

        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)

    def save_to_database(self, transaction_type, amount, reason):
        try:
            sql = """
                INSERT INTO transactions
                (timestamp, type, amount, reason)
                VALUES (%s, %s, %s, %s)
            """

            values = (
                datetime.now(),
                transaction_type,
                amount,
                reason
            )

            self.cursor.execute(sql, values)
            self.conn.commit()

            print("Saved Successfully")

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    def load_history(self):
        try:
            self.cursor.execute("""
                SELECT timestamp, type, amount, reason
                FROM transactions
                ORDER BY id
            """)

            records = self.cursor.fetchall()

            self.transaction_history = ""
            self.total_cash = 0

            for row in records:
                timestamp, ttype, amount, reason = row

                self.transaction_history += (
                    f"{timestamp} : "
                    f"{ttype} - Amount: ₹{amount:.2f} "
                    f"- Reason: {reason}\n"
                )

                if ttype == "Cash In":
                    self.total_cash += float(amount)
                else:
                    self.total_cash -= float(amount)

            self.update_transaction_text()

        except Exception as e:
            messagebox.showerror(
                "Load Error",
                str(e)
            )

    def update_transaction_text(self):
        self.transaction_text.config(state=tk.NORMAL)

        self.transaction_text.delete(
            "1.0",
            tk.END
        )

        self.transaction_text.insert(
            tk.END,
            self.transaction_history
        )

        self.transaction_text.config(state=tk.DISABLED)

        if self.total_cash <= 100:
            self.present_amount_label.config(
                fg="red",
                text=f"Present Amount: ₹{self.total_cash:.2f}"
            )
        else:
            self.present_amount_label.config(
                fg="green",
                text=f"Present Amount: ₹{self.total_cash:.2f}"
            )

    def show_database_history(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text Files", "*.txt")
                ]
            )

            if file_path:
                with open(
                    file_path,
                    "w",
                    encoding="utf-8"
                ) as file:
                    file.write(self.transaction_history)

                messagebox.showinfo(
                    "Success",
                    "History saved successfully!"
                )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()