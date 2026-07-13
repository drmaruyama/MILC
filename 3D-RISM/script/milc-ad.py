import sys

# Define coefficient sets
coeff_sets = {
    "Standard": {
        "ad" : [0.31305262, 0.0],
        "euv": [0.53900435, 0.44943914],
    },
}

def main():
    # Check command-line arguments (expecting 1 argument: base filename)
    if len(sys.argv) != 2:
        print("Usage: python milc-ad.py <base_filename>", file=sys.stderr)
        sys.exit(1)

    # Get the base filename and auto-complete extensions
    base_name = sys.argv[1]
    ad_file = f"{base_name}.ad"
    euv_file = f"{base_name}.euv"

    ad_results = []
    euv_results = []

    # Process the second file (.ad)
    try:
        with open(ad_file, 'r') as f1:
            for line_num, line in enumerate(f1, start=1):
                if not line.strip():
                    continue
                
                values = [float(x) for x in line.split()]
                
                if len(values) != 2:
                    print(f"Error: Number of data points in {ad_file} at line {line_num} is not exactly 2.", file=sys.stderr)
                    sys.exit(1)
                    
                ad_results.append(values)
                
    except FileNotFoundError:
        print(f"Error: File '{ad_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Process the first file (.euv)
    try:
        with open(euv_file, 'r') as f2:
            for line_num, line in enumerate(f2, start=1):
                if not line.strip():
                    continue
                
                values = [float(x) for x in line.split()]
                n = len(values)
                
                # Check for even number of columns
                if n % 2 != 0:
                    print(f"Error: Number of data points in {euv_file} at line {line_num} is not even (current count: {n}).", file=sys.stderr)
                    sys.exit(1)
                
                half_index = n // 2
                sum_first_half = sum(values[:half_index])
                sum_second_half = sum(values[half_index:])
                
                euv_results.append((sum_first_half, sum_second_half))

    except FileNotFoundError:
        print(f"Error: File '{euv_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Compare line counts
    if len(euv_results) != len(ad_results):
        print(f"Error: Line counts do not match. ({euv_file}: {len(euv_results)} lines, {ad_file}: {len(ad_results)} lines)", file=sys.stderr)
        sys.exit(1)

    # ---------------------------------------------------------
    # Calculation and Output
    # ---------------------------------------------------------
    # Get coefficients for the "Standard" set
    coeffs = coeff_sets["Standard"]
    coeff_ad1, coeff_ad2 = coeffs["ad"]
    coeff_euv1, coeff_euv2 = coeffs["euv"]

    # Calculate and print the final value for each line
    for i in range(len(euv_results)):
        a_val1, a_val2 = ad_results[i]
        e_val1, e_val2 = euv_results[i]
        
        # Multiply corresponding values by their coefficients and sum them up
        final_value = (a_val1 * coeff_ad1) + (a_val2 * coeff_ad2) + \
            (e_val1 * coeff_euv1) + (e_val2 * coeff_euv2)
        
        # Print the final value (Scientific notation, 15 decimal places)
        print(f"{final_value:.15e}")

if __name__ == "__main__":
    main()
