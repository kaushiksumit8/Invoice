import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import session, Invoice, Item

class InvoiceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice System")
        self.items = []

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Date Label
        self.date_label = tk.Label(self.root, text=f"Invoice Date: {datetime.now().strftime('%Y-%m-%d')}")
        self.date_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Item Name
        self.name_label = tk.Label(self.root, text="Item Name")
        self.name_label.grid(row=1, column=0, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, pady=5)

        # Item Amount
        self.amount_label = tk.Label(self.root, text="Amount")
        self.amount_label.grid(row=2, column=0, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, pady=5)

        # Item Cost
        self.cost_label = tk.Label(self.root, text="Cost")
        self.cost_label.grid(row=3, column=0, pady=5)
        self.cost_entry = tk.Entry(self.root)
        self.cost_entry.grid(row=3, column=1, pady=5)

        # Add Item Button
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Invoice Text
        self.invoice_text = tk.Text(self.root, height=10, width=50)
        self.invoice_text.grid(row=5, column=0, columnspan=2, pady=10)

        # Save Invoice Button
        self.save_button = tk.Button(self.root, text="Save Invoice", command=self.save_invoice)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Search Functionality
        self.search_label = tk.Label(self.root, text="Search Invoice by Date (YYYY-MM-DD)")
        self.search_label.grid(row=7, column=0, pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=7, column=1, pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_invoice)
        self.search_button.grid(row=8, column=0, columnspan=2, pady=10)

    def add_item(self):
        name = self.name_entry.get()
        amount = self.amount_entry.get()
        cost = self.cost_entry.get()

        if not name or not amount or not cost:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount = int(amount)
            cost = float(cost)
        except ValueError:
            messagebox.showerror("Error", "Amount must be an integer and cost must be a float.")
            return

        item = Item(name=name, amount=amount, cost=cost)
        self.items.append(item)
        self.name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.update_invoice_text()

    def update_invoice_text(self):
        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert(tk.END, f"Invoice Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        self.invoice_text.insert(tk.END, "Items:\n")
        for item in self.items:
            self.invoice_text.insert(tk.END, f" - {item.name}: {item.amount} @ {item.cost:.2f} each, Total: {item.total_cost():.2f}\n")
        self.invoice_text.insert(tk.END, f"Total Amount: {self.total_amount()}\n")
        self.invoice_text.insert(tk.END, f"Total Cost: {self.total_cost():.2f}\n")

    def total_amount(self):
        return sum(item.amount for item in self.items)

    def total_cost(self):
        return sum(item.total_cost() for item in self.items)

    def save_invoice(self):
        new_invoice = Invoice(date=datetime.now())
        for item in self.items:
            item.invoice = new_invoice
            session.add(item)
        session.add(new_invoice)
        session.commit()
        messagebox.showinfo("Success", "Invoice saved successfully!")
        self.items.clear()
        self.update_invoice_text()

    def search_invoice(self):
        search_date = self.search_entry.get()
        try:
            search_date = datetime.strptime(search_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")
            return

        invoices = session.query(Invoice).filter(Invoice.date == search_date).all()
        if not invoices:
            messagebox.showinfo("No Results", "No invoices found for the given date.")
            return

        result_text = ""
        for invoice in invoices:
            result_text += f"Invoice Date: {invoice.date}\n"
            for item in invoice.items:
                result_text += f" - {item.name}: {item.amount} @ {item.cost:.2f} each, Total: {item.total_cost():.2f}\n"
            result_text += f"Total Amount: {sum(item.amount for item in invoice.items)}\n"
            result_text += f"Total Cost: {sum(item.total_cost() for item in invoice.items):.2f}\n\n"

        self.invoice_text.delete("1.0", tk.END)
        self.invoice_text.insert(tk.END, result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceSystem(root)
    root.mainloop()
