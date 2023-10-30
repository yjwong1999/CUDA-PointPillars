# PointPillars Inference with TensorRT

[![Open In Colab](https://colab.research.google.com/drive/18EnBx9ZwBbmqa29NOhTihpvnHWeOne6X?usp=sharing)]


### Prerequisites

To build the pointpillars inference, **TensorRT** with PillarScatter layer and **CUDA** are needed. PillarScatter layer plugin is already implemented as a plugin for TRT in the demo.

## Environments

- Nvidia Jetson Xavier/Orin + Jetpack 5.0
- CUDA 11.4 + cuDNN 8.3.2 + TensorRT 8.4.0

### Compile && Run



```
!python visualize_point_cloud.py --bin_file /path/to/your/point_cloud.bin --pred_file /path/to/your/prediction.txt
```



## References

- [Detecting Objects in Point Clouds with NVIDIA CUDA-Pointpillars](https://developer.nvidia.com/blog/detecting-objects-in-point-clouds-with-cuda-pointpillars/)
- [PointPillars: Fast Encoders for Object Detection from Point Clouds](https://arxiv.org/abs/1812.05784)
