from pylibdmtx.pylibdmtx import Decoded, decode


class DataMatrixQADecoder:
    """Decoder for data matrix barcode image"""

    def __init__(self) -> None:
        pass

    def decode(self, image, sampling_rate=10) -> list[Decoded]:
        """Decode a Data Matrix barcode image.

        This method takes an image containing a Data Matrix barcode and
        attempts to decode it. The decoding process can be configured
        using the sampling_rate parameter to optimize performance and
        accuracy.

        :param image: The image containing the Data Matrix barcode.
                     Supported formats include PNG and JPEG.
        :type image: any
        :param sampling_rate: Number of pixels per module per axis.
                             Higher values may improve accuracy but
                             decrease performance. Defaults to 10.
        :type sampling_rate: int
        :return: A list of Decoded objects containing the decoded string
                 and coordinates of the barcode.
        :rtype: list[Decoded]
        :raises: Various exceptions from pylibdmtx if decoding fails
        """
        return decode(image=image, sampling_rate=sampling_rate)
