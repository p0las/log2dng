from typing import Type

from field_types import FieldType, Long, Short, Byte, SRational, Rational, Ascii


class IfdMeta(type):
    def __repr__(cls):
        return f"{cls.__name__} - code: {cls.code}, type: {cls.field_type}"


class IfdField(metaclass=IfdMeta):
    code = -1
    field_type: Type[FieldType] = -1

    def __init__(self, num_values, value):
        self.num_values = num_values
        self.value = value


class SubIFDs(IfdField):
    code = 330
    field_type = Long


class SampleFormat(IfdField):
    code = 339
    field_type = Short


class NewSubfileType(IfdField):
    code = 254
    field_type = Long


class ImageWidth(IfdField):
    code = 256
    field_type = Long


class ImageHeight(IfdField):
    code = 257
    field_type = Long


class BitsPerSample(IfdField):
    code = 258
    field_type = Short


class Compression(IfdField):
    code = 259
    field_type = Short


class PhotometricInterpretation(IfdField):
    code = 262
    field_type = Short


class StripOffsets(IfdField):
    code = 273
    field_type = Long


class Orientation(IfdField):
    code = 274
    field_type = Short


class SamplesPerPixel(IfdField):
    code = 277
    field_type = Short


class RowsPerStrip(IfdField):
    code = 278
    field_type = Long


class StripByteCounts(IfdField):
    code = 279
    field_type = Long


class PlanarConfiguration(IfdField):
    code = 284
    field_type = Short


class DNGVersion(IfdField):
    code = 50706
    field_type = Byte


class ColorMatrix1(IfdField):
    code = 50721
    field_type = SRational


class AnalogBalance(IfdField):
    code = 50727
    field_type = Rational


class CalibrationIlluminant1(IfdField):
    code = 50778
    field_type = Short


class CFAPlaneColor(IfdField):
    code = 50710
    field_type = Byte


class BlackLevel(IfdField):
    code = 50714
    field_type = Short


class WhiteLevel(IfdField):
    code = 50717
    field_type = Short


class BaselineExposure(IfdField):
    code = 50730
    field_type = SRational


class Software(IfdField):
    code = 305
    field_type = Ascii
