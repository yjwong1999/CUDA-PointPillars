import json
import os
import argparse

def convert_json_to_text(json_file_path, output_dir, magnify_factor, file_counter):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    lines = []

    for obj in json_data['objects']:
        x = obj['centroid']['x'] * magnify_factor
        y = obj['centroid']['y'] * magnify_factor
        z = obj['centroid']['z'] * magnify_factor
        dx = obj['dimensions']['length'] * magnify_factor
        dy = obj['dimensions']['width'] * magnify_factor
        dz = obj['dimensions']['height'] * magnify_factor
        rot = obj['rotations']['z']
        cls = 0 if obj['name'] == 'good' else 1

        line = f"{x} {y} {z} {dx} {dy} {dz} {rot} {cls}"
        lines.append(line)

    # Use the file_counter to name the output file
    output_filename = os.path.join(output_dir, f"{str(file_counter).zfill(6)}.txt")

    with open(output_filename, 'w') as output_file:
        for line in lines:
            output_file.write(line + '\n')

def main():
    parser = argparse.ArgumentParser(description="Convert JSON label files to text files.")
    parser.add_argument("--input_dir", required=True, help="Input directory containing JSON label files.")
    parser.add_argument("--output_dir", required=True, help="Output directory for text files.")
    parser.add_argument("--magnify_factor", type=float, default=20.0, help="Magnification factor (default: 20.0)")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    json_files = sorted([f for f in os.listdir(args.input_dir) if f.endswith(".json")])

    # Initialize a counter for the output files
    file_counter = 0

    for json_file in json_files:
        json_file_path = os.path.join(args.input_dir, json_file)
        convert_json_to_text(json_file_path, args.output_dir, args.magnify_factor, file_counter)

        # Increment the counter after each file is processed
        file_counter += 1

    print("Text files created successfully.")

if __name__ == "__main__":
    main()
