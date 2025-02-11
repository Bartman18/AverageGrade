import os
from pdf_reader import pdf_reader
from weighted_average import calculate_weighted_average

pdf_path = "your_pdf_path"
if not 'pdf_output.csv' in os.listdir():
    pdf_reader(pdf_path)
calculate_weighted_average()
