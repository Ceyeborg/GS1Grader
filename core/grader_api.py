from core.grader_factory import DataMatrixGraderFactory
from core.graders.modulation_grader import ModulationGrader
from core.graders.symbol_grader import SymbolContrastGrader
from datamatrixqa.reader.nn_decoder import DataMatrixNNDecoder

class DataMatrixGradeAPI:
    def __init__(self):
        self.factory = DataMatrixGraderFactory()
        self._register_graders()
    
    def _register_graders(self):
        """
            Register GS1 graders

            - Modulation
            - Symbol Contrast
        """
        self.factory.register_grader("modulation", ModulationGrader)
        self.factory.register_grader("symbool_contrast", SymbolContrastGrader)

    def _decode_image(self, image_path: str):
        """
            Decode image using dmtxlib
        """
        decoder = DataMatrixNNDecoder(sampling_rate=10)

        decoded_dmtx_img, nn_used, input_image = decoder.decode_image(image_path)

        
    
    def grade_datamatrix(self, image_path: str, grade_type: str = "modulation", explain: bool = False):
        """
        Grade a data matrix image
        
        Args:
            image_path (str): Path to the data matrix image
            grade_type (str): Type of grading to perform
        Returns:
            dict: Grading results
        """
        # Get the appropriate grader
        grader = self.factory.get_grader(grade_type)
        
        # Use existing decoder to get image data
        decoded_data = self._decode_image(image_path)
        
        # Process and prepare data for grading
        processed_data = self._prepare_data(decoded_data)

        grade = grader.compute_grade(processed_data)
        if explain:
            explain_grade = grader.explain_grade(processed_data)
        else:
            explain_grade = None
        
        # Compute grade
        return grade, explain_grade
