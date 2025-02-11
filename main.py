import os
from pdf_reader import pdf_reader
from weighted_average import calculate_weighted_average

pdf_path = "C:/Users/User/PycharmProjects/pdf_Reader/Karta_przebiegu_studiów-273163-2025-02-10_15_51.pdf"
if not 'pdf_output.csv' in os.listdir():
    pdf_reader(pdf_path)
calculate_weighted_average()