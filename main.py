

import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"


# -----------------------------
# Create CSV file if not exists
# -----------------------------
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Description", "Amount"])


# -----------------------------
# Add Expense
# -----------------------------
def add_expense():
    print("\n========== ADD EXPENSE ==========")

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    while True:
        try:
            amount = float(input("Enter amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break

        except ValueError:
            print("Please enter a valid amount.")

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find next ID
    expenses = read_expenses()

    if expenses:
        new_id = int(expenses[-1]["ID"]) + 1
    else:
        new_id = 1

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            new_id,
            date,
            category,
            description,
            amount
        ])

    print("\nExpense added successfully!")


# -----------------------------
# Read Expenses
# -----------------------------
def read_expenses():
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


# -----------------------------
# View Expenses
# -----------------------------
def view_expenses():
    print("\n========== ALL EXPENSES ==========")

    expenses = read_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("-" * 80)
    print(
        f"{'ID':<5}"
        f"{'Date':<20}"
        f"{'Category':<15}"
        f"{'Description':<20}"
        f"{'Amount':>10}"
    )
    print("-" * 80)

    for expense in expenses:
        print(
            f"{expense['ID']:<5}"
            f"{expense['Date']:<20}"
            f"{expense['Category']:<15}"
            f"{expense['Description']:<20}"
            f"₹{float(expense['Amount']):>9.2f}"
        )

    print("-" * 80)


# -----------------------------
# Total Expenses
# -----------------------------
def total_expenses():
    print("\n========== TOTAL EXPENSE ==========")

    expenses = read_expenses()

    total = 0

    for expense in expenses:
        total += float(expense["Amount"])

    print(f"Total spent: ₹{total:.2f}")


# -----------------------------
# Category Summary
# -----------------------------
def category_summary():
    print("\n========== CATEGORY SUMMARY ==========")

    expenses = read_expenses()

    if not expenses:
        print("No expenses found.")
        return

    categories = {}

    for expense in expenses:
        category = expense["Category"]
        amount = float(expense["Amount"])

        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    print()

    for category, amount in categories.items():
        print(f"{category:<20} ₹{amount:.2f}")


# -----------------------------
# Monthly Summary
# -----------------------------
def monthly_summary():
    print("\n========== MONTHLY SUMMARY ==========")

    expenses = read_expenses()

    if not expenses:
        print("No expenses found.")
        return

    months = {}

    for expense in expenses:
        date = expense["Date"]
        month = date[:7]  # YYYY-MM

        amount = float(expense["Amount"])

        if month in months:
            months[month] += amount
        else:
            months[month] = amount

    for month, amount in months.items():
        print(f"{month}: ₹{amount:.2f}")


# -----------------------------
# Delete Expense
# -----------------------------
def delete_expense():
    print("\n========== DELETE EXPENSE ==========")

    expenses = read_expenses()

    if not expenses:
        print("No expenses found.")
        return

    try:
        delete_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    found = False
    new_expenses = []

    for expense in expenses:

        if int(expense["ID"]) == delete_id:
            found = True
        else:
            new_expenses.append(expense)

    if not found:
        print("Expense ID not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:

        fieldnames = [
            "ID",
            "Date",
            "Category",
            "Description",
            "Amount"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(new_expenses)

    print("Expense deleted successfully!")


# -----------------------------
# Main Menu
# -----------------------------
def main():

    create_file()

    while True:

        print("\n")
        print("===================================")
        print("        EXPENSE TRACKER")
        print("===================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Total Expenses")
        print("4. Category-wise Summary")
        print("5. Monthly Summary")
        print("6. Delete Expense")
        print("7. Exit")
        print("===================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            total_expenses()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please select 1-7.")


# -----------------------------
# Start Program
# -----------------------------
if __name__ == "__main__":
    main()
