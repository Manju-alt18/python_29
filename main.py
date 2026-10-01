import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


# ==========================================
# CREATE EXPENSE FILE
# ==========================================
def create_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=[
            "Date",
            "Category",
            "Description",
            "Amount",
            "Currency"
        ])

        df.to_csv(FILE_NAME, index=False)


# ==========================================
# LOAD EXPENSES
# ==========================================
def load_expenses():
    create_file()
    return pd.read_csv(FILE_NAME)


# ==========================================
# ADD EXPENSE
# ==========================================
def add_expense(category, description, amount, currency="INR"):

    create_file()

    try:
        amount = float(amount)

        if amount <= 0:
            return False, "Amount must be greater than 0."

    except ValueError:
        return False, "Invalid amount."

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_expense = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Description": [description],
        "Amount": [amount],
        "Currency": [currency]
    })

    df = load_expenses()

    df = pd.concat(
        [df, new_expense],
        ignore_index=True
    )

    df.to_csv(FILE_NAME, index=False)

    return True, "Expense added successfully."


# ==========================================
# DELETE EXPENSE
# ==========================================
def delete_expense(index):

    df = load_expenses()

    if df.empty:
        return False, "No expenses found."

    try:
        index = int(index)
    except ValueError:
        return False, "Invalid expense ID."

    if index < 0 or index >= len(df):
        return False, "Expense not found."

    df = df.drop(index)
    df = df.reset_index(drop=True)

    df.to_csv(FILE_NAME, index=False)

    return True, "Expense deleted successfully."


# ==========================================
# GET TOTAL EXPENSE
# ==========================================
def get_total():

    df = load_expenses()

    if df.empty:
        return 0

    return float(df["Amount"].sum())


# ==========================================
# GET CATEGORY SUMMARY
# ==========================================
def get_category_summary():

    df = load_expenses()

    if df.empty:
        return {}

    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return summary.to_dict()


# ==========================================
# GET MONTHLY SUMMARY
# ==========================================
def get_monthly_summary():

    df = load_expenses()

    if df.empty:
        return {}

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = (
        df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    summary = (
        df.groupby("Month")["Amount"]
        .sum()
    )

    return summary.to_dict()


# ==========================================
# GET DASHBOARD DATA
# ==========================================
def get_dashboard():

    df = load_expenses()

    if df.empty:

        return {
            "total": 0,
            "highest": 0,
            "average": 0,
            "transactions": 0,
            "top_category": "None"
        }

    total = float(df["Amount"].sum())

    highest = float(df["Amount"].max())

    average = float(df["Amount"].mean())

    transactions = len(df)

    top_category = (
        df.groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )

    return {
        "total": total,
        "highest": highest,
        "average": average,
        "transactions": transactions,
        "top_category": top_category
    }


# ==========================================
# CURRENCY EXCHANGE RATE
# ==========================================
def get_currency_rate(base, target):

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
            return None

        data = response.json()

        if "rates" not in data:
            return None

        return data["rates"].get(target)

    except requests.RequestException:

        return None


# ==========================================
# CATEGORY CHART
# ==========================================
def create_category_chart():

    df = load_expenses()

    if df.empty:
        return False

    summary = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))

    summary.plot(kind="bar")

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("category_chart.png")

    plt.close()

    return True


# ==========================================
# MONTHLY CHART
# ==========================================
def create_monthly_chart():

    df = load_expenses()

    if df.empty:
        return False

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = (
        df["Date"]
        .dt.to_period("M")
        .astype(str)
    )

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

    plt.savefig("monthly_chart.png")

    plt.close()

    return True


# ==========================================
# MAIN
# ==========================================
def main():

    create_file()

    print("Expense Tracker data system started.")

    print("CSV file:", FILE_NAME)

    print("Total expense:", get_total())


if __name__ == "__main__":
    main()