# Motion Tracking
## ***Requirements***  
- Python 3.5 or above
- opencv 4.0 or above
### Create Anaconda env:
```bash
conda create --name "name of env"
```
### Install Requirements by conda or pip After Activate env:
```bash
conda install python
pip install opencv-python

```
## Run:
load video from local file
```python
python MotionTracking.py --input ./videos/video.mp4
``` 

or, fire webcam
```python
python MotionTracking.py --input 0
``` 
change delay (This is an unnecessary parameter, default is 25)
```python
python MotionTracking.py --input ./videos/video.mp4 --delay=30 (any number you want)
```
or
```python
python MotionTracking.py --input 0 --delay=30 (any number you want)
``` 
