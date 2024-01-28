import cv2
import numpy as np
from process_raw import DngFile

import PyOpenColorIO as OCIO

# general idea
# load tiff from resolve
# color convert from timeline to linear
# dump data to dng


adobe_example_linear = r"F:\stills\dng_samples\07_PGTM2_float16.dng"
import rawpy

# since dng are compatible with tiff we can use openCV to load some of the example dng files from Adobe
img = cv2.imread(r"F:\stills\dng_samples\01_jxl_linear_raw_integer.dng")
img = cv2.imread(r"F:\stills\dng_samples\02_jxl_linear_raw_float.dng")

# unfotunately openCV only loads the thumbnail ignoring the actual raw data so  if we write it back we get a tiny useless file
cv2.imwrite(r"F:\stills\dng_samples\test_opencv.tiff", img)

# what about hdr files? can lightroom load them?
input_file = r"F:\stills\sample_arriLogC_1.4.1.tif"
img = cv2.imread(input_file)
# cv2.imwrite(r"F:\stills\dng_samples\test_hdr.hdr", img)


# raw = rawpy.imread(adobe_example_linear)
# print(dir(raw))
# print(raw.sizes)
# print(raw.raw_type)
# print(raw)
#
# print(dir(rawpy))


timeline_colour_space = "Input - Arri - Curve - V3 LogC (EI800)"
input_file = r"F:\stills\sample_arriLogC_8bit.tif"
output_file = r"F:\stills\test.dng"

config = OCIO.Config.CreateFromFile(r"O:\utils\openimageio\ocio\config.ocio")

in_colour = config.getColorSpace(timeline_colour_space)
out_colour = config.getColorSpace("Utility - Linear - sRGB")  # TODO: find better space with wider gamut

# out_colour = config.getColorSpace("Output - sRGB")  # TODO: find better space with wider gamut

processor = config.getProcessor(in_colour, out_colour)
# processor = config.getProcessor(OCIO.ROLE_COMPOSITING_LOG,
#                                    OCIO.ROLE_SCENE_LINEAR)


cpu = processor.getDefaultCPUProcessor()

# img = cv2.imread(input_file)
# print(img.shape)
# print(type(img))

# print(img)

# Apply the color transform to the existing RGBA pixel data

original_image_float32 = img.astype(np.float32)  /  255.0

cpu.applyRGB(original_image_float32)
converted_image = (original_image_float32*255.0*255.0).astype(np.uint16)

cv2.imwrite(r"F:\stills\test_16bit.tif", converted_image)

# Download raw.dng for test:
# wget https://github.com/yl-data/yl-data.github.io/raw/master/2201.process_raw/raw-12bit-GBRG.dng


# dng = DngFile.read(dng_path)
# raw = dng.raw  # np.uint16
# raw_8bit = np.uint8(raw >> (dng.bit-8))
# cv2.imwrite("c:/temp/raw_8bit.png", raw_8bit)

# rgb1 = dng.postprocess()  # demosaicing by rawpy
# cv2.imwrite("c:/temp/rgb1.jpg", rgb1[:, :, ::-1])
# rgb2 = dng.demosaicing(poww=0.3)  # demosaicing with gamma correction
# cv2.imwrite("c:/temp/rgb2.jpg", rgb2[:, :, ::-1])

# raw = np.uint16([[[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
# print(raw.shape)
# DngFile.save(output_file, converted_image, bit=16)
# from rawpy.enhance import Enhance
