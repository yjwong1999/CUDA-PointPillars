#!/bin/bash

# Install the spconv with the same version as pytorch and nvcc
pip install spconv-cu118

# Clone the OpenPCDet repository
git clone https://github.com/yjwong1999/OpenPCDet.git
cd OpenPCDet

# Set up OpenPCDet
python setup.py develop

# Install additional dependencies
pip install plyfile
pip install av2
pip install kornia==0.5.8
pip install mayavi
pip install PyQt5

# Move back to the original directory
cd ..
