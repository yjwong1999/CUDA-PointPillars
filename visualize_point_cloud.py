import argparse
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def visualize_3d_point_cloud(bin_dir, pred_dir, truth_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # List all binary point cloud files in the specified directory
    bin_files = [f for f in os.listdir(bin_dir) if f.endswith('.bin')]

    for bin_file in bin_files:
        bin_path = os.path.join(bin_dir, bin_file)
        pred_file = os.path.join(pred_dir, bin_file.replace('.bin', '.txt'))
        truth_file = os.path.join(truth_dir, bin_file.replace('.bin', '.txt'))

        # Check if prediction and truth files exist before processing
        if not (os.path.exists(pred_file)):
            print(f"Skipping {bin_file} as prediction label file do not exist.")
            continue

        # Load binary point cloud
        bin = np.fromfile(bin_path, dtype=np.float32)

        # Reshape and drop reflection values
        points = bin.reshape((-1, 4))[:, 0:3]

        # Read the content of the output file and parse the data
        with open(pred_file, 'r') as file:
            lines = file.readlines()

        # Create a list of bounding boxes (cuboids)
        pred_boxes = []
        for line in lines:
            data = line.split()
            if len(data) == 9:
              x, y, z, dx, dy, dz, rot, cls, conf = map(float, data)
            else:
              print(f"Unexpected pred number of items in line: {len(data)}")

            # Create a rectangle representing the bounding box (bird's eye view)
            #rectangle = plt.Rectangle((x - dx / 2, y - dy / 2), dx, dy, fill=False, color="red")
            bottom_left_x = x - dx / 2
            bottom_left_y = y - dy / 2
            rot = rot * 57.2957795 # rad to degree
            if cls == 1: 
                color = 'red' 
            else:
                color = 'blue'
            rectangle = matplotlib.patches.Rectangle((bottom_left_x, bottom_left_y), dx, dy, angle=rot, \
                                                        rotation_point="center", color=color, fill=False)
            pred_boxes.append(rectangle)

        # Read the content of the output file and parse the data
        with open(truth_file, 'r') as file:
            lines = file.readlines()

        # Create a list of bounding boxes (cuboids)
        truth_boxes = []
        for line in lines:
            data = line.split()
            if len(data) == 8:
              x, y, z, dx, dy, dz, rot, cls = map(float, data)
            else:
              print(f"Unexpected truth number of items in line: {len(data)}")

            # Create a rectangle representing the bounding box (bird's eye view)
            #rectangle = plt.Rectangle((x - dx / 2, y - dy / 2), dx, dy, fill=False, color="red")
            bottom_left_x = x - dx / 2
            bottom_left_y = y - dy / 2
            rot = rot * 57.2957795 # rad to degree
            if cls == 1: 
                color = 'red' 
            else:
                color = 'blue'
            rectangle = matplotlib.patches.Rectangle((bottom_left_x, bottom_left_y), dx, dy, angle=rot, \
                                                        rotation_point="center", color=color, fill=False)
            truth_boxes.append(rectangle)

        # Create a figure with two subplots
        fig, axs = plt.subplots(1, 2, figsize=(20, 10))

        # Create a scatter plot of the point cloud (bird's eye view) in the left subplot
        axs[0].scatter(points[:, 0], points[:, 1], s=0.1, c=points[:, 2], cmap='viridis')

        # Add the bounding boxes to the right subplot
        for box in truth_boxes:
            axs[0].add_patch(box)

        # Set plot limits and labels for the left subplot
        axs[0].set_xlim(-10, 30)
        axs[0].set_ylim(0, 30)
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Y')

        # Create a scatter plot of the point cloud (bird's eye view) in the right subplot
        axs[1].scatter(points[:, 0], points[:, 1], s=0.1, c=points[:, 2], cmap='viridis')

        # Add the bounding boxes to the right subplot
        for box in pred_boxes:
            axs[1].add_patch(box)

        # Set plot limits and labels for the right subplot
        axs[1].set_xlim(-10, 30)
        axs[1].set_ylim(0, 30)
        axs[1].set_xlabel('X')
        axs[1].set_ylabel('Y')

        # Save the figure with a unique name based on the input binary file
        figure_filename = os.path.splitext(bin_file)[0] + '_visualization.png'
        figure_path = os.path.join(output_dir, figure_filename)
        plt.savefig(figure_path)
        print(f'Saved visualization for {bin_file} in {figure_path}')

        # Close the figures to prevent memory consumption
        plt.close('all')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize 3D point clouds with bounding boxes')
    parser.add_argument('--bin_dir', type=str, required=True, help='Directory containing binary point cloud files')
    parser.add_argument('--pred_dir', type=str, required=True, help='Directory containing prediction text files')
    parser.add_argument('--truth_dir', type=str, required=True, help='Directory containing truth label text files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to save visualization figures')
    args = parser.parse_args()
    visualize_3d_point_cloud(args.bin_dir, args.pred_dir, args.truth_dir, args.output_dir)
