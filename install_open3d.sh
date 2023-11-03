#!/bin/bash

# Update package list
sudo apt-get update

# Install required packages
sudo apt-get install -y libgl1-mesa-dev libglu1-mesa-dev libxrandr-dev libxinerama-dev libxcursor-dev libc++-13-dev libc++abi-13-dev libx11-dev libxrandr-dev libxi-dev libxxf86vm-dev libxinerama-dev libxcursor-dev libxinerama-dev


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
