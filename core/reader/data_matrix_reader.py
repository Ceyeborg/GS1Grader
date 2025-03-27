import cv2
from cv2.typing import MatLike



class DataMatrixQAReader:
    """Datamatrix image reader using opencv library"""

    def __init__(self) -> None:
        pass

    def read(self, filename) -> MatLike:
        """Wrapper to openvc imread method

        :param filename: filename to an image
        :type filename: str
        :return: MatLike object that contains image information
        :rtype: MatLike
        """
        return cv2.imread(filename=filename)
