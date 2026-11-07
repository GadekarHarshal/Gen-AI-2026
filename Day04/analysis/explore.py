import pandas as pd

df = pd.read_json("data/records.json")

print("Total courses:", len(df))

print("\nFact 1: Number of institutes")
print(df["institute"].nunique())

print("\nFact 2: Most common institute")
print(df["institute"].value_counts().idxmax())

print("\nFact 3: Courses by discipline")
print(df["discipline"].value_counts())