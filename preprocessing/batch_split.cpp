#include <open3d/Open3D.h>
#include <iostream>
#include <string>
#include <vector>
#include <filesystem>
#include <algorithm>
#include <armadillo>

namespace fs = std::filesystem;

int main(int argc, char *argv[]) {
    // Parse command line arguments
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " --ply_dir PLY_DIR" << std::endl;
        return 1;
    }
    std::string ply_dir = argv[2];

    // Get list of .ply files in the input directory
    std::vector<std::string> file_names;
    for (const auto &entry : fs::directory_iterator(ply_dir)) {
        if (entry.path().extension() == ".ply") {
            file_names.push_back(entry.path().filename());
        }
    }
    std::sort(file_names.begin(), file_names.end());

    // Check if the data has already been split
    if (file_names[0].find("part1") != std::string::npos || file_names[0].find("part2") != std::string::npos) {
        std::cout << "Apparently, you have split the preprocessed data previously! Please check" << std::endl;
    } else {
        // Process each .ply file
        for (const std::string &file_name : file_names) {

            // Construct file paths
            fs::path file_path = fs::path(ply_dir) / file_name;
            fs::path save_path_1 = fs::path(ply_dir) / (fs::path(file_name).stem().string() + "_part1.ply");
            fs::path save_path_2 = fs::path(ply_dir) / (fs::path(file_name).stem().string() + "_part2.ply");
            std::vector<fs::path> save_paths = {save_path_1, save_path_2};

            std::cout << save_path_1 << std::endl;
            std::cout << save_path_2 << std::endl;


            // Read the point cloud
            auto pcd = open3d::io::CreatePointCloudFromFile(file_path);

            // Get the number of points in the point cloud
            size_t num_points = pcd->points_.size();
            std::cout << "Number of points: " << num_points << std::endl;

            // Convert points to Eigen matrix
            Eigen::MatrixXd points(pcd->points_.size(), 3);
            for (size_t i = 0; i < pcd->points_.size(); ++i) {
                points.row(i) = pcd->points_[i];
            }

            // Convert points to Armadillo matrix
            arma::mat arma_points(pcd->points_.size(), 3);
            for (size_t i = 0; i < pcd->points_.size(); ++i) {
                // Convert Eigen::Vector3d to std::vector
                std::vector<double> point_vec(3);
                for (int j = 0; j < 3; ++j) {
                    point_vec[j] = pcd->points_[i][j];
                }

                // Convert std::vector to arma::rowvec
                arma_points.row(i) = arma::conv_to<arma::rowvec>::from(point_vec);
            }

            // Print the shape of arma_points
            std::cout << "Shape of arma_points: " << arma_points.n_rows << " rows x " << arma_points.n_cols << " columns" << std::endl;


            // Split points into two parts based on x-coordinate
            double x_range = 5.13;
            double x_mid_thresh = x_range / 2;
            double x_min_thresh = 0.23;
            double x_max_thresh = 0.77;

            arma::uvec part_1_indices = arma::find(arma_points.col(0) > x_mid_thresh && arma_points.col(0) < x_max_thresh * x_range);
            arma::mat part_1 = arma_points.rows(part_1_indices);
            part_1.col(0) -= x_mid_thresh;

            arma::uvec part_2_indices = arma::find(arma_points.col(0) <= x_mid_thresh && arma_points.col(0) > x_min_thresh * x_range);
            arma::mat part_2 = arma_points.rows(part_2_indices);
            part_2.col(0) -= x_min_thresh * x_range;

            std::vector<arma::mat> inlier_cloud_nps = {part_1, part_2};

            // Print out the shape of part_1 and part_2
            std::cout << "part_1 has " << part_1.n_rows << " rows and " << part_1.n_cols << " columns." << std::endl;
            std::cout << "part_2 has " << part_2.n_rows << " rows and " << part_2.n_cols << " columns." << std::endl;

           for (size_t i = 0; i < inlier_cloud_nps.size(); ++i) {


              auto splitted_pcd = std::make_shared<open3d::geometry::PointCloud>();


              // Convert arma::mat to Eigen::MatrixXd
              Eigen::MatrixXd new_points(inlier_cloud_nps[i].n_rows, inlier_cloud_nps[i].n_cols);
              for (size_t j = 0; j < inlier_cloud_nps[i].n_rows; ++j) {
                  for (size_t k = 0; k < inlier_cloud_nps[i].n_cols; ++k) {
                      new_points(j, k) = inlier_cloud_nps[i](j, k);
                  }
              }

              // Pass xyz to Open3D.o3d.geometry.PointCloud
              splitted_pcd->points_.resize(new_points.rows());
              for (int j = 0; j < new_points.rows(); ++j) {
                  splitted_pcd->points_[j] = new_points.row(j);
              }


              // Save the point cloud
              open3d::io::WritePointCloud(save_paths[i], *splitted_pcd);



            }


        // Remove original .ply file
        std::cout <<  file_path << " is deleted " << std::endl;
        fs::remove(file_path);


        }


    }

    return 0;
}


