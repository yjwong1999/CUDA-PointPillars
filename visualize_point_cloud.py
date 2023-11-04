import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def main(args):
    # Load binary point cloud
    bin = np.fromfile(args.bin_file, dtype=np.float32)

    # Reshape and drop reflection values
    points = bin.reshape((-1, 4))[:, 0:3]

    # Read the content of the output file and parse the data
    with open(args.pred_file, 'r') as file:
        lines = file.readlines()

    # Create a list of bounding boxes (cuboids)
    boxes = []
    for line in lines:
        data = line.split()
        if len(data) == 8:
          x, y, z, dx, dy, dz, rot, cls = map(float, data)
        elif len(data) == 9:
          x, y, z, dx, dy, dz, rot, cls, conf = map(float, data)
        else:
          print(f"Unexpected number of items in line: {len(data)}")

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
        boxes.append(rectangle)

    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(20, 10))

    # Create a scatter plot of the point cloud (bird's eye view) in the left subplot
    axs[0].scatter(points[:, 0], points[:, 1], s=0.1, c=points[:, 2], cmap='viridis')

    # Set plot limits and labels for the left subplot
    axs[0].set_xlim(-10, 30)
    axs[0].set_ylim(0, 30)
    axs[0].set_xlabel('X')
    axs[0].set_ylabel('Y')

    # Create a scatter plot of the point cloud (bird's eye view) in the right subplot
    axs[1].scatter(points[:, 0], points[:, 1], s=0.1, c=points[:, 2], cmap='viridis')

    # Add the bounding boxes to the right subplot
    for box in boxes:
        axs[1].add_patch(box)

    # Set plot limits and labels for the right subplot
    axs[1].set_xlim(-10, 30)
    axs[1].set_ylim(0, 30)
    axs[1].set_xlabel('X')
    axs[1].set_ylabel('Y')

    # Show the plot
    plt.savefig('visualization.png')
    print('Done Visualization....Saving in current directory')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize 3D point cloud with bounding boxes')
    parser.add_argument('--bin_file', type=str, required=True, help='Path to the binary point cloud file')
    parser.add_argument('--pred_file', type=str, required=True, help='Path to the prediction file')
    args = parser.parse_args()
    main(args)
