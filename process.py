import json
import re
import sys
import os

def process_json(json_file_path, output_file_path):
    """
    Processes a JSON file, extracts the left-hand side source code from the alignment,
    removes numbers and spaces, and writes the results to a text file.

    Args:
        json_file_path (str): The path to the input JSON file.
        output_file_path (str): The path to the output text file.
    """

    from Levenshtein import distance

    results = []
    mp = dict()

    accurracy = 0
    pair = 0

    with open(json_file_path, "r") as f:
        data = json.load(f)

    for item in data["alignment"]:
        # Split by '<->'
        parts = item.split("<->")
        if len(parts) == 2:
            left_side = parts[0]
            right_side = parts[1]

            left_match = re.search(r':src \"(\d+):(.*?)"', left_side)
            left_src = left_match.group(2) if left_match else None

            right_match = re.search(r':src \"(\d)+:(.*?)"', right_side)
            right_src = right_match.group(2) if right_match else None

            left_line = int(left_match.group(1)) if left_match else None
            right_line = int(right_match.group(1)) if right_match else None

            if left_src and right_src:
                left_src = left_src.strip()
                right_src = right_src.strip()
                left_src = left_src.strip(r"\t")
                right_src = right_src.strip(r"\t")
                left_src = left_src.strip()
                right_src = right_src.strip()
                results.append(f"{left_src} <-> {right_src}")

                if (left_line, right_line) in mp:
                    dist = distance(left_src, right_src)
                    similarity = 1 - dist / max(len(left_src), len(right_src))
                    pair += 1
                    accurracy += similarity
                mp[(left_line, right_line)] = 1

    with open(output_file_path, "w") as f:
        res = 0
        if pair != 0:
            res = accurracy / pair
        f.write(str(res) + "\n")
        for item in results:
            f.write(item + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path/to/res.json>")
        sys.exit(1)

    input_json_file = sys.argv[1]
    output_file_path = os.path.join(
     os.path.dirname(input_json_file), "align.txt"
    )
    process_json(input_json_file, output_file_path)
