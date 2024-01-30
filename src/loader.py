import cv2
import numpy as np
import PyOpenColorIO as OCIO

DNG_COLOUR_SPACE = "Utility - XYZ - D60"
# DNG_COLOUR_SPACE = "Utility - Linear - sRGB"


def getOcioConfig():
    return OCIO.Config.CreateFromFile(r"O:\utils\openimageio\ocio\config.ocio")


def convertColourSpace(img, timeline_colour_space, max_range=255.0):
    config = getOcioConfig()
    in_colour = config.getColorSpace(timeline_colour_space)
    out_colour = config.getColorSpace(DNG_COLOUR_SPACE)
    processor = config.getProcessor(in_colour, out_colour)
    cpu = processor.getDefaultCPUProcessor()
    # print(img.max())
    # print(img.min())
    original_image_float32 = img.astype(np.float32) / max_range
    cpu.applyRGB(original_image_float32)
    print(original_image_float32.max())
    # return original_image_float32

    #TODO: at this stage this is 16bit int so we need to preserve the highlights by lowering exposure. this will be float one day.
    return (original_image_float32 / original_image_float32.max() * 65535.0).astype(np.uint16)


def loadImage(path, timeline_colour_space):
    img = cv2.imread(path)

    img = convertColourSpace(img, timeline_colour_space)

    return img
