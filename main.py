
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


# ==========================================
# CREATE FILE
# ==========================================
def create_file():

    if not os.path.exists(FILE_NAME):

        df = pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Description",
                "Amount",
                "Currency"
            ]
        )

        df.to_csv(FILE_NAME, index=False)


# ==========================================
# LOAD EXPENSES
# ==========================================
def load_expenses():

    create_file()

    df = pd.read_csv(FILE_NAME)

    return df


# ==========================================
# ADD EXPENSE
# ==========================================
def add_expense():

    print("\n========== ADD EXPENSE ==========")

    category = input("Enter category: ")
    description = input("Enter description: ")

    while True:

        try:

            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break

        except ValueError:
            print("Enter a valid number.")


    currency = input(
        "Enter currency (INR/USD/EUR etc.): "
    ).upper()

    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    new_expense = pd.DataFrame(
        {
            "Date": [date],
            "Category": [category],
            "Description": [description],
            "Amount": [amount],
            "Currency": [currency]
        }
    )


    df = load_expenses()

    df = pd.concat(
        [df, new_expense],
        ignore_index=True
    )

    df.to_csv(FILE_NAME, index=False)

    print("\nExpense added successfully!")


# ==========================================
# VIEW EXPENSES
# ==========================================
def view_expenses():

    print("\n========== ALL EXPENSES ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses found.")

        return


    print(df.to_string(index=True))

    print("\nTotal records:", len(df))


# ==========================================
# TOTAL EXPENSE
# ==========================================
def total_expense():

    print("\n========== TOTAL EXPENSE ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses found.")

        return


    total = df["Amount"].sum()

    print(f"Total Expense: ₹{total:.2f}")


# ==========================================
# CATEGORY SUMMARY
# ==========================================
def category_summary():

    print("\n========== CATEGORY SUMMARY ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses found.")

        return


    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


    print(summary)


# ==========================================
# MONTHLY SUMMARY
# ==========================================
def monthly_summary():

    print("\n========== MONTHLY SUMMARY ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses found.")

        return


    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.to_period("M")


    summary = (
        df.groupby("Month")["Amount"]
        .sum()
    )


    print(summary)


# ==========================================
# EXPENSE CHART
# ==========================================
def expense_chart():

    print("\n========== EXPENSE CHART ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses available for chart.")

        return


    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )


    plt.figure(figsize=(9, 5))

    summary.plot(
        kind="bar"
    )

    plt.title("Expenses by Category")

    plt.xlabel("Category")

    plt.ylabel("Amount")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ==========================================
# MONTHLY CHART
# ==========================================
def monthly_chart():

    print("\n========== MONTHLY EXPENSE CHART ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses available.")

        return


    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.to_period("M").astype(str)


    summary = (
        df.groupby("Month")["Amount"]
        .sum()
    )


    plt.figure(figsize=(9, 5))

    summary.plot(
        kind="line",
        marker="o"
    )

    plt.title("Monthly Expenses")

    plt.xlabel("Month")

    plt.ylabel("Amount")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ==========================================
# DELETE EXPENSE
# ==========================================
def delete_expense():

    print("\n========== DELETE EXPENSE ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses found.")

        return


    print(df.to_string())


    try:

        index = int(
            input("\nEnter row index to delete: ")
        )

    except ValueError:

        print("Invalid index.")

        return


    if index not in df.index:

        print("Index not found.")

        return


    df = df.drop(index)

    df = df.reset_index(drop=True)

    df.to_csv(FILE_NAME, index=False)

    print("Expense deleted successfully!")


# ==========================================
# CURRENCY API
# ==========================================
def currency_rate():

    print("\n========== CURRENCY EXCHANGE ==========")

    base = input(
        "Enter base currency (example: USD): "
    ).upper()

    target = input(
        "Enter target currency (example: INR): "
    ).upper()


    try:

        url = (
            "https://api.frankfurter.app/latest"
            f"?from={base}&to={target}"
        )


        response = requests.get(
            url,
            timeout=10
        )


        if response.status_code != 200:

            print("Unable to get exchange rate.")

            return


        data = response.json()


        if "rates" not in data:

            print("Invalid currency.")

            return


        rate = data["rates"][target]


        print(
            f"\n1 {base} = "
            f"{rate} {target}"
        )


    except requests.RequestException:

        print(
            "Internet connection/API error."
        )


# ==========================================
# DASHBOARD
# ==========================================
def dashboard():

    print("\n========== EXPENSE DASHBOARD ==========")

    df = load_expenses()

    if df.empty:

        print("No expenses recorded yet.")

        return


    total = df["Amount"].sum()

    highest = df["Amount"].max()

    average = df["Amount"].mean()

    category = (
        df.groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )


    print(f"Total Expenses   : ₹{total:.2f}")

    print(f"Highest Expense  : ₹{highest:.2f}")

    print(f"Average Expense  : ₹{average:.2f}")

    print(f"Top Category     : {category}")

    print(f"Total Transactions: {len(df)}")


# ==========================================
# MAIN MENU
# ==========================================
def main():

    create_file()


    while True:

        print("\n")
        print("==========================================")
        print("           EXPENSE TRACKER")
        print("==========================================")

        print("1. Add Expense")

        print("2. View Expenses")

        print("3. Total Expense")

        print("4. Category Summary")

        print("5. Monthly Summary")

        print("6. Category Chart")

        print("7. Monthly Chart")

        print("8. Delete Expense")

        print("9. Currency Exchange Rate")

        print("10. Dashboard")

        print("11. Exit")

        print("==========================================")


        choice = input(
            "Enter your choice: "
        )


        if choice == "1":

            add_expense()


        elif choice == "2":

            view_expenses()


        elif choice == "3":

            total_expense()


        elif choice == "4":

            category_summary()


        elif choice == "5":

            monthly_summary()


        elif choice == "6":

            expense_chart()


        elif choice == "7":

            monthly_chart()


        elif choice == "8":

            delete_expense()


        elif choice == "9":

            currency_rate()


        elif choice == "10":

            dashboard()


        elif choice == "11":

            print(
                "\nThank you for using Expense Tracker!"
            )

            break


        else:

            print(
                "\nInvalid choice. Enter 1-11."
            )


# ==========================================
# START PROGRAM
# ==========================================
if __name__ == "__main__":

    main()
