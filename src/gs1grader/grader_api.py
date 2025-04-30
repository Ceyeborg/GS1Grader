"""
DataMatrix Grading API Module

This module provides the API for grading Data Matrix codes using various
grading methods. It includes the main API class and supporting functionality.

The module implements a factory pattern to create appropriate graders based
on the requested grade type, allowing for extensibility and separation of
concerns between the API interface and the grading implementations.

See Also:
    - `DataMatrixGraderFactory`: Factory class for creating graders
    - `ModulationGrader`: Grader for modulation quality
    - `SymbolContrastGrader`: Grader for symbol contrast
"""

from gs1grader.common import DecodedDmtxData
from gs1grader.grader_factory import DataMatrixGraderFactory
from gs1grader.graders.axial_non_uniformity_grader import (
    AxialNonUniformityGrader,
)
from gs1grader.graders.fixed_pattern_damage_grader import (
    FixedPatternDamageGrader,
)
from gs1grader.graders.grid_non_uniformity_grader import (
    GridNonUniformityGrader,
)
from gs1grader.graders.modulation_grader import ModulationGrader
from gs1grader.graders.symbol_contrast_grader import SymbolContrastGrader
from gs1grader.graders.uec_grader import UECGrader
from gs1grader.reader.data_matrix_decoder import DataMatrixQADecoder
from gs1grader.reader.data_matrix_reader import DataMatrixQAReader


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
        self.dmtx_reader = DataMatrixQAReader()
        self.dmtx_decoder = DataMatrixQADecoder()
        self._register_graders()

    def _register_graders(self):
        """Register all available graders with the factory."""
        self.factory.register_grader("modulation", ModulationGrader)
        self.factory.register_grader("symbol_contrast", SymbolContrastGrader)
        self.factory.register_grader(
            "axial_non_uniformity", AxialNonUniformityGrader
        )
        self.factory.register_grader(
            "grid_non_uniformity", GridNonUniformityGrader
        )
        self.factory.register_grader(
            "fixed_pattern_damage", FixedPatternDamageGrader
        )
        self.factory.register_grader("uec", UECGrader)

    def _decode_image(
        self, image_path: str, sampling_rate: int = 10
    ) -> DecodedDmtxData:
        """Decode the image using the neural network decoder.

        :param image_path: Path to the image to decode
        :param sampling_rate: Sampling rate for decoding, defaults to 10
        :return: Decoded DataMatrix image data
        :rtype: DecodedDmtxData
        """
        dmtx_img = self.dmtx_reader.read(filename=image_path)

        decoded_dmtx_image = self.dmtx_decoder.decode(
            image=dmtx_img, sampling_rate=sampling_rate
        )

        if decoded_dmtx_image is None or len(decoded_dmtx_image) == 0:
            print(
                "Decoding failed due to sub-standard input \
                Checkout our advanced GS1Grader to avail grade using \
                neural network"
            )

        pixels_fit = decoded_dmtx_image[0].pixelsFit
        pixels_raw = decoded_dmtx_image[0].pixelsRaw
        dmtx_size_row = int(len(pixels_fit) / sampling_rate)
        dmtx_size_col = int(len(pixels_fit[0]) / sampling_rate)

        raw_x, raw_y, fit_x, fit_y, color = [], [], [], [], []

        for row in pixels_raw:
            for col in row:
                raw_x.append(float(col[0]))
                raw_y.append(float(col[1]))

        for row in pixels_fit:
            for col in row:
                fit_x.append(float(col[0]) * dmtx_size_row)
                fit_y.append(float(col[1]) * dmtx_size_col)
                color.append(int(col[2]))

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
        self, image_path: str, grade_type: str, explanation_path: str = ""
    ):
        """Grade a Data Matrix code image using the specified grading method.

        This function decodes the provided data matrix image and applies
        the specified grading method to evaluate its quality.

        :param image_path: Path to the data matrix image file
        :type image_path: str
        :param grade_type: Type of grading to perform
                            (e.g. modulation, symbol contrast)
        :type grade_type: str
        :param explanation_path: Provide a path to save png of the detailed
                            explanation of the grade
        :type explanation_path: str, optional
        :returns: A tuple containing the grade and explanation (if requested)
        :rtype: tuple

        :raises ValueError: If the specified grade_type is not registered
        :raises FileNotFoundError: If the image file does not exist
        """
        # Get the appropriate grader
        grader = self.factory.get_grader(grade_type)

        decoded_data = self._decode_image(image_path)

        grade = grader.compute_grade(decoded_data)
        if bool(explanation_path):
            explain_grade = grader.explain_grade(
                decoded_data, explanation_path=explanation_path
            )
        else:
            explain_grade = None

        return (grade, explain_grade)
