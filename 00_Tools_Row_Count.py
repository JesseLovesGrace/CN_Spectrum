import os
import csv

def count_total_rows(directory):
    total_rows = 0
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                total_rows += sum(1 for row in csv_reader)
    return total_rows


# Example usage
directory = r'C:\Users\jesse\Desktop\Master Thesis\01_Data\Spectrums\CN_Political_Spectrum\30_生育是自由_哪怕老龄化或人口膨胀(132216)\你会生孩子吗(112312)'
total_rows = count_total_rows(directory)
print("Total number of rows in all CSV files:", total_rows)
