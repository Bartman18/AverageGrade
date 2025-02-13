import os.path

import pandas as pd
from pandastable import Table
import tkinter as tk
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

def show_table():
    df = pd.read_csv("srednia_wazona_sorted.csv")

    root = tk.Tk()
    root.title("Tabela wyników")

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

    root.mainloop()

def extract_year_and_type(semester):
    parts = semester.split()

    year_part = parts[-1]
    main_year = int(year_part.split("/")[0])

    season_weight = 0 if "zimowy" in semester else 1

    return (main_year, season_weight)

def calculate_weighted_average(path="pdf_output.csv", csv_output="srednia_wazona_sorted.csv"):

    data = pd.read_csv(path)

    df = pd.DataFrame(data)

    df["Ocena 1"] = df["Ocena 1"].str.replace(",", ".").astype(float)

    df["ECTS"] = pd.to_numeric(df["ECTS"], errors="coerce").fillna(0)


    df["Result"] = df["Ocena 1"] * df["ECTS"]



    grouped_df = df.groupby("Semestr", as_index = False)[["Result", "ECTS"]].sum()

    valid_ects = 30

    if (grouped_df["ECTS"] > valid_ects).any():
        invalid_semesters = grouped_df[grouped_df["ECTS"] > valid_ects][["Semestr", "ECTS"]]
        print(f"Check CSV for unnecessary ECTS values! The following semesters have more than 30 ECTS:\n{invalid_semesters}")
        grouped_df["Average"] = grouped_df["Result"] / grouped_df["ECTS"]


    if (grouped_df["ECTS"] < valid_ects).any():
        invalid_semesters = grouped_df[grouped_df["ECTS"] < valid_ects][["Semestr", "ECTS"]]
        print(f"Warning: Not all marks are included in the semester:\n{invalid_semesters}")


        grouped_df["Average"] = grouped_df.apply(
            lambda row: row["Result"] / row["ECTS"] if row["ECTS"] == valid_ects else 0,
            axis=1
        )

    else:
        grouped_df["Average"] = grouped_df["Result"] / grouped_df["ECTS"]

    grouped_df.to_csv("srednia_wazona.csv", index=False)


    sorted_data = pd.read_csv("srednia_wazona.csv")
    sorted_data["Sort_Key"] = sorted_data["Semestr"].apply(extract_year_and_type)
    sorted_data = sorted_data.sort_values(by="Sort_Key", ascending=True).drop(columns=["Sort_Key"])
    sorted_data.to_csv(csv_output, index=False)

    if(os.path.exists("srednia_wazona.csv")):
        os.remove("srednia_wazona.csv")

    filtred_df = sorted_data[sorted_data["ECTS"] == 30]

    if not filtred_df.empty:
        filtred_df.plot(x='Semestr', y='Average', kind='line')
        plt.xlabel('Semestr')
        plt.ylabel('Average')
        plt.title('Average Grade per Semestr')
        plt.xticks (ha="center", fontsize=8)
        plt.grid()
        plt.show()
    else:
        print("Invalid data")

    show_table()
