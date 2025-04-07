from pylibdmtx.pylibdmtx import Decoded, decode


class DataMatrixQADecoder:
    """Decoder for 2d barcode image"""

    def __init__(self) -> None:
        pass

    def decode(self, image, sampling_rate=10) -> list[Decoded]:
        """Decodes 2d barcode image

        :param image: image in PNG, JPEG formats
        :type image: any
        :param sampling_rate: Number of pixels per module per axis(default: 10)
        :type sampling_rate: int
        :return: list of Decoded object contains decoded string and coordinates
        :rtype: list(type[Decoded])
        """
        return decode(image=image, sampling_rate=sampling_rate)
