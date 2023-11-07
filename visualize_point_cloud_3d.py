import numpy as np
import os

# Check if Plotly is installed and install it if necessary
try:
    import plotly.express as px
except ImportError:
    !pip install plotly
    import plotly.express as px
import plotly.graph_objects as go

def load_point_cloud(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    return point_cloud

def load_label_data(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, 'r') as f:
        label_data = [line.strip().split() for line in f]
    return label_data

def add_bounding_boxes(fig, label_data):
    for label in label_data:
        x, y, z, dx, dy, dz, rot, cls = map(float, label)
        corners, edges = get_bounding_box(x, y, z, dx, dy, dz, rot)
        fig = add_edges_to_plot(fig, edges, cls)
    return fig

def get_bounding_box(x, y, z, dx, dy, dz, rot):
    corners = np.array([
        [x - dx / 2, y - dy / 2, z - dz / 2],
        [x + dx / 2, y - dy / 2, z - dz / 2],
        [x + dx / 2, y + dy / 2, z - dz / 2],
        [x - dx / 2, y + dy / 2, z - dz / 2],
        [x - dx / 2, y - dy / 2, z + dz / 2],
        [x + dx / 2, y - dy / 2, z + dz / 2],
        [x + dx / 2, y + dy / 2, z + dz / 2],
        [x - dx / 2, y + dy / 2, z + dz / 2]
    ])
    R = np.array([
        [np.cos(rot), -np.sin(rot), 0],
        [np.sin(rot), np.cos(rot), 0],
        [0, 0, 1]
    ])
    corners = np.dot(corners - np.array([x, y, z]), R.T) + np.array([x, y, z])
    edges = [
        [corners[0], corners[1]],
        [corners[1], corners[2]],
        [corners[2], corners[3]],
        [corners[3], corners[0]],
        [corners[4], corners[5]],
        [corners[5], corners[6]],
        [corners[6], corners[7]],
        [corners[7], corners[4]],
        [corners[0], corners[4]],
        [corners[1], corners[5]],
        [corners[2], corners[6]],
        [corners[3], corners[7]]
    ]
    return corners, edges

def add_edges_to_plot(fig, edges, cls):
    color_map = {0: 'blue', 1: 'red'}
    for edge in edges:
        x_values = [point[0] for point in edge]
        y_values = [point[1] for point in edge]
        z_values = [point[2] for point in edge]
        color = color_map[cls]
        fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(color=color)))
    return fig

def main():
    parser = argparse.ArgumentParser(description='Visualize point cloud data with bounding boxes')
    parser.add_argument('bin_file', help='Path to the binary file')
    parser.add_argument('label_file', help='Path to the label text file')
    args = parser.parse_args()

    point_cloud = load_point_cloud(args.bin_file)
    label_data = load_label_data(args.label_file)

    fig = go.Figure(data=[go.Scatter3d(
        x=point_cloud[:, 0],
        y=point_cloud[:, 1],
        z=point_cloud[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=point_cloud[:, 2],
            colorscale='Viridis',
            opacity=0.8
        )
    )])

    fig = add_bounding_boxes(fig, label_data)

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=None),
            yaxis=dict(showbackground=False, showticklabels=False, title=None),
            zaxis=dict(showbackground=False, showticklabels=False, title=None),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=0.5)
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual'
        ),
        paper_bgcolor='rgba(255,255,255,255)',
        plot_bgcolor='rgba(255,255,255,255)'
    )

    fig.show()

if __name__ == '__main__':
    main()
