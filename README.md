# Color Simple Figures
Script to locate and color figures in images.

## About
The program detects simple shapes in the image and colors them.

Detected figures will be also subscribed in the output image. The function
can detect triangles, quadrilateral, and circles; any other figure will be
marked "UNEXPECTED".

The algorithm uses OpenCV to find contours on a grayscale version of
the image. Then it uses a polygon approximation algorithm to reduce the
number of vertices in contours. The resulted polygons are used to identify
and color figures in the image.

## Requirements
- python >= 3.6

## Getting Started
First of all, clone the repo and `cd` into the directory.

0. It is recommended to use virtual Python environment:
```
$ python3 -m pip install virtualenv
python3 -m virtualenv env
source env/bin/activate
pip install --upgrade pip
```

1. Install required packages from the repo:
```
$ pip install -r requirements.txt
```

2. Run the script:
```
$ python main.py -i path/to/image
```

## Additional parameters
User may pass parameters to the script:
- `-u` - unique colors flag. Pass to color all figures in unique colores independent of the number of vertices.
The default behavior is coloring all the figures of the same type in one color.
- `-t` - background threshold value for a grayscale image, using that the algo will separate figures from the background.
- `-a` - accuracy of polygon approximation for detected contours.

### TO-DO:
1. run linter
3. generator script
4. tests
6. poetry package