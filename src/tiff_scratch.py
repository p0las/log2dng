import struct
from typing import Type

import numpy as np

import constants
from constants import IfdField

import cv2

from loader import loadImage


def packIfd(ifd_class: Type[IfdField], num_values, value_offset):
    return struct.pack('<HHII', ifd_class.code, ifd_class.field_type, num_values, value_offset)


def generateMatrix():
    # sRGB to DCDMXYZ
    # NOT THIS ONE
    # m = [[0.4356235907, 0.3971433934, 0.1672800655],
    #      [0.2208065115, 0.7122275776, 0.0669677600],
    #      [0.0172263726, 0.1086536976, 0.8740667768]]

    """3.1336  -1.6168  -0.4907
          -0.9787   1.9161   0.0335
           0.0721  -0.2291   1.4054"""

    # from linear raw example:
    # oversaturated with sRGB and way too purple
    # NOT THIS ONE
    # m = [[
    #    0.9054,  -0.4504,   0.0215],
    #   [-0.4751,   1.2611,   0.2388],
    #   [-0.0296,   0.0802,   0.6816]]

    # NOT THIS ONE with sRGB data
    # m = [[1, 0, 0],
    #      [0, 1, 0],
    #      [0, 0, 1]]

    # taken from red.dng
    # this one is okish. too yellow/red
    # m = [
    #     [3.1336, -1.6168, -0.4907],
    #     [-0.9787, 1.9161, 0.0335],
    #     [0.0721, -0.2291, 1.4054]
    # ]

    # XYZ to sRGB https://www.image-engineering.de/library/technotes/958-how-to-convert-between-srgb-and-ciexyz
    # m = [[3.2404542, -1.5371385, -0.4985314,],
    #         [-0.9692660, 1.8760108, 0.0415560],
    #         [0.0556434, -0.2040259, 1.0572252]]

    # m = [[0.5767309, 0.1855540, 0.1881852],
    #      [0.2973769, 0.6273491, 0.0752741],
    #      [0.0270343, 0.0706872, 0.9911085]]
    #
    # #ACEScg to ProPhoto RGB
    # m = [[ 0.8550007004,  0.0330931791,  0.1120852557],
    #    [ 0.0518356731,  0.9368420118,  0.0112815341],
    #    [-0.0070844894,  0.0018182897,  1.0055405093]]
    #
    # #adobe wide gamut RGB to ProPhotoRGB
    # m = [[ 0.8982790259, -0.0518720305,  0.1537721399],
    #    [ 0.0000076458,  1.0389999049, -0.0390483317],
    #    [-0.0000000000,  0.0620840881,  0.9381902215]]

    # # AP1 to xyz https://colour.readthedocs.io/en/v0.3.7/colour.models.dataset.aces.html
    # m = [[0.66245418, 0.13400421, 0.15618769], [0.27222872, 0.67408177, 0.05368952], [-0.00557465, 0.00406073, 1.0103391]]
    # # AP0 to xyz
    # m = [[0.952552396, 0.00000000, 0.0000936786317], [0.343966450, 0.728166097, -0.0721325464], [0.00000000, 0.00000000, 1.00882518]]
    #
    # #to CIE XYZ
    # m = [[0.412453,0.212671,0.019334],[0.357580,0.715160,0.119193],[0.180423,0.072169,0.950227]]

    #DCDM XYZ to sRGB https://www.colour-science.org:8010/apps/rgb_colourspace_transformation_matrix?input-colourspace=DCDM+XYZ&output-colourspace=sRGB&chromatic-adaptation-transform=CAT02&formatter=repr&decimals=10
    m = [[ 3.1748210722, -1.6974555545, -0.4775222350],
       [-0.9899325492,  1.9499869504,  0.0400447478],
       [ 0.0604790950, -0.2089180222,  1.1485133649]]

    #DCDM XYZ to ALEXA Wide Gamut 4
    # m = [[ 1.4652841412, -0.3164934342, -0.1487907070],
    #    [-0.5139051082,  1.4065965188,  0.1073085894],
    #    [ 0.0007037509,  0.0009869408,  0.9983093083]]

    mult = 100000000
    m = [[int(x * mult) for x in y] for y in m]
    print(m)

    # from red.dng
    # return b"hz\x00\x00\x10'\x00\x00\xd8\xc0\xff\xff\x10'\x00\x00\xd5\xec\xff\xff\x10'\x00\x00\xc5\xd9\xff\xff\x10'\x00\x00\xd9J\x00\x00\x10'\x00\x00O\x01\x00\x00\x10'\x00\x00\xd1\x02\x00\x00\x10'\x00\x00\r\xf7\xff\xff\x10'\x00\x00\xe66\x00\x00\x10'\x00\x00"

    return struct.pack('<iiiiiiiiiiiiiiiiii', m[0][0], mult, m[0][1], mult, m[0][2], mult, m[1][0], mult, m[1][1], mult, m[1][2], mult, m[2][0], mult, m[2][1], mult, m[2][2], mult)


def writeDNG(filename, width, height, data):
    # TIFF Header
    tiff_header = b'II*\x00'  # Little-endian byte order, TIFF identifier and TIFF version (always 42)

    image_data_offset = 8
    # dump image data here and get the offset for ifds
    image = b''
    for x in data:
        for y in x:
            image += struct.pack('<eee', y[0], y[1], y[2])  # 16bit half floats BGR for some reason

    bits_per_sample_offset = image_data_offset + width * height * 3 * 2
    print(f"bits_per_sample_offset: {bits_per_sample_offset}")

    # dump bits per sample and get the offset for it
    image += struct.pack('<HHH', 16, 16, 16)

    matrix_offset = bits_per_sample_offset + 3 * 2

    # image += m
    # 3x3 float matrix
    image += generateMatrix()

    sample_format_offset = matrix_offset + 9 * 8

    image += struct.pack('<HHH', 3, 3, 3)  # float

    analog_balance_offset = sample_format_offset + 3 * 2

    image += b'@B\x0f\x00@B\x0f\x00@B\x0f\x00@B\x0f\x00@B\x0f\x00@B\x0f\x00'
    # print(len(m))
    # Image File Directory (IFD)
    ifd_offset = analog_balance_offset + 6 * 2
    # ifd_offset += 4
    # Offset to the IFD
    print(f"ifd_offset: {ifd_offset}")

    # NewSubfileType: Tag: 254, Field Type: 4, Field Count: 1, Value: 1
    # ImageWidth: Tag: 256, Field Type: 4, Field Count: 1, Value: 256
    # ImageHeight: Tag: 257, Field Type: 4, Field Count: 1, Value: 128
    # BitsPerSample: Tag: 258, Field Type: 3, Field Count: 3, Value: 482
    # Compression: Tag: 259, Field Type: 3, Field Count: 1, Value: 1
    # PhotometricInterpretation: Tag: 262, Field Type: 3, Field Count: 1, Value: 2
    # StripOffsets: Tag: 273, Field Type: 4, Field Count: 1, Value: 138302
    # Orientation: Tag: 274, Field Type: 3, Field Count: 1, Value: 1
    # SamplesPerPixel: Tag: 277, Field Type: 3, Field Count: 1, Value: 3
    # RowsPerStrip: Tag: 278, Field Type: 4, Field Count: 1, Value: 128
    # StripByteCounts: Tag: 279, Field Type: 4, Field Count: 1, Value: 98304
    # PlanarConfiguration: Tag: 284, Field Type: 3, Field Count: 1, Value: 1
    # Software: Tag: 305, Field Type: 2, Field Count: 49, Value: 488
    # DateTime: Tag: 306, Field Type: 2, Field Count: 20, Value: 538
    # SubIFDs: Tag: 330, Field Type: 4, Field Count: 1, Value: 6760
    # XMP: Tag: 700, Field Type: 1, Field Count: 5882, Value: 558
    # Exif IFD Pointer: Tag: 34665, Field Type: 4, Field Count: 1, Value: 6722
    # DNGVersion: Tag: 50706, Field Type: 1, Field Count: 4, Value: 1025
    # DNGBackwardVersion: Tag: 50707, Field Type: 1, Field Count: 4, Value: 257
    # UniqueCameraModel: Tag: 50708, Field Type: 2, Field Count: 5, Value: 6440
    # ColorMatrix1: Tag: 50721, Field Type: 10, Field Count: 9, Value: 6446
    # AnalogBalance: Tag: 50727, Field Type: 5, Field Count: 3, Value: 6518
    # AsShotWhiteXY: Tag: 50729, Field Type: 5, Field Count: 2, Value: 6542
    # BaselineExposure: Tag: 50730, Field Type: 10, Field Count: 1, Value: 6558
    # BaselineNoise: Tag: 50731, Field Type: 5, Field Count: 1, Value: 6566
    # BaselineSharpness: Tag: 50732, Field Type: 5, Field Count: 1, Value: 6574
    # LinearResponseLimit: Tag: 50734, Field Type: 5, Field Count: 1, Value: 6582
    # ShadowScale: Tag: 50739, Field Type: 5, Field Count: 1, Value: 6590
    # CalibrationIlluminant1: Tag: 50778, Field Type: 3, Field Count: 1, Value: 0
    # RawDataUniqueID: Tag: 50781, Field Type: 1, Field Count: 16, Value: 6598
    # ColorimetricReference: Tag: 50879, Field Type: 3, Field Count: 1, Value: 1
    # ProfileName: Tag: 50936, Field Type: 2, Field Count: 9, Value: 6614
    # ProfileEmbedPolicy: Tag: 50941, Field Type: 4, Field Count: 1, Value: 0
    # PreviewApplicationName: Tag: 50966, Field Type: 2, Field Count: 34, Value: 6624
    # PreviewApplicationVersion: Tag: 50967, Field Type: 2, Field Count: 5, Value: 6658
    # PreviewSettingsDigest: Tag: 50969, Field Type: 1, Field Count: 16, Value: 6664
    # PreviewColorSpace: Tag: 50970, Field Type: 4, Field Count: 1, Value: 2
    # PreviewDateTime: Tag: 50971, Field Type: 2, Field Count: 26, Value: 6680
    # NewRawImageDigest: Tag: 51111, Field Type: 1, Field Count: 16, Value: 6706

    num_entries = 17

    ifd = struct.pack('<H', num_entries)  # Number of directory entries (including one entry for the end of the IFD)
    # field type
    # ifd_entry = struct.pack('<HHIHH', tag, field_type, field_count, field_value, 0)
    # 4 Type: Long (32-bit unsigned integer) - I
    # 3 Type: Short (16-bit unsigned integer) - H

    # ifd += struct.pack('<HHII', constants.NewSubfileType.code, constants.NewSubfileType.field_type, 1, 1)  # NewSubfileType 1: Reduced-resolution image (often used for thumbnails or previews).

    ifd += packIfd(constants.NewSubfileType, 1, 0)
    ifd += packIfd(constants.ImageWidth, 1, width)
    ifd += packIfd(constants.ImageHeight, 1, height)
    ifd += packIfd(constants.BitsPerSample, 3, bits_per_sample_offset)
    ifd += packIfd(constants.Compression, 1, 1)
    ifd += packIfd(constants.PhotometricInterpretation, 1,
                   34892)  # 0x106 (PhotometricInterpretation), Short, 1 value, 34892 (linear raw) https://community.adobe.com/t5/camera-raw-discussions/what-are-the-minimum-required-tags-for-a-dng-file/m-p/8962268
    ifd += packIfd(constants.StripOffsets, 1, image_data_offset)
    ifd += packIfd(constants.Orientation, 1, 1)
    ifd += packIfd(constants.SamplesPerPixel, 1, 3)
    ifd += packIfd(constants.RowsPerStrip, 1, height)
    ifd += packIfd(constants.StripByteCounts, 1, width * height * 3 * 2)
    ifd += packIfd(constants.PlanarConfiguration, 1, 1)
    ifd += packIfd(constants.DNGVersion, 4, 1025)  # 1.4.0.0
    ifd += packIfd(constants.ColorMatrix1, 9, matrix_offset)
    ifd += packIfd(constants.SampleFormat, 3, sample_format_offset)
    ifd += packIfd(constants.AnalogBalance, 3, analog_balance_offset)  # no differnce to the weird colours
    ifd += packIfd(constants.CalibrationIlluminant1, 1, 0)  # no difference to the weird colours

    # 274
    # # Bits Per Sample
    #
    # # Strip Offsets
    # strip_offset = ifd_offset + len(ifd) + 4  # Offset to the image data
    # ifd += struct.pack('<HHI4s', 273, 4, 1, struct.pack('<I', strip_offset))
    #
    # # Rows Per Strip
    # rows_per_strip = height
    # ifd += struct.pack('<HHI4s', 278, 4, 1, struct.pack('<I', rows_per_strip))
    #
    # # Strip Byte Counts
    # strip_byte_counts = width * height
    # ifd += struct.pack('<HHI4s', 279, 4, 1, struct.pack('<I', strip_byte_counts))
    #
    # End of IFD
    ifd += struct.pack('<I', 0)

    # Write TIFF file
    with open(filename, 'wb') as f:
        f.write(tiff_header)
        f.write(struct.pack('<I', ifd_offset))
        f.write(image)
        f.write(ifd)

        # Write the image data as a single strip
        # for row in data:
        #     f.write(struct.pack(f'<{width}B', *row))


if __name__ == "__main__":
    # img = loadImage(r"F:\stills\sample_arriLogC_1.4.1.tif", "Input - Arri - Curve - V3 LogC (EI800)")
    # img = loadImage(r"F:\stills\lego_car\sRGB_linear.tif", "Utility - Linear - sRGB")  # "Utility - Linear - sRGB"

    # img = loadImage(r"F:\stills\lego_car\arriLogC.tif", "Input - Arri - Curve - V3 LogC (EI800)")  # "Utility - Linear - sRGB"

    img = loadImage(r"F:\stills\lego_car\ACEScc.tif", "ACES - ACEScc")  # "Utility - Linear - sRGB"


    cv2.imwrite(r"F:\stills\lego_car\dng_test_fromArri.tif", (img * 255).astype(np.uint8))
    print(img.shape)
    print(img[0][0])

    # width = 2
    # height = 2
    # data = [
    #     [[255 * 10, 0, 0], [0, 255 * 10, 0]],
    #     [[0, 0, 255 * 10], [0, 0, 0]],
    # ]  # RGB 2x2 image
    #
    # m = np.matrix([0.4124564,  0.3575761,  0.1804375, 0.2126729,  0.7151522,  0.0721750, 0.0193339,  0.1191920,  0.9503041])
    #
    #
    # xyz_pixels = np.matmul(np.array([1,0,0]), m)
    # xyz_data = [[xyz_pixels[0], xyz_pixels[1]],
    #             [xyz_pixels[2], xyz_pixels[0]]]

    tiff_filename = "f:/stills/lego_car/dng_test_fromArri.dng"

    height, width, _ = img.shape
    print(f"width: {width}, height: {height}")

    writeDNG(tiff_filename, width, height, img)

    print(f"TIFF file '{tiff_filename}' created successfully.")
