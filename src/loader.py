import os.path

import cv2
import numpy as np
import PyOpenColorIO as OCIO

DNG_COLOUR_SPACE = 'ACES - ACES2065-1'

# XYZ to ACES2065-1
# https://github.com/ampas/aces-dev/blob/master/transforms/ctl/README-MATRIX.md
# https://www.colour-science.org:8010/apps/rgb_colourspace_transformation_matrix?input-colourspace=DCDM+XYZ&output-colourspace=ACES2065-1&chromatic-adaptation-transform=None&formatter=repr&decimals=10
DNG_MATRIX = [[1.0498110175, 0.0000000000, -0.0000974845],
              [-0.4959030231, 1.3733130458, 0.0982400361],
              [0.0000000000, 0.0000000000, 0.9912520182]]


def getOcioConfig():
    ocio_path = os.path.dirname(__file__) + "/../ocio/config.ocio"
    if not os.path.exists(ocio_path):
        raise RuntimeError(f"embedded OCIO config file not found at {ocio_path}.")

    return OCIO.Config.CreateFromFile(ocio_path)


def convertColourSpace(img, timeline_colour_space):
    config = getOcioConfig()
    in_colour = config.getColorSpace(timeline_colour_space)
    out_colour = config.getColorSpace(DNG_COLOUR_SPACE)
    processor = config.getProcessor(in_colour, out_colour)
    cpu = processor.getDefaultCPUProcessor()
    cpu.applyRGB(img)

    return img


def loadImage(path, timeline_colour_space=None):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if not img.dtype == np.uint16:
        raise RuntimeError(f"Image {path} is not 16 bit")

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_float = img2.astype(np.float32) / 65535.0

    if timeline_colour_space is not None:
        return convertColourSpace(img_float, timeline_colour_space)
    else:
        return img_float
