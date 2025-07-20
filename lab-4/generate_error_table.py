#!/usr/bin/env python3
"""
Generate the commutation table for X errors with stabilizers.
This script calculates whether each X error commutes (0) or anti-commutes (1) 
with each stabilizer and outputs the result in markdown table format.
"""

import numpy as np

def pauli_commute(pauli1, pauli2):
    """
    Check if two Pauli strings commute.
    Returns True if they commute, False if they anti-commute.
    
    Two Pauli operators commute if the number of positions where they 
    have different non-identity operators is even.
    Commutation rules:
    - I commutes with everything
    - X anti-commutes with Z and Y
    - Y anti-commutes with X and Z  
    - Z anti-commutes with X and Y
    - Same operators (XX, YY, ZZ) commute
    """
    if len(pauli1) != len(pauli2):
        raise ValueError("Pauli strings must have same length")
    
    anti_commute_count = 0
    for p1, p2 in zip(pauli1, pauli2):
        # Count positions where operators anti-commute
        if (p1 == 'X' and p2 in ['Y', 'Z']) or \
           (p1 == 'Y' and p2 in ['X', 'Z']) or \
           (p1 == 'Z' and p2 in ['X', 'Y']):
            anti_commute_count += 1
    
    # If odd number of anti-commuting pairs, overall anti-commute
    return anti_commute_count % 2 == 0

def generate_syndrome_dictionary():
    """Generate syndrome dictionary mapping syndrome patterns to error types."""
    
    # Define stabilizers (7-qubit code)
    stabilizers = {
        'S5': 'ZIZIZIZ',
        'S4': 'IZZIIZZ', 
        'S3': 'IIIZZZZ',
        'S2': 'XIXIXIX',
        'S1': 'IXXIIXX',
        'S0': 'IIIXXXX'
    }
    
    syndrome_dict = {}
    
    # Helper function to get syndrome for an error
    def get_syndrome(error_string):
        syndrome = []
        for stab_name in ['S5', 'S4', 'S3', 'S2', 'S1', 'S0']:
            stab_string = stabilizers[stab_name]
            commutes = pauli_commute(error_string, stab_string)
            syndrome.append('0' if commutes else '1')
        return ''.join(syndrome)
    
    # Generate all single-qubit errors
    for i in range(7):
        # X errors
        error_string = ['I'] * 7
        error_string[6-i] = 'X'
        x_error = ''.join(error_string)
        syndrome = get_syndrome(x_error)
        syndrome_dict[syndrome] = f'X{i}'
        
        # Y errors
        error_string = ['I'] * 7
        error_string[6-i] = 'Y'
        y_error = ''.join(error_string)
        syndrome = get_syndrome(y_error)
        syndrome_dict[syndrome] = f'Y{i}'
        
        # Z errors
        error_string = ['I'] * 7
        error_string[6-i] = 'Z'
        z_error = ''.join(error_string)
        syndrome = get_syndrome(z_error)
        syndrome_dict[syndrome] = f'Z{i}'
    
    # Identity (no error)
    identity = 'IIIIIII'
    syndrome = get_syndrome(identity)
    syndrome_dict[syndrome] = 'I'
    
    return syndrome_dict

def generate_x_error_table():
    """Generate the commutation table for X errors with stabilizers."""
    
    # Define stabilizers (7-qubit code)
    stabilizers = {
        'S5': 'ZIZIZIZ',
        'S4': 'IZZIIZZ', 
        'S3': 'IIIZZZZ',
        'S2': 'XIXIXIX',
        'S1': 'IXXIIXX',
        'S0': 'IIIXXXX'
    }
    
    # Generate X errors for each qubit (0 to 6)
    # Convention: qubit 0 is rightmost, qubit 6 is leftmost
    x_errors = {}
    for i in range(7):
        error_string = ['I'] * 7
        error_string[6-i] = 'X'  # Qubit 0 is at position 6, qubit 6 is at position 0
        x_errors[f'X_{i}'] = ''.join(error_string)
    
    # Create the table header - exactly as requested
    print("| Error Code | Error Pauli String | S5(ZIZIZIZ) | S4(IZZIIZZ) | S3 (IIIZZZZ) | S2 (XIXIXIX) | S1 (IXXIIXX) | S0 (IIIXXXX) |")
    print("|---|---|---|---|---|---|---|---|")
    
    # Calculate commutation for each error with each stabilizer
    for error_name, error_string in x_errors.items():
        # Build the row exactly as in the format
        row_parts = [f"${error_name}$", error_string]
        
        # Check commutation with each stabilizer
        for stab_name in ['S5', 'S4', 'S3', 'S2', 'S1', 'S0']:
            stab_string = stabilizers[stab_name]
            commutes = pauli_commute(error_string, stab_string)
            
            if commutes:
                row_parts.append("0 (commute)")
            else:
                row_parts.append("1 (anti-commute)")
        
        # Join with proper spacing
        print("| " + " | ".join(row_parts) + " |")

if __name__ == "__main__":
    # Generate and print the X error table
    generate_x_error_table()
    
    print("\n" + "="*50)
    print("SYNDROME DICTIONARY")
    print("="*50)
    
    # Generate and print the syndrome dictionary
    syndrome_dict = generate_syndrome_dictionary()
    
    # Sort by syndrome pattern for cleaner output
    sorted_syndromes = sorted(syndrome_dict.items())
    
    print("{")
    for i, (syndrome, error) in enumerate(sorted_syndromes):
        comma = "," if i < len(sorted_syndromes) - 1 else ""
        print(f"    '{syndrome}': '{error}'{comma}")
    print("}")
