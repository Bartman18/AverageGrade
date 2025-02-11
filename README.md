# 📊 Weighted Average Calculator & Visualization from USOS PDF (PWr)

## 📌 Overview

This Python project calculates and visualizes the **weighted average grade** based on a **PDF file exported from USOS** (University Study System). It is specifically designed for **Wrocław University of Science and Technology (PWr)** but may work with similar formats from other universities.

## 🎯 How It Works

### 1️⃣ Export Your Grades from USOS

- Navigate to **USOS** > **Grades** > **Print Study Progress Card(in polish)**.
- Save the **PDF file** to your computer.

### 2️⃣ Set the Correct PDF Path in `main.py`

- Open `main.py` in a text editor.
- Locate the following line:
  ```python
  pdf_path = "your_pdf_path"  # Change this to your PDF file path
  ```
- Replace `"your_pdf_path"` with the **absolute path** to your **USOS PDF file**.

### 3️⃣ Install Dependencies

Ensure you have **Python 3.9+** installed. Then, install the required libraries:

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Script

- Execute the script using the command:
  ```bash
  python main.py
  ```
- The program will:
  - Extract **subjects, grades, and ECTS points** from the **PDF**.
  - Calculate the **weighted average grade** based on the **ECTS values**.
  - Generate a **CSV file** with results and a **visual chart**.

### 5️⃣ View Your Results
- It calculates the **weighted average grade** based on the **ECTS values**.
- It generates a **CSV file**, a **graph of weighted averages per semester**, and a **GUI table** displaying the results for better visualization.


## ⚠️ Known Issues

- The program currently **supports only PDFs in Polish**.
- The PDF reader might **misinterpret some data**, requiring **manual correction**.

## 🤝 Contributions

Contributions are welcome! If you'd like to improve the project:

1. Fork the repository.
2. Make your changes.
3. Submit a **pull request**.

## 📝 License

This project is licensed under the **MIT License**. Free to use and modify. Attribution is appreciated! 🚀

