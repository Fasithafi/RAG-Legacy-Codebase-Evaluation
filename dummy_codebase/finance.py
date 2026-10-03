def calculate_tax(amount, rate=0.05):
    if amount < 0:
        return 0
    return amount * rate

def process_invoice(invoice_id, amount):
    print(f"Processing invoice {invoice_id}")
    tax = calculate_tax(amount)
    total = amount + tax
    return total

class InvoiceManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.active_invoices = []

    def add_invoice(self, invoice):
        self.active_invoices.append(invoice)
        print("Invoice added to manager")

    def get_total_revenue(self):
        total = 0
        for inv in self.active_invoices:
            total += inv.amount
        return total
