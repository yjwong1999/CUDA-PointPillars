#!/bin/bash

# Clone the Open3D repository
git clone --recursive https://github.com/intel-isl/Open3D.git

# Change directory to the Open3D repository
cd Open3D

# Create a build directory
mkdir build

# Change directory to the build directory
cd build

# Configure the build with CMake
cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=${HOME}/open3d_install ..

# Build and install Open3D with 12 parallel jobs
make install -j 12

# Change back to the original directory
cd ../..
