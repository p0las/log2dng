import cv2
import numpy as np
from process_raw import DngFile

import PyOpenColorIO as OCIO

#load tiff from resolve
#color convert from timeline to linear
#dump data to dng

config = OCIO.GetCurrentConfig()
processor = config.getProcessor(OCIO.ROLE_COMPOSITING_LOG,
                                   OCIO.ROLE_SCENE_LINEAR)
cpu = processor.getDefaultCPUProcessor()

   # Apply the color transform to the existing RGBA pixel data
img = [1, 0, 0, 0]
img = cpu.applyRGBA(img)


# Download raw.dng for test:
# wget https://github.com/yl-data/yl-data.github.io/raw/master/2201.process_raw/raw-12bit-GBRG.dng
dng_path = "F:/stills/dng_samples/04_PGTM2_per_profile.dng"

# dng = DngFile.read(dng_path)
# raw = dng.raw  # np.uint16
# raw_8bit = np.uint8(raw >> (dng.bit-8))
# cv2.imwrite("c:/temp/raw_8bit.png", raw_8bit)

# rgb1 = dng.postprocess()  # demosaicing by rawpy
# cv2.imwrite("c:/temp/rgb1.jpg", rgb1[:, :, ::-1])
# rgb2 = dng.demosaicing(poww=0.3)  # demosaicing with gamma correction
# cv2.imwrite("c:/temp/rgb2.jpg", rgb2[:, :, ::-1])

raw = np.uint16([[0,0,0],[0,0,0],[0,0,0]])

DngFile.save(dng_path + "-save.dng", raw, bit=16)