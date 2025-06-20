import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from tqdm import tqdm  # for progress bar

load_dotenv()

# Read the data
data = pd.read_csv("Layoffs.csv")

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to convert a row to descriptive text (template)
def row_to_text(row):
    return (
        f"{row['Company']} headquartered in {row['Location HQ']} and "
        f"laid off {row['# Laid Off']} employees on {row['Date']} "
        f"in the {row['Industry']} industry."
    )

# Create a new column 'text_for_embedding' with descriptive text
data['text_for_embedding'] = data.apply(row_to_text, axis=1)

# Embed each row's text and store embeddings
embeddings = []
for text in tqdm(data['text_for_embedding']):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    embeddings.append(response.data[0].embedding)

# Add embeddings back to DataFrame
data['embedding'] = embeddings

# Save the DataFrame with embeddings to a file for later use
data.to_pickle("Layoffs_with_embeddings.pkl")

print("embeddings are done!!")


