import os.path

import cv2
import numpy as np
import PyOpenColorIO as OCIO

DNG_COLOUR_SPACE = 'ACES - ACES2065-1'

# XYZ to ACES2065-1
# https://github.com/ampas/aces-dev/blob/master/transforms/ctl/README-MATRIX.md
DNG_MATRIX = [[1.0498110175, 0.0000000000, -0.0000974845],
              [-0.4959030231, 1.3733130458, 0.0982400361],
              [0.0000000000, 0.0000000000, 0.9912520182]]


def getOcioConfig():
    return OCIO.Config.CreateFromFile(os.path.dirname(__file__) + "/../ocio/config.ocio")


def convertColourSpace(img, timeline_colour_space):
    config = getOcioConfig()
    in_colour = config.getColorSpace(timeline_colour_space)
    out_colour = config.getColorSpace(DNG_COLOUR_SPACE)
    processor = config.getProcessor(in_colour, out_colour)
    cpu = processor.getDefaultCPUProcessor()
    cpu.applyRGB(img)

    return img


def loadImage(path, timeline_colour_space=None):
    img = cv2.imread(path)

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_float = img2.astype(np.float32) / 255.0

    if timeline_colour_space is not None:
        return convertColourSpace(img_float, timeline_colour_space)
    else:
        return img_float
