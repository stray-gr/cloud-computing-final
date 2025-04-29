import csv

# Households
with open("400_households.csv", "r") as input_csv:
    with open("households.csv", "w") as output_csv:
        input_reader = csv.reader(input_csv)
        for row in input_reader:
            output_csv.write(','.join(map(lambda col: col.strip(), row)))
            output_csv.write('\n')

# Products
with open("400_products.csv", "r") as input_csv:
    with open("products.csv", "w") as output_csv:
        input_reader = csv.reader(input_csv)
        for row in input_reader:
            output_csv.write(','.join(map(lambda col: col.strip(), row)))
            output_csv.write('\n')

# Transactions
with open("400_transactions.csv", "r") as input_csv:
    with open("transactions.csv", "w") as output_csv:
        input_reader = csv.reader(input_csv)
        for row in input_reader:
            output_csv.write(','.join(map(lambda col: col.strip(), row)))
            output_csv.write('\n')
