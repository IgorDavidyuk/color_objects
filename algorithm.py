import colorsys
from pathlib import Path
from typing import Tuple, Union
import cv2
import numpy as np

def print_figure_name(img: np.ndarray, n_vertices: int,
                      position: Tuple[int, int]) -> None:
    """
    Puts the figure name on an image.

    parameters:
        img - image with figures to print text on
        n_vertices - number of vertices in the shape
        position - position of left bottom point of the text line

    output:
        the image with printed text
    """

    fontScale = img.shape[0] / 700
    thickness = max(int(img.shape[0]/300), 1)
    
    if n_vertices == 3:
        cv2.putText(img, 'TRIANGLE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    elif n_vertices == 4:
        cv2.putText(img, 'SQUARE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    elif n_vertices >= 10:
        cv2.putText(img, 'CIRCLE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    else:
        cv2.putText(img, 'UNEXPECTED FIGURE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)


def gen_colors(n: int) -> np.ndarray:
    """Generates n unique equidistant colors using HSV color system."""
    hues = np.linspace(0, 1, n, endpoint=False)
    colors = [colorsys.hsv_to_rgb(h, 1, 0.6) for h in hues]
    return (np.array(colors) * 255).astype(int)


def get_color_for_figure(n_vertices: int) -> Tuple[int, int, int]:
    """Returns an RBG color tuple depending on the number of vertices."""
    if n_vertices == 3:
        return (200, 0, 0)

    elif n_vertices == 4:
        return (0, 200, 0)

    elif n_vertices >= 10:
        return (0, 0, 200)

    return (70, 70, 70)


def color_image(img: np.ndarray, unique_colors=True, threshold=100,
                approximation_accuracy=150) -> np.ndarray:
    """
    This function detects simple shapes in the image and colors them.

    Detected figures will be also subscribed in the final image. The function
    can detect triangles, quadrilateral, and circles; any other figure will be
    marked "UNEXPECTED".

    The algorithm uses OpenCV to find contours on a grayscale version of
    the image. Then it uses a polygon approximation algorithm to reduce the
    number of vertices in contours. The resulted polygons are used to identify
    and color figures in the image.

    parameters:
        img - image with figures to color
        unique_colors - flag to color all figures in unique colores
            independent of the number of vertices. The default behavior is
            coloring all the figures of the same type in one color
        threshold - background threshold for a grayscale image, using that
            the algo will separate figures from the background
        approximation_accuracy - accuracy of polygon approximation for
            detected contours

    output:
        the image with colored and subscribed figures
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply threshold
    thresholded_im = np.zeros(img.shape[:2], dtype=np.uint8)
    thresholded_im[gray>threshold] = 255

    contours, _ = cv2.findContours(thresholded_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if unique_colors:
        colors = gen_colors(len(contours))

    for i, contour in enumerate(contours):
        # find positions of vertices to count them
        # we need some value to estimate approximation accuracy - let it be perimeter
        object_perimeter = cv2.arcLength(contour, closed=True)
        approx = cv2.approxPolyDP(contour, epsilon=object_perimeter/approximation_accuracy,
                                  closed=True)
        n_vertices = len(approx)
        
        # find object centers
        # M = cv2.moments(contour)
        x, y = approx.squeeze().mean(axis=0).astype(int)
        # offset to the left for x
        x = (x + 2*approx[:,0,0].min()) // 3
        
        # COLORING PART
        # highlight contours
        cv2.drawContours(img, [contour], 0, (255, 255, 255), 4)
        # fill the object
        if unique_colors:
            color = colors[i].tolist()
        else:
            color = get_color_for_figure(n_vertices)
        cv2.fillPoly(img, pts=[contour], color=color)
        
        # subscribe the figure
        print_figure_name(img, n_vertices, (x,y))

    return img


def read_image(path: Union[Path, str]) -> np.ndarray:
    """This function reads image from disk."""
    path = Path(path).absolute()
    return cv2.imread(str(path))


def show_image(img: np.ndarray) -> None:
    """Function uses OpenCV to show the image in a window."""
    cv2.imshow('Colored Figures', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    img =  read_image('./test_figures.jpg')
    colored = color_image(img)
    show_image(colored)