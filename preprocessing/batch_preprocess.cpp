#include <iostream>
#include <filesystem>
#include <open3d/Open3D.h>
#include <vector>
#include <string>

namespace fs = std::filesystem;

int main(int argc, char** argv) {
    // Get arguments from the user
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " --input-dir <input_folder> --output-dir <output_folder>\n";
        return 1;
    }

    std::string inputDir;
    std::string outputDir;

    for (int i = 1; i < argc; i += 2) {
        std::string arg = argv[i];
        if (arg == "--input-dir") {
            inputDir = argv[i + 1];
        } else if (arg == "--output-dir") {
            outputDir = argv[i + 1];
        } else {
            std::cerr << "Unknown argument: " << arg << "\n";
            return 1;
        }
    }

    // List all files in the input directory
    std::vector<std::string> fileNames;
    for (const auto& entry : fs::directory_iterator(inputDir)) {
        if (entry.path().extension() == ".ply") {
            std::string filePath = entry.path().string();
            std::cout << "Found file: " << filePath << std::endl; // Print the file path
            fileNames.push_back(entry.path().string());
        }
    }

    // Check if the output directory exists, create it if not
    if (!fs::is_directory(outputDir)) {
        fs::create_directory(outputDir);
    } else {
        std::cout << "Apparently, you have preprocessed the input data previously! Please check.\n";
        return 1;
    }

    // Process each .ply file
    for (const std::string& filePath : fileNames) {
        std::string fileName = fs::path(filePath).filename();
        std::string savePath = fs::path(outputDir) / fileName;

        // Read the point cloud
        auto pcd = open3d::io::CreatePointCloudFromFile(filePath);

        // Uniform downsample
        auto uniDownPcd = pcd->UniformDownSample(8);

        // Remove statistical outlier
        auto [cl, ind] = uniDownPcd->RemoveStatisticalOutliers(5, 1.0);
        auto inlierCloud = uniDownPcd->SelectByIndex(ind);


        // Save the filtered point cloud
        open3d::io::WritePointCloud(savePath, *inlierCloud);
        std::cout << "Processed Successfully: " << savePath << std::endl; // Print the file path

    }

    return 0;
}
