import os
import re
import sys
from glob import glob


def extract_cost_time(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Look for the cost time pattern
            match = re.search(r"Cost time: (\d+\.\d+)s", content)
            if match:
                return float(match.group(1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None


def extract_align_value(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            try:
                return float(first_line)
            except ValueError:
                print(
                    f"Could not convert first line to float in {file_path}: {first_line}"
                )
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None


def main(base_path):
    # Process feedback.txt files
    feedback_files = glob(f"{base_path}/**/feedback.txt", recursive=True)

    total_cost_time = 0.0
    files_without_cost_time = 0
    total_file = 0
    for file_path in feedback_files:
        cost_time = extract_cost_time(file_path)
        if cost_time is not None:
            total_cost_time += cost_time
            total_file += 1
        else:
            files_without_cost_time += 1

    if total_file > 0:
        print(f"Average cost time: {total_cost_time / total_file:.2f}s")
    else:
        print("No files with valid cost time found.")
    print(f"Can't aligned: {files_without_cost_time}")
    print(f"Total feedback files processed: {len(feedback_files)}")

    # Process align.txt files
    align_files = glob(f"{base_path}/**/tmp/align.txt", recursive=True)

    align_values = []
    for file_path in align_files:
        value = extract_align_value(file_path)
        if value is not None:
            align_values.append(value)

    if align_values:
        avg_align_value = sum(align_values) / len(align_values)
        print(f"\nTotal align.txt files processed: {len(align_files)}")
        print(f"Average accuracy: {avg_align_value:.10f}")
    else:
        print("\nNo align.txt files found or no valid values extracted.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_search>")
        print("Example: python script.py ./data/MAXDIFF/bpex_result/")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.exists(base_path):
        print(f"Error: Path '{base_path}' does not exist")
        sys.exit(1)

    main(base_path)
