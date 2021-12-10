import colorsys
from typing import Tuple
import cv2
import numpy as np

def print_figure_name(img: np.ndarray, n_vertices: int,
                      position: Tuple[int, int]) -> None:
    fontScale = img.shape[0] / 700
    thickness = max(int(img.shape[0]/300), 1)
    
    if n_vertices == 3:
        cv2.putText(img, 'TRIANGLE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    elif n_vertices == 4:
        cv2.putText(img, 'SQUARE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    elif n_vertices > 10:
        cv2.putText(img, 'CIRCLE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)

    else:
        cv2.putText(img, 'UNEXPECTED FIGURE', position, cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale, (255,255,255), thickness)


def gen_colors(n: int) -> np.ndarray:
    hues = np.linspace(0, 1, n, endpoint=False)
    colors = [colorsys.hsv_to_rgb(h, 1, 0.6) for h in hues]
    return (np.array(colors) * 255).astype(int)


def get_color_for_figure(n_vertices: int) -> Tuple[int, int, int]:
    if n_vertices == 3:
        return (200, 0, 0)

    elif n_vertices == 4:
        return (0, 200, 0)

    elif n_vertices > 10:
        return (0, 0, 200)

    return (70, 70, 70)


def color_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply threshold
    thresholded_im = np.zeros(img.shape[:2], dtype=np.uint8)
    thresholded_im[gray>100] = 255

    contours, _ = cv2.findContours(thresholded_im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    colors = gen_colors(len(contours))

    for i, contour in enumerate(contours):
        # find positions of vertices to count them
        # we need some value to estimate approximation accuracy - let it be perimeter
        object_perimeter = cv2.arcLength(contour, closed=True)
        approx = cv2.approxPolyDP(contour, epsilon=object_perimeter/150, closed=True)
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
        color = colors[i].tolist()
        color = get_color_for_figure(n_vertices)
        cv2.fillPoly(img, pts=[contour], color=color)
        
        # subscribe the figure
        print_figure_name(img, n_vertices, (x,y))
    return img

if __name__ == '__main__':
    img = cv2.imread('~/test_figures.jpg')  
    colored = color_image(img)
    cv2.imshow('Colored Figures', colored)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
