import argparse
from pathlib import Path
from algorithm import color_image, read_image, show_image


def main() -> None:
    parser = argparse.ArgumentParser(description="A Script Coloring Figures")
    parser.add_argument(
        "-i",
        "--image-path",
        type=lambda p: Path(p).absolute(),
        required=True,
        help="Path to an image with figures",
    )
    parser.add_argument(
        "-u",
        "--unique-colors",
        help="Use unique equidistant colors for figures",
        action="store_true"
    )
    parser.add_argument(
        '-t',
        '--grayscale-threshold',
        type=int,
        help="Background threshold for grayscale picture. Default is 100",
        default=100
    )
    parser.add_argument(
        '-a',
        '--approx-accuracy',
        type=int,
        help="Poligon approximation accuracy. Default is 150",
        default=150
    )

    args = parser.parse_args()

    thresh = args.grayscale_threshold
    if thresh < 0:
        raise ValueError("The grayscale threshold is smaller than minimum uint8 value.")
    if thresh > 255:
        raise ValueError("The grayscale threshold is bigger than maximum uint8 value.")
    if thresh < 10:
        print("\nWARNING!\nThe grayscale threshold is too small. Try values between 10 and 245.")
    if thresh > 245:
        print("\nWARNING!\nThe grayscale threshold is too big. Try values between 10 and 245.")

    approx_acc = args.approx_accuracy
    if approx_acc < 1:
        raise ValueError("The Poligon approximation accuracy is too small.")
    if approx_acc < 90:
        print("\nWARNING!\nThe Poligon approximation accuracy is too low."
              "Values smaller than 90 may result in circle detection failure.\n")
    if approx_acc > 800:
        print("\nWARNING!\nThe Poligon approximation accuracy is too high. "
              "Values greater than 800 may result in triangle detection failure.\n")

    image = read_image(args.image_path)
    modified_image = color_image(image, args.unique_colors, threshold=thresh,
                                 approximation_accuracy=approx_acc)
    show_image(modified_image)


if __name__ == '__main__':
    main()