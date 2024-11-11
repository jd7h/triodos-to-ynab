import csv
import datetime


def str_to_float(s: str):
    return float(s.replace(".", "").replace(",", "."))


def read_csv(my_file):
    with open(my_file, "r") as infile:
        reader = csv.DictReader(
            infile,
            fieldnames=[
                "transaction_date",
                "bank_account",
                "amount",
                "debit_or_credit",
                "counterparty_name",
                "counterparty_iban",
                "transaction_type",
                "description",
                "balance",
            ],
        )
        data = [row_to_record(row) for row in reader]
    return data


def row_to_record(row):
    row["amount"] = str_to_float(row["amount"])
    row["balance"] = str_to_float(row["balance"])
    row["transaction_date"] = datetime.datetime.strptime(
        row["transaction_date"], "%d-%m-%Y"
    ).strftime("%Y-%m-%d")
    if row["debit_or_credit"] == "Debet":
        row["amount"] *= -1
    return row


def record_to_YNAB(record):
    ynab_record = {
        "Date": record["transaction_date"],
        "Amount": record["amount"],
        "Payee": record.get("counterparty_name") or "unknown",
        "Memo": record.get("description"),
    }

    return ynab_record


def main(mutations_file: str):
    records = read_csv(mutations_file)

    bank_accounts = set([record["bank_account"] for record in records])
    for account in bank_accounts:
        print(f"Processing records for account {account}...")
        account_records = [r for r in records if r["bank_account"] == account]
        print(f"Found {len(account_records)} records for account {account}")
        min_date = min([r["transaction_date"] for r in account_records])
        max_date = max([r["transaction_date"] for r in account_records])
        outfilename = f"triodos_{account}_from_{min_date}_to_{max_date}_for_YNAB.csv"
        print(f"Writing {len(account_records)} records to file {outfilename}")

        with open(outfilename, "w", newline="") as csvfile:
            fieldnames = ["Date", "Payee", "Amount", "Memo"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows([record_to_YNAB(r) for r in account_records])
