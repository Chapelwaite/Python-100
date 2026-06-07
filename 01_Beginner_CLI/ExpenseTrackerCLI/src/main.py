from pathlib import Path
from datetime import datetime
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPENSES_FILE = PROJECT_ROOT / "data" / "expenses.json"


def load_expenses():
    """
    Loads expenses from data/expenses.json.
    If the file does not exist, returns an empty list.
    """

    if not EXPENSES_FILE.exists():
        return []

    with open(EXPENSES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_expenses(expenses):
    """
    Saves expenses into data/expenses.json.
    """

    EXPENSES_FILE.parent.mkdir(exist_ok=True)

    with open(EXPENSES_FILE, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_next_id(expenses):
    """
    Creates the next ID for a new expense.
    """

    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1


def add_expense(expenses):
    """
    Adds a new expense.
    """

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than 0.")
        return

    category = input("Enter category: ").strip().lower()

    if not category:
        category = "other"

    note = input("Enter note or press Enter to skip: ").strip()

    date_input = input("Enter date YYYY-MM-DD or press Enter for today: ").strip()

    if date_input:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            expense_date = date_input
        except ValueError:
            print("Invalid date format.")
            return
    else:
        expense_date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "id": get_next_id(expenses),
        "amount": amount,
        "category": category,
        "note": note,
        "date": expense_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.")


def list_expenses(expenses):
    """
    Shows all expenses.
    """

    if not expenses:
        print("No expenses found.")
        return

    print("\n==============================")
    print(" ALL EXPENSES")
    print("==============================")

    for expense in expenses:
        print(f"\nID: {expense['id']}")
        print(f"Amount: {expense['amount']} GEL")
        print(f"Category: {expense['category']}")
        print(f"Note: {expense['note'] if expense['note'] else '-'}")
        print(f"Date: {expense['date']}")


def delete_expense(expenses):
    """
    Deletes an expense by ID.
    """

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense deleted.")
            return

    print("Expense not found.")


def show_total(expenses):
    """
    Shows total money spent.
    """

    total = sum(expense["amount"] for expense in expenses)

    print("\n==============================")
    print(" TOTAL SPENT")
    print("==============================")
    print(f"Total: {total:.2f} GEL")


def show_category_summary(expenses):
    """
    Shows how much money was spent in each category.
    """

    if not expenses:
        print("No expenses found.")
        return

    summary = {}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category not in summary:
            summary[category] = 0

        summary[category] += amount

    print("\n==============================")
    print(" CATEGORY SUMMARY")
    print("==============================")

    for category, total in summary.items():
        print(f"{category}: {total:.2f} GEL")


def show_month_summary(expenses):
    """
    Shows spending summary for selected month.
    Example month format: 2026-06
    """

    month = input("Enter month YYYY-MM: ").strip()

    if len(month) != 7:
        print("Invalid month format.")
        return

    monthly_expenses = [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]

    if not monthly_expenses:
        print("No expenses found for this month.")
        return

    total = sum(expense["amount"] for expense in monthly_expenses)

    print("\n==============================")
    print(f" MONTH SUMMARY: {month}")
    print("==============================")
    print(f"Expenses count: {len(monthly_expenses)}")
    print(f"Total spent: {total:.2f} GEL")

    print("\nExpenses:")
    for expense in monthly_expenses:
        print(f"- {expense['date']} | {expense['category']} | {expense['amount']} GEL | {expense['note']}")


def search_expenses(expenses):
    """
    Searches expenses by category or note.
    """

    keyword = input("Enter search keyword: ").strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    results = [
        expense for expense in expenses
        if keyword in expense["category"].lower()
        or keyword in expense["note"].lower()
    ]

    if not results:
        print("No matching expenses found.")
        return

    list_expenses(results)


def show_menu():
    """
    Prints the main menu.
    """

    print("\n==============================")
    print(" EXPENSE TRACKER CLI")
    print("==============================")
    print("1. Add expense")
    print("2. List expenses")
    print("3. Delete expense")
    print("4. Show total spent")
    print("5. Category summary")
    print("6. Month summary")
    print("7. Search expenses")
    print("8. Exit")


def main():
    """
    Program starts here.
    """

    expenses = load_expenses()

    while True:
        show_menu()

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            show_total(expenses)
        elif choice == "5":
            show_category_summary(expenses)
        elif choice == "6":
            show_month_summary(expenses)
        elif choice == "7":
            search_expenses(expenses)
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1-8.")


if __name__ == "__main__":
    main()