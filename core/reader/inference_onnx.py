import math
import os
import shutil
from pathlib import Path

import numpy as np
import onnxruntime
import torch
import torchvision.transforms.v2 as T
from PIL import Image

from datamatrixqa.reader.data_matrix_decoder import DataMatrixQADecoder


def pad_to_target_size(image, target_size=(256, 256), pad_value=255):
    # Get original dimensions
    original_width, original_height = image.size

    # Calculate the amount of padding needed
    pad_left = (target_size[0] - original_width) // 2
    pad_right = target_size[0] - original_width - pad_left
    pad_top = (target_size[1] - original_height) // 2
    pad_bottom = target_size[1] - original_height - pad_top

    # Create a padding transform
    padding_transform = T.Pad(
        padding=(pad_left, pad_top, pad_right, pad_bottom), fill=pad_value
    )

    # Apply the padding transform
    padded_image = padding_transform(image)

    return padded_image, (pad_left, pad_top, pad_right, pad_bottom)


def unpad_array(padded_array, padding):
    pad_left, pad_top, pad_right, pad_bottom = padding

    # Calculate the original dimensions
    original_height = padded_array.shape[2] - (pad_top + pad_bottom)
    original_width = padded_array.shape[3] - (pad_left + pad_right)

    unpadded_array = padded_array[
        :,
        :,
        pad_top : pad_top + original_height,
        pad_left : pad_left + original_width,
    ]

    return unpadded_array


class DataMatrixInference:
    """
    This class is used to perform inference on DMC of variable sizes.
    """

    def __init__(
        self, onnx_model_path, save_images: bool = False, save_dir: str = None
    ):
        self.onnx_model_path = onnx_model_path
        self.save_images = save_images
        self.save_dir = save_dir
        if self.save_images and not self.save_dir:
            raise ValueError(
                "`save_directory` must be provided if `save_images` is True."
            )

        self.totensor = T.Compose(
            [
                T.ToImage(),
                T.ToDtype(torch.float32, scale=True),
            ]
        )

    def pad_to_nearest_multiple_of_32(self, height, width):
        """
        Pad the dimensions of image to the nearest multiple of 32 to
        make the inference via unet work
        """

        padded_height = math.ceil(height / 32) * 32
        padded_width = math.ceil(width / 32) * 32
        return padded_height, padded_width

    def preprocess(self, image_path):
        "Reads the image and transforms to a model usable input"

        image = Image.open(image_path).convert("RGB")
        original_height, original_width = image.size
        padded_height, padded_width = self.pad_to_nearest_multiple_of_32(
            original_height, original_width
        )
        log(f"Original size: {image.size}", 0)
        image, padding_info = pad_to_target_size(
            image, target_size=(padded_height, padded_width)
        )
        log(f"Padded image size: {image.size}", 0)
        image_tensor = self.totensor(image)

        image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension

        input_array = image_tensor.cpu().numpy().astype(np.float32)

        return input_array, padding_info

    def infer(self, input_array: np.ndarray):
        assert input_array.shape[0] == 1, "Currently works on batch_size=1"

        ort_session = onnxruntime.InferenceSession(self.onnx_model_path)
        ort_inputs = {ort_session.get_inputs()[0].name: input_array}
        ort_outs = ort_session.run(None, ort_inputs)

        output_array = (
            ort_outs[0] * 255
        )  # converting sigmoid outputs to [0,255]
        return output_array

    def postprocess(self, input_array, output_array, padding_info):
        """
        Removes padding and returns the original size inputs and
        reconstructed outputs
        """

        input_array = unpad_array(input_array, padding_info)
        output_array = unpad_array(output_array, padding_info)

        input_array = (input_array * 255).astype(
            np.uint8
        )  # mul by 255 since the range is between [0 1]
        output_array = output_array.astype(np.uint8)

        assert input_array.shape == output_array.shape

        return input_array, output_array

    @timer
    def model_inference(self, input_image_path: str):
        """
        Perform model inference on an input image over the ONNX model.

        This method preprocesses the input image and performs inference
        using the specified ONNX model.
        It returns both the input image and the output of
        the model inference.
        """

        # if gt_image_path:
        #     return

        resized_input_array, padding_info = self.preprocess(input_image_path)

        output_array = self.infer(input_array=resized_input_array)

        self.input_array, self.output_array = self.postprocess(
            resized_input_array, output_array, padding_info
        )

        assert self.input_array.shape == self.output_array.shape

        if self.save_images:
            self.save_as_png_image(self.input_array, "inputs", image_path.stem)
            self.save_as_png_image(
                self.output_array, "outputs", image_path.stem
            )
        return self.input_array, self.output_array

    def save_as_png_image(
        self, input_array: np.ndarray, save_folder, img_name
    ):
        save_path = self.save_dir / save_folder
        os.makedirs(save_path, exist_ok=True)

        num_images = input_array.shape[0]

        assert num_images == 1, "currently only batch_size=1 is supported"

        for i in range(num_images):
            img_array = input_array[i]
            out_np_array = np.transpose(img_array, (1, 2, 0))
            img = Image.fromarray(out_np_array)
            img.save(f"{save_path}/{img_name}.png")

    def decode_datamatrix(self, input_array: np.ndarray):
        assert (
            input_array.shape[0] == 1
        ), "currently only batch_size=1 is supported "
        decoder = DataMatrixQADecoder()
        dmtx_input = np.transpose(input_array.squeeze(0), (1, 2, 0))

        result = decoder.decode(dmtx_input)
        if len(result) > 0:
            return result[0].data
        else:
            return "Unable to Decode"

    def reconstruct_resized_input_image(self, input_image: np.ndarray):
        """
        Reconstructs the input image to the original size.
        """
        raw_image_reconstructed = {}
        x_size = input_image.shape[1]
        y_size = input_image.shape[0]
        for y in range(y_size - 1, -1, -1):
            for x in range(0, x_size, 1):
                raw_image_reconstructed[(x, y)] = input_image[
                    y, x, 0
                ]  # (y,x) coordinates and all three channeels are same

        return raw_image_reconstructed


