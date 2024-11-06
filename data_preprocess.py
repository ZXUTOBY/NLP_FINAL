import pandas as pd
import os



def transform_dataset(df):
    # Rename 'id' to 'textid'
    df = df.rename(columns={'id': 'textid'})

    # Combine 'context' and 'question' into one column called 'text'
    df['text'] = df['context'] + ' ' + df['question']

    # Create a 'condition' column with the value "random"
    df['condition'] = 'random'

    # Create formatted 'target'
    def format_target(row):
        combined_text = row['text']
        answer_text = row['answers']['text'][0]  # Extracting the answer text
        
        # Split the combined text into words and initialize the target tagging with "O"
        words = combined_text.split()
        target_tags = ["O"] * len(words)

        # Find the starting index of the answer in the combined text
        start_index = combined_text.find(answer_text)
        if start_index != -1:
            # Find the word-level indexes of the answer
            answer_words = answer_text.split()
            answer_start_word_index = len(combined_text[:start_index].split())
            for i in range(len(answer_words)):
                target_tags[answer_start_word_index + i] = 'A'

        # Create the formatted target string
        return " ".join(target_tags)
    
    # Apply the target formatting function
    df['target'] = df.apply(format_target, axis=1)

    # Drop the original 'title', 'context', 'question', and 'answers' columns
    df = df.drop(columns=['title', 'context', 'question', 'answers'])
    
    return df

def transform_and_save_to_csv(df, folder_path, file_name):
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Full path for the output CSV file
    output_path = os.path.join(folder_path, file_name)

    # Save the DataFrame to a CSV file
    df.to_csv(output_path, index=False, sep="\t")
    print(f"DataFrame has been saved to {output_path}")
    

def main():
    
    #splits = {'train': 'squad_v2/train-00000-of-00001.parquet', 'validation': 'squad_v2/validation-00000-of-00001.parquet'}
    #df = pd.read_parquet("hf://datasets/rajpurkar/squad_v2/" + splits["train"])
        
    # Apply the function to transform the dataset
    #test_train_df = transform_dataset(df.iloc[0:100])
    #test_valid_df = transform_dataset(df.iloc[101:200])
    #test_eval_df = transform_dataset(df.iloc[201:300])

    #transform_and_save_to_csv(test_train_df, "train_data", "test.csv")
    #transform_and_save_to_csv(test_valid_df, "validation_data", "test.csv")
    #transform_and_save_to_csv(test_eval_df, "test_data", "test.csv")

    

if __name__ == "__main__":
    main()
