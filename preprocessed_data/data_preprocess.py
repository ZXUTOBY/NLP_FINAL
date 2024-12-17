import re
import pandas as pd
import json

def custom_tokenize(text):
    pattern = r'\b\w+(?:[.\-&]\w+)*\b|[^\w\s]'
    return re.findall(pattern, text)

def write_jsonl(input_file, output_file):
    data = pd.read_csv(input_file, sep='\t')

    # Process each row in the TSV file
    with open(output_file, 'w') as f:
        for _, row in data.iterrows():
            count = 0
            
            '''
            if count > 100:
                break
            '''
            
            # Extract context, question, and answers
            context = row['context']
            question = row['question']
            
            # Replace "array(" with "[" and ")" with "]", and remove "dtype=" sections
            answers_str = row['answers']
            answers_str = re.sub(r'\barray\(', '[', answers_str)  # Replace "array(" with "["
            answers_str = re.sub(r'\bdtype=\w+\b', '', answers_str)  # Remove "dtype=..." completely
            answers_str = answers_str.replace(')', ']')  # Replace ")" with "]"
            answers_str = re.sub(r'\s+', ' ', answers_str).strip()  # Clean up any extra whitespace

            # Convert modified string to a dictionary safely
            try:
                answers = eval(answers_str)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing answers: {answers_str}\n{e}")
                continue  # Skip this row if eval fails
            
            # Tokenize context and question
            context_tokens = custom_tokenize(context)
            question_tokens = custom_tokenize(question)
            tokens = ["TEXT"] + context_tokens + ["QUESTION"] + question_tokens
            
            # Initialize tags with 0s for all tokens
            tags = [0] * len(tokens)

            # Check if 'text' key exists in answers and contains non-empty answers
            if 'text' in answers and answers['text']:
                # Process each answer in the "text" list
                for answer_text in answers['text']:
                    if isinstance(answer_text, list) and answer_text:
                        answer_text = answer_text[0]  # Handle nested non-empty lists
                    elif not answer_text:  # Skip if answer_text is empty or None
                        continue
                    
                    answer_tokens = custom_tokenize(answer_text)  # Tokenize answer

                    # Attempt a flexible match using a sliding window over context_tokens
                    answer_length = len(answer_tokens)
                    for i in range(len(context_tokens) - answer_length + 1):
                        # Compare a window in context_tokens with answer_tokens
                        window = context_tokens[i:i + answer_length]
                        # Normalize to lowercase and ignore punctuation for matching
                        window_norm = [re.sub(r'\W+', '', w).lower() for w in window]
                        answer_norm = [re.sub(r'\W+', '', a).lower() for a in answer_tokens]

                        if window_norm == answer_norm:
                            # Set tags to 1 for matched tokens
                            for j in range(answer_length):
                                tags[i + j] = 1
                            break  # Stop after finding the first match for this answer

            # Create entry and write to JSONL
            entry = {"tokens": tokens, "tags": tags}
            f.write(json.dumps(entry) + '\n')
            count += 1

    print(f"Data has been written to {output_file}")

    

def main():
    '''
    # Read the Parquet file
    df = pd.read_parquet('train.parquet')
    
    # Save as JSON in the current folder
    df.to_csv('train.tsv', sep='\t', index=False)   
    '''
    write_jsonl('train.tsv', 'train&valid.jsonl')


if __name__ == "__main__":
    main()
