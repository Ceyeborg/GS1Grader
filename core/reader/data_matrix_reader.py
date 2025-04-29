import cv2
from cv2.typing import MatLike


class DataMatrixQAReader:
    """Datamatrix image reader using opencv library"""

    def __init__(self) -> None:
        pass

    def read(self, filename: str) -> MatLike:
        """Read a DataMatrix image from a file.

        This method uses OpenCV's imread function to load an image from the
        specified file path. The image is returned as a MatLike object which
        contains the image data in a format compatible with OpenCV operations.

        :param filename: The path to the image file to be read.
        :type filename: str
        :return: An OpenCV MatLike object containing the image data.
        :rtype: MatLike

        :Example:

            >>> reader = DataMatrixQAReader()
            >>> image = reader.read("datamatrix.png")
        """
        return cv2.imread(filename=filename)
