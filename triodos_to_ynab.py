import csv

def str_to_float(s: str):
    return float(s.replace(".","").replace(",","."))

def read_csv(my_file):
    with open(my_file, 'r') as infile:
        reader = csv.DictReader(infile, fieldnames=["date","account","amount","debit_or_credit","counterparty_name","counterparty_iban","transaction_type","description","balance"])
        data = [row for row in reader]

    for record in data:
        record['amount'] = str_to_float(record['amount'])
        record['balance'] = str_to_float(record['balance'])

    return data

def main(mutations_file: str):
    pass

