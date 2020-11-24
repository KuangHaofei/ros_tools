# ros_tools
nice ros tools for myself

## setup
- Python: Anaconda
```shell script
conda create --name ros_env python=3
conda activate ros_env
pip install catkin-tools rospkg
pip install pycryptodomex gnupg
pip install tqdm

conda install numpy scipy matplotlib
pip install opencv-python
```


## Normal Function Package
- videos to bag file (python)
    - launch file: `ros_tools/normal_function/launch/video2bag.launch`
    - script file: `ros_tools/normal_function/scripts/video2bag.py`