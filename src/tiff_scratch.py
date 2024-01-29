import struct
from typing import Type

from src import constants
from src.constants import IfdField


def packIfd(ifd_class: Type[IfdField], num_values, value_offset):
    return struct.pack('<HHII', ifd_class.code, ifd_class.field_type, num_values, value_offset)


def write_tiff(filename, width, height, data):
    # TIFF Header
    tiff_header = b'II*\x00'  # Little-endian byte order, TIFF identifier and TIFF version (always 42)

    image_data_offset = 8
    # dump image data here and get the offset for ifds
    image = b''
    for x in data:
        for y in x:
            image += struct.pack('<HHH', y[0], y[1], y[2])

    bits_per_sample_offset = image_data_offset + width * height * 3 *2
    print(f"bits_per_sample_offset: {bits_per_sample_offset}")

    # dump bits per sample and get the offset for it
    image += struct.pack('<HHH', 16, 16, 16)

    matrix_offset = bits_per_sample_offset + 3*2
    #color matrix
    m = b"hz\x00\x00\x10'\x00\x00\xd8\xc0\xff\xff\x10'\x00\x00\xd5\xec\xff\xff\x10'\x00\x00\xc5\xd9\xff\xff\x10'\x00\x00\xd9J\x00\x00\x10'\x00\x00O\x01\x00\x00\x10'\x00\x00\xd1\x02\x00\x00\x10'\x00\x00\r\xf7\xff\xff\x10'\x00\x00\xe66\x00\x00\x10'\x00\x00"
    image += m

    print(len(m))
    # Image File Directory (IFD)
    ifd_offset = matrix_offset + len(m)
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




    num_entries = 14

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
    ifd += packIfd(constants.PhotometricInterpretation, 1, 34892) #0x106 (PhotometricInterpretation), Short, 1 value, 34892 (linear raw) https://community.adobe.com/t5/camera-raw-discussions/what-are-the-minimum-required-tags-for-a-dng-file/m-p/8962268
    ifd += packIfd(constants.StripOffsets, 1, image_data_offset)
    ifd += packIfd(constants.Orientation, 1, 1)
    ifd += packIfd(constants.SamplesPerPixel, 1, 3)
    ifd += packIfd(constants.RowsPerStrip, 1, height)
    ifd += packIfd(constants.StripByteCounts, 1, width * height * 3 *2)
    ifd += packIfd(constants.PlanarConfiguration, 1, 1)
    ifd += packIfd(constants.DNGVersion, 4, 1025) #1.4.0.0
    ifd += packIfd(constants.ColorMatrix1, 9, matrix_offset)

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
    width = 2
    height = 2
    data = [
        [[0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0]],
    ]  # RGB 2x2 image

    tiff_filename = "f:/stills/minimalistic_dng_test.dng"
    write_tiff(tiff_filename, width, height, data)

    print(f"TIFF file '{tiff_filename}' created successfully.")
