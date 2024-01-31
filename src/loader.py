import cv2
import numpy as np
import PyOpenColorIO as OCIO

# DNG_COLOUR_SPACE = "Utility - XYZ - D60"
# DNG_COLOUR_SPACE = "Utility - Linear - rec.709"

DNG_COLOUR_SPACE = 'ACES - ACES2065-1'

#https://www.colour-science.org:8010/apps/rgb_colourspace_transformation_matrix?input-colourspace=DCDM+XYZ&output-colourspace=ARRI+Wide+Gamut+4&chromatic-adaptation-transform=CAT02&formatter=repr&decimals=10
#DCDM XYZ to ACES2065-1
DNG_MATRIX = [[ 1.4652841412, -0.3164934342, -0.1487907070],
       [-0.5139051082,  1.4065965188,  0.1073085894],
       [ 0.0007037509,  0.0009869408,  0.9983093083]]

def getOcioConfig():
    return OCIO.Config.CreateFromFile(r"O:\utils\openimageio\ocio\config.ocio")


def convertColourSpace(img, timeline_colour_space):
    print(timeline_colour_space)
    print("to:")
    print(DNG_COLOUR_SPACE)

    config = getOcioConfig()
    in_colour = config.getColorSpace(timeline_colour_space)
    out_colour = config.getColorSpace(DNG_COLOUR_SPACE)
    processor = config.getProcessor(in_colour, out_colour)
    cpu = processor.getDefaultCPUProcessor()
    cpu.applyRGB(img)
    print(f"max pixel value: {img.max()}")

    return img


def loadImage(path, timeline_colour_space=None):
    img = cv2.imread(path)

    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img2 = img[:, :, ::-1]  # swap BGR to RGB

    img_float = img2.astype(np.float32) / 255.0

    if timeline_colour_space is not None:
        return convertColourSpace(img_float, timeline_colour_space)
    else:
        return img_float

