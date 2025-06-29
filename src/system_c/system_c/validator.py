# system_c/validator.py

"""
System C: Validation Module for Synthetic Data Fidelity
- Compares original and generated data for statistical alignment.
- Routes validation failures back to System A or B for targeted repair.
- Optionally applies local patching if repair is minor and authorized.
"""

import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np

def validate_output(original_df, synthetic_df, threshold=0.05):
    """
    Validates the statistical similarity of synthetic data to the original.
    Returns a diagnostic report and validation status.
    """
    report = {}
    for column in original_df.columns:
        if column not in synthetic_df.columns:
            report[column] = 'Missing in synthetic'
            continue

        orig = original_df[column].dropna()
        synth = synthetic_df[column].dropna()

        if orig.dtype != synth.dtype:
            report[column] = 'Type mismatch'
            continue

        if np.issubdtype(orig.dtype, np.number):
            mse = mean_squared_error(orig, synth)
            report[column] = f'MSE: {mse:.4f}'
            if mse > threshold:
                report[column] += ' (Too divergent)'
        else:
            match = (orig == synth).mean()
            report[column] = f'Match rate: {match:.2%}'
            if match < (1 - threshold):
                report[column] += ' (Too divergent)'

    passed = all('Too divergent' not in v and 'Missing' not in v and 'Type mismatch' not in v for v in report.values())
    return {'passed': passed, 'details': report}

# Placeholder for repair signaling
def signal_repair(source, issues):
    print(f"Signaling {source} to revise based on issues: {issues}")
