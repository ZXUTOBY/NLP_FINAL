import ast

def parse_file(file_path):
    """
    Reads and parses a file assuming all rows are valid.

    Args:
        file_path (str): Path to the input file.

    Returns:
        dict: Parsed predictions as {textid: (tokens, positions)}.
    """
    predictions = {}
    with open(file_path, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            parts = line.strip().split('\t')
            textid = parts[0]
            
            # Custom parsing for 'predicted' column
            tokens = parts[1].strip("[]").split(", ")
            tokens = [token.strip("'") for token in tokens]  # Remove surrounding quotes
            
            # Custom parsing for 'wordpos' column
            positions = parts[2].strip("[]").split(", ")
            positions = [int(pos) for pos in positions if pos.isdigit()]  # Convert to integers
            
            predictions[textid] = (tokens, positions)
    return predictions

def aggregate_predictions(all_predictions, weights, threshold):
    """
    Combines predictions from multiple models using weights and a threshold.

    Args:
        all_predictions (list of dict): Predictions from all input files.
        weights (list of float): Weights for each model.
        threshold (float): Minimum score to include a token.

    Returns:
        dict: Aggregated predictions as {textid: {"tokens": [...], "positions": [...]}}.
    """
    combined_scores = {}
    textid_order = []  # Track the original order of textids

    # Combine predictions with weights
    for predictions, weight in zip(all_predictions, weights):
        for textid, (tokens, positions) in predictions.items():
            if textid not in textid_order:
                textid_order.append(textid)  # Add to order tracking
            for token, position in zip(tokens, positions):
                key = (textid, token, position)
                if key not in combined_scores:
                    combined_scores[key] = 0
                combined_scores[key] += weight

    # Filter by threshold and aggregate results
    aggregated = {}
    for (textid, token, position), score in combined_scores.items():
        if score >= threshold:
            if textid not in aggregated:
                aggregated[textid] = {"tokens": [], "positions": []}
            aggregated[textid]["tokens"].append(token)
            aggregated[textid]["positions"].append(position)

    # Ensure all textids are preserved, even those with no valid tokens
    for predictions in all_predictions:
        for textid in predictions.keys():
            if textid not in aggregated:
                aggregated[textid] = {"tokens": [], "positions": []}

    # Return aggregated results and original order
    return aggregated, textid_order


def write_output(predictions, textid_order, output_file):
    """
    Writes aggregated predictions to a TSV file in the original order of textids.

    Args:
        predictions (dict): Aggregated predictions as {textid: {"tokens": [...], "positions": [...]}}.
        textid_order (list): Original order of textids.
        output_file (str): Path to the output TSV file.
    """
    with open(output_file, 'w') as file:
        file.write("textid\tpredicted\twordpos\n")
        for textid in textid_order:
            values = predictions.get(textid, {"tokens": [], "positions": []})
            tokens = repr(values["tokens"])  # Preserve single quotes
            positions = repr(values["positions"])  # Preserve formatting
            file.write(f"{textid}\t{tokens}\t{positions}\n")


def compute_weights(numbers):
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")
    
    total = sum(numbers)
    
    if total == 0:
        raise ValueError("The sum of the numbers cannot be zero.")
    
    ratios = [num / total for num in numbers]
    return ratios

    
def main():
    model_files = ["BERT.tsv", "ROBERTA.tsv", "MiniLM.tsv", "MULTIBERT.tsv"]
    raw_weights = [0.5031831130113923, 0.435627058867456, 0.4256175795679302, 0.46968535792013516]
    weights = compute_weights(raw_weights)  # Example weights
    threshold = 0.7
    output_file = "0.7_RECL.tsv"

    # Parse input files
    all_predictions = [parse_file(file) for file in model_files]

    # Aggregate predictions
    aggregated, textid_order = aggregate_predictions(all_predictions, weights, threshold)

    # Write to output file
    write_output(aggregated, textid_order, output_file)
    print(f"Aggregated predictions saved to {output_file}.")


if __name__ == "__main__":
    main()










