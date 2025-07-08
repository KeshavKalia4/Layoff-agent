import pandas as pd
import os

class DataProcessor:
    def load_and_preprocess(self, data_path):
        embeddings_path = "backend/data/Layoffs_with_embeddings.pkl"
        if os.path.exists(embeddings_path):
            print("Loading precomputed embeddings...")
            data = pd.read_pickle(embeddings_path)
        else:
            raise FileNotFoundError(f"Embeddings file not found at {embeddings_path}! Please run the embedding process first.")
        # Always create the 'combined' column for downstream use
        if 'combined' not in data.columns:
            data['combined'] = data.apply(
                lambda row: f"{row['Company']} headquartered in {row['Location HQ']} and laid off {row['# Laid Off']} employees on {row['Date']} in the {row['Industry']} industry.",
                axis=1
            )
        return data


