import argparse
import pathlib
import cv2
from matplotlib import pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--images-path",
        type=str,
        default="referenceData/OcamCalib",
        help="the root directory of the images. the results will be saved in the same directory",
    )
    parser.add_argument("--image-format", type=str, default="jpg")
    parser.add_argument(
        "--chessboard-size",
        type=int,
        nargs=2,
        default=[9, 6],
        help="the size of the chessboard (x, y).",
    )

    return parser.parse_args()


def main(args):
    images = read_images(args.images_path, args.image_format)
    for image in images:
        tag_corners(image, args.chessboard_size)
    pass


def read_images(images_path, image_format):
    image_paths = pathlib.Path(images_path).glob("*.{}".format(image_format))
    images = []
    for path in image_paths:
        image = cv2.imread(str(path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images.append(image)

    return images


def tag_corners(image, chessboard_size):
    fig, ax = plt.subplots()
    ax.imshow(image, cmap="gray")

    class TagSession:
        def __init__(self, chessboard_size):
            self.num_x = chessboard_size[0]
            self.num_y = chessboard_size[1]
            self.current_idx = 0
            self.points = []

        def __call__(self, event):
            if event.button == 1:
                x, y = event.xdata, event.ydata
                if self._is_duplicated_point(x, y):
                    pass

        def _is_duplicated_point(self, x, y):
            for point in self.points:
                if point[0] == x and point[1] == y:
                    return True
            return False

    fig.canvas.mpl_connect("button_press_event", lambda event: print(event))
    plt.show()


if __name__ == "__main__":
    args = parse_args()
    main(args)
