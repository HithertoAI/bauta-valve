# generate_symbolic_blueprint.py

"""
System A — Interpreter/Symbolizer
Reads original dataset and generates abstract symbolic blueprint
for privacy-safe synthetic generation.
"""

import pandas as pd
import hashlib
import json
from pathlib import Path

def load_data(file_path):
    return pd.read_csv(file_path)

def hash_column(column_data):
    return hashlib.sha256(column_data.encode('utf-8')).hexdigest()

def generate_symbolic_blueprint(df):
    blueprint = {
        "columns": {},
        "structure": {
            "num_rows": df.shape[0],
            "num_columns": df.shape[1]
        }
    }
    for col in df.columns:
        col_type = str(df[col].dtype)
        sample_values = df[col].dropna().unique()[:5].tolist()
        blueprint["columns"][col] = {
            "type": col_type,
            "sample_hashes": [hash_column(str(val)) for val in sample_values]
        }
    return blueprint

def save_blueprint(blueprint, output_path):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(blueprint, f, indent=2)

# Example usage:
if __name__ == "__main__":
    df = load_data("data/flat-training.csv")
    blueprint = generate_symbolic_blueprint(df)
    save_blueprint(blueprint, "system_c/intermediate/blueprint_flat.json")
