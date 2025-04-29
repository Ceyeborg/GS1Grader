from dataclasses import dataclass
from typing import Dict


@dataclass
class DecodedDmtxData:
    """Data class to store the decoded DataMatrix image.

    :param raw_x: List of raw x coordinates
    :type raw_x: list
    :param raw_y: List of raw y coordinates
    :type raw_y: list
    :param fit_x: List of fitted x coordinates
    :type fit_x: list
    :param fit_y: List of fitted y coordinates
    :type fit_y: list
    :param color: List of color values for each module
    :type color: list
    :param dmtx_size_row: Number of rows in the DataMatrix
    :type dmtx_size_row: int
    :param dmtx_size_col: Number of columns in the DataMatrix
    :type dmtx_size_col: int
    """

    raw_x: list
    raw_y: list
    fit_x: list
    fit_y: list
    color: list
    dmtx_size_row: int
    dmtx_size_col: int


@dataclass
class ModulationAttributes:
    """Data class to store modulation attributes for DataMatrix grading.

    :param module_x_y: Dictionary mapping (x,y) module coordinates to
    their pixel data
    :type module_x_y: Dict[tuple, list]
    :param module_average: Dictionary mapping (x,y) module coordinates
    to their average color values
    :type modulation_average: Dict[tuple, float]
    :param symbol_contrast: The contrast between light and dark modules
    in the DataMatrix
    :type symbol_contrast: int
    :param global_threshold: The global threshold value used for module
    classification
    :type global_threshold: float
    """

    module_x_y: Dict[tuple, list]
    module_average: Dict[tuple, float]
    symbol_contrast: float
    global_threshold: float


def convert_to_module_x_y(
    fit_x: list, fit_y: list, color: list, size_x: int, size_y: int
):
    """Convert raw x, y coordinates to module x, y coordinates

    This function maps the raw coordinates to their corresponding
    module positions in the DataMatrix and associates color values
    with each module.

    :param fit_x: List of x coordinates of the modules
    :type fit_x: list
    :param fit_y: List of y coordinates of the modules
    :type fit_y: list
    :param color: List of color magnitude values of the modules
    :type color: list
    :param size_x: Width of the matrix in modules
    :type size_x: int
    :param size_y: Height of the matrix in modules
    :type size_y: int

    :return: Dictionary mapping module coordinates to their
    pixel data
    :rtype: dict
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
) -> (float, float, float, Dict[tuple, float]):
    """Compute module intensity of the entire matrix

    This function calculates the average intensity for each module
    in the DataMatrix and determines the minimum, maximum intensity
    values and global threshold.

    :param module_x_y: Dictionary mapping (x,y) coordinates to lists
    of pixel data
    :type module_x_y: Dict[tuple, list]
    :param size_x: Width of the matrix in modules
    :type size_x: int
    :param size_y: Height of the matrix in modules
    :type size_y: int

    :return: A tuple containing minimum intensity, maximum intensity,
            global threshold, and a dictionary of module average
            intensities
    :rtype: tuple(int, int, float, Dict[tuple, float])
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
) -> ModulationAttributes:
    """Get modulation attributes to calculate modulation grade
    and symbol contrast grade.

    This function processes decoded DataMatrix data to extract
    various attributes needed for calculating modulation and
    symbol contrast grades. It converts pixel coordinates to
    module coordinates and computes intensity values across the matrix.

    :param decoded_data: Decoded DataMatrix data containing fit
                        coordinates, color values, and matrix dimensions
    :type decoded_data: DecodedDmtxData
    :return: A ModulationAttributes object containing:
             - module_x_y: Dictionary mapping (x,y) module coordinates
                to lists of pixel data
             - module_average: Dictionary mapping (x,y) module coordinates
                to average color values
             - symbol_contrast: The difference between maximum and
                minimum intensity in the matrix
             - global_threshold: The average of minimum and maximum
                intensity values
    :rtype: ModulationAttributes
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

    return ModulationAttributes(
        module_x_y=module_x_y,
        module_average=module_average,
        symbol_contrast=symbol_contrast,
        global_threshold=global_threshold,
    )


def map_raw_fit_x_y(decoded_data: DecodedDmtxData) -> Dict[tuple, tuple]:
    """Map the raw x, y coordinates to the fit x, y coordinates.

    This function creates a mapping between the fitted coordinates
    (processed/corrected) and the raw coordinates (original) from the
    decoded DataMatrix data.

    :param decoded_data: Decoded DataMatrix data containing raw
                        and fit coordinates
    :type decoded_data: DecodedDmtxData
    :return: Dictionary mapping fitted coordinates to raw coordinates
    :rtype: Dict[tuple, tuple]
    """
    map_raw_fit_x_y = {}
    assert (
        len(decoded_data.raw_x)
        == len(decoded_data.raw_y)
        == len(decoded_data.fit_x)
        == len(decoded_data.fit_y)
    ), "length of raw_x, raw_y, fit_x, fit_y must be the same"
    for i in range(len(decoded_data.raw_x)):
        map_raw_fit_x_y[
            (round(decoded_data.fit_x[i], 1), round(decoded_data.fit_y[i], 1))
        ] = (
            decoded_data.raw_x[i],
            decoded_data.raw_y[i],
        )

    return map_raw_fit_x_y
