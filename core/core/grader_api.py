from datetime import datetime

from datamatrixqa.core.common import DecodedDmtxData
from datamatrixqa.core.grader_factory import DataMatrixGraderFactory
from datamatrixqa.core.graders.modulation_grader import ModulationGrader
from datamatrixqa.core.graders.symbol_grader import SymbolContrastGrader
from datamatrixqa.reader.nn_decoder import DataMatrixNNDecoder


class DataMatrixGradeAPI:
    """
    API for grading Data Matrix codes.

    This class provides a simplified interface for grading Data Matrix codes
    using various grading methods. It uses the factory pattern to create
    appropriate graders based on the requested grade type.

    Attributes:
        factory (DataMatrixGraderFactory): Factory for creating graders.
    """

    def __init__(self):
        """Initialize the grading API with a factory and
        register available graders."""
        self.factory = DataMatrixGraderFactory()
        self._register_graders()

    def _register_graders(self):
        """Register all available graders with the factory."""
        self.factory.register_grader("modulation", ModulationGrader)
        self.factory.register_grader("symbol_contrast", SymbolContrastGrader)

    def _decode_image(self, image_path: str) -> DecodedDmtxData:
        """Decode the image using the neural network decoder

        Args:
            image_path (str): Path to the image to decode

        Returns:
            DecodedDmtxData: Decoded DataMatrix image data
        """
        # Create timestamp for image being processed
        timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S-%f")
        decoder = DataMatrixNNDecoder(
            sampling_rate=10,
            onnx_model=None,
        )
        decoded_dmtx_img, nn_used, input_image = decoder.decode_image(
            image_path
        )

        (
            raw_x,
            raw_y,
            fit_x,
            fit_y,
            color,
            uec,
            dmtx_size_row,
            dmtx_size_col,
        ) = decoder.process_pixels(
            decoded_dmtx_img, nn_used, input_image, timestamp
        )
        return DecodedDmtxData(
            raw_x=raw_x,
            raw_y=raw_y,
            fit_x=fit_x,
            fit_y=fit_y,
            color=color,
            dmtx_size_row=dmtx_size_row,
            dmtx_size_col=dmtx_size_col,
        )

    def grade_datamatrix(
        self, image_path: str, grade_type: str, explain: bool = False
    ):
        """
        Grade a data matrix image

        Args:
            image_path (str): Path to the data matrix image
            grade_type (str): Type of grading to perform
        Returns:
            tuple: Grading results

        Raises:
            ValueError: If the specified grade_type is not registered.
            FileNotFoundError: If the image file does not exist.Raises:
        """
        # Get the appropriate grader
        grader = self.factory.get_grader(grade_type)

        decoded_data = self._decode_image(image_path)

        grade = grader.compute_grade(decoded_data)
        if explain:
            explain_grade = grader.explain_grade(decoded_data)
        else:
            explain_grade = None

        return (grade, explain_grade)
