import re
import pandas as pd
import json

def custom_tokenize(text):
    pattern = r'\b\w+(?:[.\-&]\w+)*\b|[^\w\s]'
    return re.findall(pattern, text)

def write_tsv(input_file, output_file, max_tokens=350):
    data = pd.read_csv(input_file, sep='\t')

    # Prepare rows for output
    output_rows = []

    for _, row in data.iterrows():
        # Extract columns from input data
        textid = row['id']  # Keep "id" as "textid"
        context = row['context']
        question = row['question']
        
        # Tokenize context and question
        context_tokens = custom_tokenize(context)
        question_tokens = custom_tokenize(question)
        
        # Combine tokens into a single list
        tokens = ["TEXT"] + context_tokens + ["QUESTION"] + question_tokens
        
        # Skip rows where token count exceeds max_tokens
        if len(tokens) > max_tokens:
            continue
        
        # Combine tokens into a single string, ensuring no spaces before punctuation

        '''
        text = "".join(
            token if re.match(r"[^\w\s]", token) else f" {token}" for token in tokens
        ).strip()
        '''
        text = " ".join(tokens)
        
        
        # Generate the "target" column with all 'N'
        target = " ".join(["O"] * len(tokens))
        
        # Use "random" as the condition
        condition = "random"
        
        # Add row to output
        output_rows.append({
            'textid': textid,
            'text': text,
            'condition': condition,
            'target': target
        })

    # Convert rows to DataFrame and save as TSV
    output_df = pd.DataFrame(output_rows)
    output_df.to_csv(output_file, sep='\t', index=False)

    print(f"Data has been written to {output_file}, excluding rows with more than {max_tokens} tokens.")






def main():
    #splits = {'validation': 'squad_v2/validation-00000-of-00001.parquet'}
    #df = pd.read_parquet("hf://datasets/rajpurkar/squad_v2/" + splits["validation"])
    #df.to_csv('test.tsv', sep='\t', index=False)   

    write_tsv('before.tsv', 'after.tsv')

    '''
    print(len("TEXT: The Normans( Norman: Nourmands; French: Normands; Latin: Normanni) were the people who in the 10th and 11th centuries gave their name to Normandy, a region in France. They were descended from Norse("" Norman"" comes from"" Norseman"") raiders and pirates from Denmark, Iceland and Norway who, under their leader Rollo, agreed to swear fealty to King Charles III of West Francia. Through generations of assimilation and mixing with the native Frankish and Roman-Gaulish populations, their descendants would gradually merge with the Carolingian-based cultures of West Francia. The distinct cultural and ethnic identity of the Normans emerged initially in the first half of the 10th century, and it continued to evolve over the succeeding centuries."))
    '''

if __name__ == "__main__":
    main()