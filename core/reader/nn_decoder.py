import numpy as np

from core.reader.inference_onnx import DataMatrixInference
from core.reader.data_matrix_decoder import DataMatrixQADecoder
from core.reader.data_matrix_reader import DataMatrixQAReader


class DataMatrixNNDecoder:
    def __init__(self, sampling_rate, onnx_model):
        """Initialize the neural network decoder."""
        self.sampling_rate = sampling_rate
        self.onnx_model = onnx_model
        self.output_path = output_path
        self.save_plots = save_plots
        self.dmtx_reader = DataMatrixQAReader()
        self.dmtx_decoder = DataMatrixQADecoder()
        self.dmtx_inference = DataMatrixInference(
            onnx_model_path=self.onnx_model
        )

    def decode_image(self, image_file_name):
        """Decode a DataMatrix image using traditional and neural network
        methods.

        Args:
            image_file_name (str): The file name of the image to decode.

        Returns:
            tuple: A tuple containing the decoded DataMatrix image, a boolean
            indicating if neural network was used, and the resized input image
            if neural network was used.
        """

        dmtx_img = self.dmtx_reader.read(filename=image_file_name)

        decoded_dmtx_image = self.dmtx_decoder.decode(
            image=dmtx_img, sampling_rate=self.sampling_rate
        )

        if decoded_dmtx_image is None or len(decoded_dmtx_image) == 0:
            (
                resized_input_image,
                reconstructed_image,
            ) = self.dmtx_inference.model_inference(
                input_image_path=image_file_name
            )
            input_reconstructed_image = np.transpose(
                reconstructed_image.squeeze(0), (1, 2, 0)
            )
            resized_input_image = np.transpose(
                resized_input_image.squeeze(0), (1, 2, 0)
            )
            decoded_dmtx_image = self.dmtx_decoder.decode(
                input_reconstructed_image, sampling_rate=self.sampling_rate
            )
            return decoded_dmtx_image, True, resized_input_image

        return decoded_dmtx_image, False, None

    def process_pixels(
        self,
        decoded_dmtx_image,
        nn_used,
        resized_input_image,
        timestamp,
    ):
        """Process the pixels of a decoded DataMatrix image and generate
        heatmaps.

        Args:
            decoded_dmtx_image (list): The decoded DataMatrix image.
            nn_used (bool): Whether neural network was used for decoding.
            resized_input_image (np.ndarray): The resized input image if neural
            network was used.
            timestamp (str): Timestamp for the image being processed.

        Returns:
            tuple: A tuple containing raw x and y coordinates, fit x and y
            coordinates, color values, uec grade and the size of the
            DataMatrix in rows and columns.
        """
        pixels_fit = decoded_dmtx_image[0].pixelsFit
        pixels_raw = decoded_dmtx_image[0].pixelsRaw
        dmtx_size_row = int(len(pixels_fit) / self.sampling_rate)
        dmtx_size_col = int(len(pixels_fit[0]) / self.sampling_rate)
        uec = decoded_dmtx_image[0].uec

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

        if nn_used:
            pixel_input = self.dmtx_inference.reconstruct_resized_input_image(
                input_image=resized_input_image
            )
            raw_x_y = list(zip(raw_x, raw_y))
            color = [pixel_input[elem] for elem in raw_x_y]

        if self.save_plots:
            self.generate_heatmaps(
                fit_x,
                fit_y,
                raw_x,
                raw_y,
                color,
                timestamp,
            )

        return (
            raw_x,
            raw_y,
            fit_x,
            fit_y,
            color,
            uec,
            dmtx_size_row,
            dmtx_size_col,
        )

