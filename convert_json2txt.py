import json
import os
import argparse

def convert_json_to_text(json_file, output_dir, magnify_factor):
    with open(json_file, 'r') as json_file:
        json_data = json.load(json_file)

    # Loop through objects in the JSON data
    for i, obj in enumerate(json_data['objects']):
        x = obj['centroid']['x'] * magnify_factor
        y = obj['centroid']['y'] * magnify_factor
        z = obj['centroid']['z'] * magnify_factor
        dx = obj['dimensions']['length'] * magnify_factor
        dy = obj['dimensions']['width'] * magnify_factor
        dz = obj['dimensions']['height'] * magnify_factor
        rot = obj['rotations']['z']
        cls = obj['name']

        # Format the data as a line of text
        line = f"{x} {y} {z} {dx} {dy} {dz} {rot} {cls}"

        # Create the output text file name following the naming logic
        file_number = str(i).zfill(6)  # Format the index with leading zeros
        output_filename = os.path.join(output_dir, f"{file_number}.txt")

        # Write the line to the text file
        with open(output_filename, 'w') as output_file:
            output_file.write(line)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON label files to text files.")
    parser.add_argument("--input_dir", required=True, help="Input directory containing JSON label files.")
    parser.add_argument("--output_dir", required=True, help="Output directory for text files.")
    parser.add_argument("--magnify_factor", type=float, default=20.0, help="Magnification factor (default: 20.0)")

    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Loop through the input directory and process each JSON file
    for root, dirs, files in os.walk(args.input_dir):
        for file in files:
            if file.endswith(".json"):
                json_file = os.path.join(root, file)
                convert_json_to_text(json_file, args.output_dir, args.magnify_factor)

    print("Text files created successfully.")

if __name__ == "__main__":
    main()
