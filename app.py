
from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

FILE_NAME = "expenses.csv"


# -----------------------------------
# Create CSV if it doesn't exist
# -----------------------------------
def create_file():

    if not os.path.exists(FILE_NAME):

        df = pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Description",
                "Amount"
            ]
        )

        df.to_csv(FILE_NAME, index=False)


# -----------------------------------
# Home Page
# -----------------------------------
@app.route("/")
def home():

    create_file()

    df = pd.read_csv(FILE_NAME)

    total = df["Amount"].sum() if not df.empty else 0

    return render_template(
        "index.html",
        expenses=df.to_dict("records"),
        total=total
    )


# -----------------------------------
# Add Expense
# -----------------------------------
@app.route("/add", methods=["POST"])
def add_expense():

    create_file()

    category = request.form["category"]
    description = request.form["description"]
    amount = float(request.form["amount"])

    date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    new_expense = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Description": [description],
        "Amount": [amount]
    })

    df = pd.read_csv(FILE_NAME)

    df = pd.concat(
        [df, new_expense],
        ignore_index=True
    )

    df.to_csv(FILE_NAME, index=False)

    return redirect("/")


# -----------------------------------
# Delete Expense
# -----------------------------------
@app.route("/delete/<int:index>")
def delete_expense(index):

    df = pd.read_csv(FILE_NAME)

    if index >= 0 and index < len(df):

        df = df.drop(index)

        df = df.reset_index(drop=True)

        df.to_csv(FILE_NAME, index=False)

    return redirect("/")


# -----------------------------------
# Expense Summary API
# -----------------------------------
@app.route("/api/summary")
def summary():

    df = pd.read_csv(FILE_NAME)

    if df.empty:

        return jsonify({
            "total": 0,
            "categories": {}
        })

    total = float(df["Amount"].sum())

    categories = (
        df.groupby("Category")["Amount"]
        .sum()
        .to_dict()
    )

    return jsonify({
        "total": total,
        "categories": categories
    })


# -----------------------------------
# Run Flask
# -----------------------------------
if __name__ == "__main__":

    create_file()

    app.run(
        debug=True
    )
