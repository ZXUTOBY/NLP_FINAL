import pandas as pd

'''
def process_and_save_file(input_file, output_file):
    """
    Process the input file to filter and deduplicate predictions, saving the results as a TSV file.
    :param input_file: Path to the input TSV file.
    :param output_file: Path to save the processed TSV file.
    """
    # Load the input file
    data = pd.read_csv(input_file, sep='\t')
    
    # Filter rows where predicted is 'A'
    filtered_data = data[data['predicted'] == 'A']
    
    # Group by textid and deduplicate based on wordpos
    result = (
        filtered_data.groupby('textid')
        .apply(lambda group: group.sort_values('wordpos')  # Sort by wordpos for consistency
                             .drop_duplicates(subset=['wordpos'])  # Drop duplicate wordpos
                             ['word'].tolist())  # Collect unique words as a list
        .reset_index(name='predicted')  # Reset index and rename the column
    )
    
    # Ensure all textids are included, even those without predictions
    all_textids = pd.DataFrame({'textid': data['textid'].unique()})
    result = all_textids.merge(result, on='textid', how='left')
    result['predicted'] = result['predicted'].apply(
        lambda x: x if isinstance(x, list) else []  # Replace NaN with empty lists
    )
    
    # Save the result to a TSV file
    result.to_csv(output_file, sep='\t', index=False)
'''

def process_and_save_file(input_file, output_file):
    """
    Process the input file to filter and deduplicate predictions, saving the results as a TSV file.
    Adds a 'wordpos' column corresponding to the positions of the predicted words.
    
    :param input_file: Path to the input TSV file.
    :param output_file: Path to save the processed TSV file.
    """
    # Load the input file
    data = pd.read_csv(input_file, sep='\t')
    
    # Filter rows where predicted is 'A'
    filtered_data = data[data['predicted'] == 'A']
    
    # Exclude 'textid' explicitly before grouping
    filtered_data_excluded = filtered_data.drop(columns=['textid'])

    # Group by 'textid' and deduplicate based on wordpos
    grouped_result = filtered_data_excluded.groupby(filtered_data['textid'], group_keys=False).apply(
        lambda group: {
            'words': group.sort_values('wordpos')['word'].drop_duplicates().tolist(),  # Deduplicate and list words
            'positions': group.sort_values('wordpos')['wordpos'].drop_duplicates().tolist()  # Deduplicate and list positions
        }
    )
    
    # Flatten the grouped result into a DataFrame
    result = pd.DataFrame({
        'textid': grouped_result.index,
        'predicted': [x['words'] for x in grouped_result.values],
        'wordpos': [x['positions'] for x in grouped_result.values]
    })
    
    # Ensure all textids are included, even those without predictions
    all_textids = pd.DataFrame({'textid': data['textid'].unique()})
    result = all_textids.merge(result, on='textid', how='left')
    
    # Replace NaN with empty lists for missing predictions
    result['predicted'] = result['predicted'].apply(lambda x: x if isinstance(x, list) else [])
    result['wordpos'] = result['wordpos'].apply(lambda x: x if isinstance(x, list) else [])
    
    # Save the result to a TSV file
    result.to_csv(output_file, sep='\t', index=False)
    print(f"Processed data saved to {output_file}.")
    return result

# Re-run the processing on the provided file
try:
    processed_result_test_fixed = process_and_save_file_fixed(input_file_path_test, output_file_path_test)
    # Verify if the file has been saved correctly
    tools.display_dataframe_to_user(name="Processed Data for Fixed File", dataframe=processed_result_test_fixed)
except Exception as e:
    str(e)




def main():
    """
    Main function to execute the processing script.
    """
    
    # Process the file and save the output
    process_and_save_file('../predictions/MULTIBERT.tsv', 'MULTIBERT.tsv')
    #process_and_save_file('../predictions/SQUAD.tsv', 'SQUAD.tsv')
    #print(pd.__version__)


# Entry point for the script
if __name__ == "__main__":
    main()
