import pandas as pd
import ast

def EM(pred_file, answers_file):
    pred_data = pd.read_csv(pred_file, sep='\t')
    answers_data = pd.read_csv(answers_file, sep='\t')
    merged_data = pd.merge(pred_data, answers_data, on='textid', how='inner')
    exact_match_count = 0

    for _, row in merged_data.iterrows():
        if pd.isna(row['predicted']) and pd.isna(row['answers']):
            exact_match_count += 1  # Both are empty, count as correct
            continue
        
        if pd.isna(row['predicted']) or pd.isna(row['answers']):
            continue  # Skip if only one is empty
        
        try:
            predicted = ast.literal_eval(row['predicted'])
            answers = ast.literal_eval(row['answers'])
        except (SyntaxError, ValueError):
            continue

        if not predicted and not answers:
            exact_match_count += 1  # Both are empty lists, count as correct
        else:
            predicted_combination = ' '.join(predicted)
            if predicted_combination in answers:
                exact_match_count += 1

    return exact_match_count


def precision(pred_file, answers_file):
    pred_data = pd.read_csv(pred_file, sep='\t')
    answers_data = pd.read_csv(answers_file, sep='\t')
    merged_data = pd.merge(pred_data, answers_data, on='textid', how='inner')
    total_precision = 0.0

    for _, row in merged_data.iterrows():
        if pd.isna(row['predicted']) and pd.isna(row['answers']):
            total_precision += 1  # Both are empty, count as correct
            continue
        
        if pd.isna(row['predicted']) or pd.isna(row['answers']):
            continue  # Skip if only one is empty

        try:
            predicted = set(ast.literal_eval(row['predicted']))
            answers = [set(answer.split()) for answer in ast.literal_eval(row['answers'])]
        except (SyntaxError, ValueError):
            continue

        if not predicted:
            total_precision += 1 if not any(answers) else 0  # Empty prediction matches empty answers
        else:
            max_overlap = 0
            for answer_set in answers:
                overlap = len(predicted & answer_set) / len(predicted)
                max_overlap = max(max_overlap, overlap)
            total_precision += max_overlap

    return total_precision


def recall(pred_file, answers_file):
    pred_data = pd.read_csv(pred_file, sep='\t')
    answers_data = pd.read_csv(answers_file, sep='\t')
    merged_data = pd.merge(pred_data, answers_data, on='textid', how='inner')
    total_recall = 0.0

    for _, row in merged_data.iterrows():
        if pd.isna(row['predicted']) and pd.isna(row['answers']):
            total_recall += 1  # Both are empty, count as correct
            continue
        
        if pd.isna(row['predicted']) or pd.isna(row['answers']):
            continue  # Skip if only one is empty

        try:
            predicted = set(ast.literal_eval(row['predicted']))
            answers = [set(answer.split()) for answer in ast.literal_eval(row['answers'])]
        except (SyntaxError, ValueError):
            continue

        if not predicted:
            total_recall += 1 if not any(answers) else 0  # Empty prediction matches empty answers
        else:
            max_overlap = 0
            for answer_set in answers:
                overlap = len(predicted & answer_set) / len(answer_set)
                max_overlap = max(max_overlap, overlap)
            total_recall += max_overlap

    return total_recall




def main():
    '''
    count = EM("0.5_EM.tsv", "answers.tsv")
    print("Exact Match Percentage: " + str(count / 11652))
    
    precision_count = precision("0.5_EM.tsv", "answers.tsv")
    print("PRECISION: " + str(precision_count / 11652))
    
    recall_count = recall("0.5_EM.tsv", "answers.tsv")
    print("RECALL: " + str(recall_count / 11652))
    
    '''
    count = EM("0.7_RECL.tsv", "answers.tsv")
    print("Exact Match Percentage: " + str(count / 11652))
    
    precision_count = precision("0.7_RECL.tsv", "answers.tsv")
    print("PRECISION: " + str(precision_count / 11652))
    
    recall_count = recall("0.7_RECL.tsv", "answers.tsv")
    print("RECALL: " + str(recall_count / 11652))
    
    

# Entry point for the script
if __name__ == "__main__":
    main()