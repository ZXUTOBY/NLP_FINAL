import pandas as pd

def take_first_n_lines(input_file_path, output_file_path, n=10000):
    """
    Reads the first n lines from a TSV file and writes them to a new file.
    
    Parameters:
        input_file_path (str): Path to the input TSV file.
        output_file_path (str): Path to save the output TSV file.
        n (int): Number of lines to take from the start. Default is 300.
    """
    try:
        # Read the input file, limiting to n rows
        data = pd.read_csv(input_file_path, sep='\t', nrows=n)
        
        # Save the first n rows to the output file
        data.to_csv(output_file_path, sep='\t', index=False)
        print(f"File successfully saved to {output_file_path}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Define file paths
    input_file_path = 'ALBERT.tsv'  # Replace with your file path
    output_file_path = 'ab_try.tsv'  # Replace with your desired output path

    # Specify the number of rows to extract
    n = 300

    # Call the function
    take_first_n_lines(input_file_path, output_file_path, n)

if __name__ == "__main__":
    main()

