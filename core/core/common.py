from dataclasses import dataclass
from typing import Dict


@dataclass
class DecodedDmtxData:
    """Data class to store the decoded DataMatrix image."""

    raw_x: list
    raw_y: list
    fit_x: list
    fit_y: list
    color: list
    dmtx_size_row: int
    dmtx_size_col: int


def convert_to_module_x_y(
    fit_x: list, fit_y: list, color: list, size_x: int, size_y: int
):
    """Convert raw x, y coordinates to module x, y coordinates

    Args:
        raw_x (list): list of x coordinates of the modules
        raw_y (list): list of y coordinates of the modules
        color (list): list of color magnitude of the modules
        size_x (int): width of the matrix
        size_y (int): height of the matrix

    Returns:
        dict: key (tuple): (x, y) coordinates of the module,
                value (list): list of [x, y, color] of the module
    """
    module_x_y = {
        (i, j): []
        for i in range(-1, size_x + 1)
        for j in range(-1, size_y + 1)
    }

    for i in range(len(fit_x)):
        if (
            fit_x[i] < 0
            or fit_x[i] > size_x
            or fit_y[i] < 0
            or fit_y[i] > size_y
            or fit_x[i] % 1 == 0
            or fit_y[i] % 1 == 0
        ):
            continue
        module_x_y[(int(fit_x[i]), int(fit_y[i]))].append(
            [fit_x[i], fit_y[i], color[i]]
        )
    return module_x_y


def compute_module_intensity(
    module_x_y: Dict[tuple, list], size_x: int, size_y: int
) -> (int, int, float, Dict[tuple, float]):
    """Compute module intensity of the entire matrix

    Args:
        module_x_y (dict): key (tuple): (x, y) coordinates of the module,
        size_x (int): width of the matrix
        size_y (int): height of the matrix

    Returns:
        int: minimum intensity of the entire matrix
        int: maximum intensity of the entire matrix
        float: global threshold of the entire matrix


    """
    module_average = {}
    for i in range(-1, size_x + 1):
        for j in range(-1, size_y + 1):
            module_average[(i, j)] = 0

    # Calculate MOD for each module and determine the grade
    for key in module_x_y:
        if key[0] > -1 and key[1] > -1 and key[0] < size_x and key[1] < size_y:
            if len(module_x_y[key]) != 0:
                module_average[key] = sum(
                    [x[2] for x in module_x_y[key]]
                ) / len(module_x_y[key])

    # remove empty modules
    module_average = {
        key: module_average[key]
        for key in module_average
        if len(module_x_y[key]) != 0
    }
    min_intensity = min(module_average.values())
    max_intensity = max(module_average.values())
    global_threshold = (min_intensity + max_intensity) / 2

    return min_intensity, max_intensity, global_threshold, module_average


def get_modulation_attributes(
    decoded_data: DecodedDmtxData,
) -> (Dict[tuple, list], Dict[tuple, float], int, float):
    """Get modulation attributes to calculate modulation grade,
        symbol contrast grade

    Args:
        decoded_data (DecodedDmtxData): Decoded DataMatrix data

    Returns:
        Dict[tuple, list]: key (tuple): (x, y) coordinates of the module,
        Dict[tuple, float]: key (tuple): (x, y) color average of the module,
        int: symbol contrast of the entire matrix,
        float: global threshold of the entire matrix
    """
    module_x_y = convert_to_module_x_y(
        decoded_data.fit_x,
        decoded_data.fit_y,
        decoded_data.color,
        decoded_data.dmtx_size_row,
        decoded_data.dmtx_size_col,
    )
    (
        min_intensity,
        max_intensity,
        global_threshold,
        module_average,
    ) = compute_module_intensity(
        module_x_y, decoded_data.dmtx_size_row, decoded_data.dmtx_size_col
    )

    symbol_contrast = max_intensity - min_intensity

    return (module_x_y, module_average, symbol_contrast, global_threshold)
