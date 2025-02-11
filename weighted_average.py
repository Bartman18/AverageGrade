import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt


def extract_year_and_type(semester):
    parts = semester.split()

    year_part = parts[-1]
    main_year = int(year_part.split("/")[0])

    season_weight = 0 if "zimowy" in semester else 1

    return (main_year, season_weight)


path = "pdf_output.csv"

data = pd.read_csv(path)

df = pd.DataFrame(data)

df["Ocena 1"] = df["Ocena 1"].str.replace(",", ".").astype(float)

df["ECTS"] = pd.to_numeric(df["ECTS"], errors="coerce").fillna(0)


df["Result"] = df["Ocena 1"] * df["ECTS"]

# print(df[["Ocena 1", "ECTS", "Result"]])

grouped_df = df.groupby("Semestr", as_index = False)[["Result", "ECTS"]].sum()

valid_ects = 30


if (grouped_df["ECTS"] > valid_ects).any():
    raise ValueError("Check CSV for unnecessary ECTS values! Some values are greater than 30 ECTS." )


if (grouped_df["ECTS"] < valid_ects).any():
    print("Warning: Not all marks are included in the semester.")


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
sorted_data.to_csv("srednia_wazona_sorted.csv", index=False)


display(sorted_data)

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

