import os
import argparse
import pandas as pd

def get_runtime_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-input-path', type=str)
    parser.add_argument('--data-output-path', type=str)
    args = parser.parse_args()
    return args

def main():
    args = get_runtime_args()

    # Create output dir
    os.makedirs(args.data_output_path, exist_ok=True)

    input_file_path = os.path.join(args.data_input_path, 'german_credit_data.csv')
    output_file_path = os.path.join(args.data_output_path, 'german_credit_data.csv')

    print(f'Reading data from {input_file_path} and writing processed output to {output_file_path}')
    print(f'Output dir: {os.listdir(args.data_output_path)}')
    # Read input data
    credit_data_df = pd.read_csv(input_file_path)

    # Some data preprocessing should happen here...

    # Write output data
    credit_data_df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    main()