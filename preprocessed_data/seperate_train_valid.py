import json
import random

def split_json_file(input_file, output_file_90, output_file_10):
    try:
        with open(input_file, "r") as file:
            lines = file.readlines()

        random.shuffle(lines)
        split_index = int(len(lines) * 0.9)
        lines_90 = lines[:split_index]
        lines_10 = lines[split_index:]

        with open(output_file_90, "w") as file_90:
            file_90.writelines(lines_90)

        with open(output_file_10, "w") as file_10:
            file_10.writelines(lines_10)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    input_file = "../train_data/train&valid.jsonl"
    output_file_90 = "../train_data/train.jsonl"
    output_file_10 = "../train_data/valid.jsonl"
    split_json_file(input_file, output_file_90, output_file_10)

if __name__ == "__main__":
    main()
