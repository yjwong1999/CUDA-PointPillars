#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <open3d/Open3D.h>
#include <fstream>

struct Point {
    float x, y, z, intensity;
};

void convert_ply(const std::string& input_path, const std::string& output_path) {
    // Read data
    auto point_cloud = open3d::io::CreatePointCloudFromFile(input_path);

    // Convert to DataFrame
    std::vector<Point> points;
    for (int i = 0; i < point_cloud->points_.size(); ++i) {
        Point point;
        point.x = point_cloud->points_.at(i)(0); // Access x
        point.y = point_cloud->points_.at(i)(1); // Access y
        point.z = point_cloud->points_.at(i)(2); // Access z
        point.intensity = 0.0f;
        points.push_back(point);
    }

    // Magnify coordinates
    const float magnify_factor = 20.0f;
    for (auto& point : points) {
        point.x *= magnify_factor;
        point.y *= magnify_factor;
        point.z *= magnify_factor;
    }

    // Record point cloud range
    std::vector<float> x_values, y_values, z_values;
    for (const auto& point : points) {
        x_values.push_back(point.x);
        y_values.push_back(point.y);
        z_values.push_back(point.z);
    }
    const float min_x = *std::min_element(x_values.begin(), x_values.end());
    const float min_y = *std::min_element(y_values.begin(), y_values.end());
    const float min_z = *std::min_element(z_values.begin(), z_values.end());
    const float max_x = *std::max_element(x_values.begin(), x_values.end());
    const float max_y = *std::max_element(y_values.begin(), y_values.end());
    const float max_z = *std::max_element(z_values.begin(), z_values.end());

    // Initialize array to store data
    const std::size_t num_points = points.size();
    std::vector<float> data(num_points * 4);

    // Read data by property
    for (std::size_t i = 0; i < num_points; ++i) {
        data[i * 4 + 0] = points[i].x;
        data[i * 4 + 1] = points[i].y;
        data[i * 4 + 2] = points[i].z;
        data[i * 4 + 3] = points[i].intensity;
    }

    // Save
    if (output_path.substr(output_path.size() - 4) == ".bin") {
        std::ofstream output_file(output_path, std::ios::binary);
        output_file.write(reinterpret_cast<const char*>(data.data()), num_points * sizeof(float) * 4);
        output_file.close();
    } else if (output_path.substr(output_path.size() - 4) == ".npy") {
        // Save as numpy array
        // ...
    }
}

int main() {
    const std::string input_path = "/content/preprocessed_techpartnerfile-ply/RF 000_R0C0_F_Snap3D_part1.ply";
    const std::string output_path = "/content/000002.bin";

    convert_ply(input_path, output_path);
    std::cout << "Conversion completed." << std::endl;

    return 0;
}



