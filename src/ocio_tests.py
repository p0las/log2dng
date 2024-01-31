import cv2
import numpy as np
import PyOpenColorIO as OCIO


path = "F:\stills\lego_car\ACEScc.tif"

input_cs = "ACES - ACEScc"
output_cs = "Utility - Linear - sRGB"

img = cv2.imread(path)

config = OCIO.Config.CreateFromFile(r"O:\utils\openimageio\ocio2\cg-config-v2.1.0_aces-v1.3_ocio-v2.3.ocio")
in_colour = config.getColorSpace(input_cs)
out_colour = config.getColorSpace(output_cs)
processor = config.getProcessor(in_colour, out_colour)
cpu = processor.getDefaultCPUProcessor()
img2 = img.astype(np.float32) / 255

print(img2[0][0])
cpu.applyRGB(img2)
print(img2[0][0])


img4 = (img2*255.0).astype(np.uint8)

print(img[0][0])
print(img4[0][0])

cv2.imwrite(r"F:\stills\lego_car\ocio_test.tif", img4)