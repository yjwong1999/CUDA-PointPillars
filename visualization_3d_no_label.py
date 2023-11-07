import numpy as np
import argparse
import plotly.graph_objects as go

try:
    import open3d as o3d
    print("Open3D is already installed.")
except ImportError:
    print("Open3D is not found. Installing Open3D...")
    try:
        import subprocess
        subprocess.check_call(["pip", "install", "open3d"])
        print("Open3D has been successfully installed.")
    except Exception as e:
        print("An error occurred while installing Open3D:", e)

def draw(geometries):
    graph_obj = []

    for gm in geometries:
        geometry_type = gm.get_geometry_type()

        if geometry_type == o3d.geometry.Geometry.Type.PointCloud:
            pts = np.asarray(gm.points)
            clr = None  #for colors
            if gm.has_colors():
                clr = np.asarray(gm.colors)
            elif gm.has_normals():
                clr = (0.5, 0.5, 0.5) + np.asarray(gm.normals) * 0.5
            else:
                gm.paint_uniform_color((1.0, 0.0, 0.0))
                clr = np.asarray(gm.colors)

            sc = go.Scatter3d(x=pts[:,0], y=pts[:,1], z=pts[:,2], mode='markers', marker=dict(size=1, color=clr))
            graph_obj.append(sc)

        if geometry_type == o3d.geometry.Geometry.Type.TriangleMesh:
            tri = np.asarray(gm.triangles)
            vert = np.asarray(gm.vertices)
            clr = None
            if gm.has_triangle_normals():
                clr = (0.5, 0.5, 0.5) + np.asarray(gm.triangle_normals) * 0.5
                clr = tuple(map(tuple, clr))
            else:
                clr = (1.0, 0.0, 0.0)

            mesh = go.Mesh3d(x=vert[:,0], y=vert[:,1], z=vert[:,2], i=tri[:,0], j=tri[:,1], k=tri[:,2], facecolor=clr, opacity=0.50)
            graph_obj.append(mesh)

    fig = go.Figure(
        data=graph_obj,
        layout=dict(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            )
        )
    )
    fig.show()

def main(bin_file_path):
    # Load the point cloud data from the BIN file
    points = np.fromfile(bin_file_path, dtype=np.float32).reshape(-1, 4)

    # Extract the depth values (e.g., using the z-coordinate)
    depth_values = points[:, 2]

    # Normalize the depth values to a range between 0 and 1
    normalized_depth = (depth_values - depth_values.min()) / (depth_values.max() - depth_values.min())

    # Inverse the color gradient (red to blue)
    inverted_normalized_depth = 1 - normalized_depth

    # Create an Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])  # Assuming x, y, z coordinates

    # Create an array of colors with the color gradient
    colors = []
    for depth in inverted_normalized_depth:
        color = [1 - depth, 0, depth]  # Red to blue gradient
        colors.append(color)

    # Assign the colors to the point cloud
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # Visualize the point cloud
    o3d.visualization.draw_geometries = draw  # Replace with your draw function
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize point cloud from a BIN file.")
    parser.add_argument("bin_file_path", type=str, help="Path to the BIN file")
    args = parser.parse_args()

    main(args.bin_file_path)
