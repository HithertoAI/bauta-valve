import os
import sys
from system_a.generate_symbolic_blueprint import generate_symbolic_blueprint
from system_b.recomposer import recombine_from_blueprint
from system_c.validator_module import validate_output

from system_c.popeye import compute_florentine_score as florentine_score

def run_bauta_valve_pipeline(input_csv, blueprint_path, synthetic_output_path):
    print("Step 1: Generating symbolic blueprint...")
    generate_symbolic_blueprint(input_csv, blueprint_path)
    print(f"✓ Blueprint saved to {blueprint_path}")

    print("Step 2: Reconstructing synthetic data from blueprint...")
    recombine_from_blueprint(blueprint_path, synthetic_output_path)
    print(f"✓ Synthetic dataset saved to {synthetic_output_path}")

    print("Step 3: Validating synthetic data...")
    is_valid, diagnostics = validate_output(input_csv, synthetic_output_path)
    if not is_valid:
        print("✗ Validation failed. Diagnostics:")
        print(diagnostics)
        return

    print("✓ Validation passed.")

    print("Step 4: Running Popeye Florentine Score...")
    score = florentine_score(input_csv, synthetic_output_path)
    print(f"✓ Florentine Score: {score:.4f}")

    if score >= 0.9:
        print("✅ Synthetic dataset accepted for release.")
    else:
        print("⚠️ Score below threshold. Manual review recommended.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_pipeline.py <input_csv> <blueprint_output> <synthetic_output>")
        sys.exit(1)

    input_csv = sys.argv[1]
    blueprint_path = sys.argv[2]
    synthetic_output_path = sys.argv[3]

    run_bauta_valve_pipeline(input_csv, blueprint_path, synthetic_output_path)
