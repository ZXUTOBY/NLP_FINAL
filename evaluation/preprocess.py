import pandas as pd
import ast
import re

def custom_tokenize(text):
    pattern = r'\b\w+(?:[.\-&]\w+)*\b|[^\w\s]'
    return re.findall(pattern, text)

def extract_text_from_answers(answer_str):
    # Replace "array(" with "[" and ")" with "]"
    answer_str = re.sub(r'array\(', '[', answer_str)  # Replace array with [
    answer_str = re.sub(r'\bdtype=\w+\b', '', answer_str)  # Remove dtype=...
    answer_str = answer_str.replace(')', ']')  # Replace closing parenthesis
    answer_str = re.sub(r'\s+', ' ', answer_str).strip()  # Remove extra spaces
    try:
        # Safely evaluate the cleaned string as a dictionary
        parsed_answer = ast.literal_eval(answer_str)
        return parsed_answer.get('text') if isinstance(parsed_answer, dict) else None
    except (ValueError, SyntaxError):
        return None

def flatten_text_array(answer_text):
    if isinstance(answer_text, list):
        # Flatten nested arrays and remove duplicates
        flat_list = [item for sublist in answer_text for item in sublist] if isinstance(answer_text[0], list) else answer_text
        return list(set(flat_list))  # Remove duplicates
    return answer_text

def process_file(input_file, output_file, max_tokens=350):
    # Load the input file
    data = pd.read_csv(input_file, sep='\t')  # Limit to 100 rows for simplicity

    # Prepare rows for output
    output_rows = []

    for _, row in data.iterrows():
        # Tokenize the context and question to calculate the total token count
        context_tokens = custom_tokenize(row['context'])
        question_tokens = custom_tokenize(row['question'])
        tokens = ["TEXT"] + context_tokens + ["QUESTION"] + question_tokens

        # Skip rows where token count exceeds the limit
        if len(tokens) > max_tokens:
            continue

        # Process the 'answers' column
        answers = extract_text_from_answers(row['answers'])
        answers = flatten_text_array(answers)

        # Add the processed row to output
        output_rows.append({
            'textid': row['id'],
            'answers': answers
        })

    # Create a new DataFrame
    modified_data = pd.DataFrame(output_rows)

    # Save the modified data to the output file
    modified_data.to_csv(output_file, sep='\t', index=False)
    print(f"Processed data has been saved to {output_file}, excluding rows with more than {max_tokens} tokens.")


# Main entry point
if __name__ == "__main__":
    input_file = "../test_data/before.tsv"  # Input file path
    output_file = "answers.tsv"  # Output file path
    process_file(input_file, output_file)









