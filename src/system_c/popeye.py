# system_c/popeye.py

import pandas as pd
import numpy as np

def compute_florentine_score(synthetic_df: pd.DataFrame, blueprint_df: pd.DataFrame) -> float:
    """
    Compute the Florentine Score based on structural and statistical alignment
    between synthetic and symbolic blueprint datasets.

    Returns a score between 0 and 1.
    """
    score_components = []

    for col in blueprint_df.columns:
        if col in synthetic_df.columns:
            if blueprint_df[col].dtype == object:
                # Compare distribution of unique values
                overlap = len(set(blueprint_df[col]) & set(synthetic_df[col])) / max(len(set(blueprint_df[col])), 1)
                score_components.append(overlap)
            else:
                # Compare means and std deviations
                blueprint_stats = blueprint_df[col].describe()
                synthetic_stats = synthetic_df[col].describe()
                mean_diff = abs(blueprint_stats['mean'] - synthetic_stats['mean']) / max(abs(blueprint_stats['mean']), 1)
                std_diff = abs(blueprint_stats['std'] - synthetic_stats['std']) / max(abs(blueprint_stats['std']), 1)
                score = 1 - (mean_diff + std_diff) / 2
                score_components.append(score)

    return round(np.mean(score_components), 3)

def popeye_final_check(synthetic_df: pd.DataFrame, blueprint_df: pd.DataFrame, threshold: float = 0.85) -> bool:
    """
    Final integrity check: returns True if Florentine Score passes threshold.
    """
    score = compute_florentine_score(synthetic_df, blueprint_df)
    print(f"🌀 Florentine Score: {score}")
    return score >= threshold
