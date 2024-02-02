import struct
from logging import getLogger
from typing import Type, List

import numpy as np

import ifd_types
from field_types import HalfFloat, FieldType, SRational
from loader import DNG_MATRIX

logger = getLogger('dng_creator')

IDF_DATA_BITS_COUNT = 4


def flatten(matrix):
    return [item for row in matrix for item in row]


def packIfd(ifd_class: Type[ifd_types.IfdField], num_values, value_offset):
    return struct.pack('<HHII', ifd_class.code, ifd_class.field_type.dng_code, num_values, value_offset)


class DNG():
    image_data_type = HalfFloat

    def __init__(self, width, height):
        self._width = width
        self._height = height

        # predefined
        self._header_size = 8

        # binary data
        self._binary_data = b''
        self._ifds = b''

        self._num_ifds = 0
        self._offsets = dict()
        self._last_ifd_id = -1  # to make sure they are in order as per DNG docs

    def _makeHeader(self):
        return b'II*\x00'  # Little-endian byte order, TIFF identifier and TIFF version (always 42)

    def add(self, ifd: Type[ifd_types.IfdField], num_values, data):

        if self._fitsToIfd(ifd.field_type, num_values):
            self.addIfd(ifd, num_values, data)
        else:
            # TODO: generate unique name here or id in case we have the same tag more then once
            name = str(ifd)
            offset = self.addData(name, data, ifd.field_type)
            self.addIfd(ifd, num_values, offset)

    def addData(self, name, data: List, data_type: Type[FieldType]):
        if not isinstance(data, list):
            data = [data]

        logger.info(f"Adding data {name} - size: {len(data)}, {data_type}")
        self._offsets[name] = self._header_size + len(self._binary_data)

        if data_type == SRational:
            denominator = 100000000
            numerators = [int(x * denominator) for x in data]
            denominators = [denominator] * len(data)
            data = flatten(zip(numerators, denominators))
            self._binary_data += struct.pack(f'<{len(data)}i', *data)
        else:

            # self._binary_data += np.array(data, dtype=f'<{data_type.short_code}').tobytes()

            self._binary_data += struct.pack(f'<{len(data)}{data_type.short_code}', *data)

        return self._offsets[name]

    def addIfd(self, ifd: Type[ifd_types.IfdField], num_values: int, value):
        logger.info(f"Adding IFD: {ifd}")
        if ifd.code < self._last_ifd_id:
            # TODO: handle it internally by keeping a dict of ifds instead one binary chunk
            raise Exception(f"IFD codes must be in ascending order: {ifd}")
        self._last_ifd_id = ifd.code
        self._ifds += packIfd(ifd, num_values, value)
        self._num_ifds += 1

    def addImageData(self, data):
        '''rgb data, no alpha'''

        logger.info(f"Adding image data - {self.image_data_type}")

        self._offsets['image'] = self._header_size + len(self._binary_data)

        self._binary_data += np.array(data.flatten(), dtype=f'<{self.image_data_type.short_code}').tobytes()

        return self._offsets['image']

    def _getIfdOffset(self):
        return self._header_size + len(self._binary_data)

    def _makeIfdHeader(self):
        return struct.pack('<H', self._num_ifds)

    def _makeIfdFooter(self):
        return struct.pack('<I', 0)

    def write(self, path):
        with open(path, 'wb') as f:
            f.write(self._makeHeader())
            f.write(struct.pack('<I', self._getIfdOffset()))
            f.write(self._binary_data)
            f.write(self._makeIfdHeader())
            f.write(self._ifds)
            f.write(self._makeIfdFooter())

    def _fitsToIfd(self, field_type: Type[FieldType], field_count: int):
        """check if the provided data can fit into ifd"""
        # we have 4 bytes to fit the data into

        if field_type.size * field_count <= IDF_DATA_BITS_COUNT:
            return True
        return False


def writeDNG(filename, width, height, data):
    dng = DNG(width, height)

    dng.add(ifd_types.NewSubfileType, 1, 0)
    dng.add(ifd_types.ImageWidth, 1, width)
    dng.add(ifd_types.ImageHeight, 1, height)
    dng.add(ifd_types.BitsPerSample, 3, [16, 16, 16])
    dng.add(ifd_types.Compression, 1, 1)  # 1 = uncompressed, 5 = LZW
    # https://community.adobe.com/t5/camera-raw-discussions/what-are-the-minimum-required-tags-for-a-dng-file/m-p/8962268
    dng.add(ifd_types.PhotometricInterpretation, 1, 34892)  # 34892 (linear raw)

    # TODO: combine those two into one
    offset = dng.addImageData(data)
    dng.addIfd(ifd_types.StripOffsets, 1, offset)

    dng.add(ifd_types.Orientation, 1, 1)
    dng.add(ifd_types.SamplesPerPixel, 1, 3)
    dng.add(ifd_types.RowsPerStrip, 1, height)
    dng.add(ifd_types.StripByteCounts, 1, width * height * 3 * dng.image_data_type.size)
    dng.add(ifd_types.PlanarConfiguration, 1, 1)
    dng.add(ifd_types.SampleFormat, 3, [3, 3, 3])
    dng.add(ifd_types.DNGVersion, 4, 1025)  # 1.4.0.0 yes I'm lazy here
    dng.add(ifd_types.BlackLevel, 3, [0, 0, 0])
    dng.add(ifd_types.WhiteLevel, 3, [100, 100, 100])  # a bit random value. not sure what max value I can get from aces_cc encoded footage
    dng.add(ifd_types.ColorMatrix1, 9, flatten(DNG_MATRIX))
    dng.add(ifd_types.BaselineExposure, 1, 5)  # this needs to be tailored  to the white level. very experimental values here. exposure is power of 2 (2^5 = 32) so the 100 makes no sense but works

    dng.add(ifd_types.CalibrationIlluminant1, 1, 0)

    dng.write(filename)

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
    # NewRawImageDigest: Tag: 51111, Field Type: 1, Field Count: 16, Value: 6706c

    # BaselineExposure: +3.32
    # BaselineNoise: 0.60
    # BaselineSharpness: 1.33
    # LinearResponseLimit: 1.00
    # BlackLevel: 0.00 0.00 0.00
    # WhiteLevel: 32768 32768 32768
