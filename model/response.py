import pandas as pd

# Load your CSV
df = pd.read_csv("C:/Users/ayo/Documents/NF/model/intent.csv")

# Create response dictionary
RESPONSES = dict(zip(df["text"], df["answer"]))

print(RESPONSES)
