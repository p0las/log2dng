from field_types import Long, Short, Byte, SRational, Rational


class IfdMeta(type):
    def __repr__(cls):
        return f"{cls.__name__} - code: {cls.code}, type: {cls.field_type}"


class IfdField(metaclass=IfdMeta):
    code = -1
    field_type = -1


class SubIFDs(IfdField):
    code = 330
    field_type = Long.dng_code


class SampleFormat(IfdField):
    code = 339
    field_type = Short.dng_code


class NewSubfileType(IfdField):
    code = 254
    field_type = Long.dng_code


class ImageWidth(IfdField):
    code = 256
    field_type = Long.dng_code


class ImageHeight(IfdField):
    code = 257
    field_type = Long.dng_code


class BitsPerSample(IfdField):
    code = 258
    field_type = Short.dng_code


class Compression(IfdField):
    code = 259
    field_type = Short.dng_code


class PhotometricInterpretation(IfdField):
    code = 262
    field_type = Short.dng_code


class StripOffsets(IfdField):
    code = 273
    field_type = Long.dng_code


class Orientation(IfdField):
    code = 274
    field_type = Short.dng_code


class SamplesPerPixel(IfdField):
    code = 277
    field_type = Short.dng_code


class RowsPerStrip(IfdField):
    code = 278
    field_type = Long.dng_code


class StripByteCounts(IfdField):
    code = 279
    field_type = Long.dng_code


class PlanarConfiguration(IfdField):
    code = 284
    field_type = Short.dng_code


class DNGVersion(IfdField):
    code = 50706
    field_type = Byte.dng_code


class ColorMatrix1(IfdField):
    code = 50721
    field_type = SRational.dng_code


class AnalogBalance(IfdField):
    code = 50727
    field_type = Rational.dng_code


class CalibrationIlluminant1(IfdField):
    code = 50778
    field_type = Short.dng_code


class CFAPlaneColor(IfdField):
    code = 50710
    field_type = Byte.dng_code


class BlackLevel(IfdField):
    code = 50714
    field_type = Short.dng_code


class WhiteLevel(IfdField):
    code = 50717
    field_type = Short.dng_code


class BaselineExposure(IfdField):
    code = 50730
    field_type = SRational.dng_code

ifd_descriptions = {
    254: "NewSubfileType",
    256: "ImageWidth",
    257: "ImageHeight",
    258: "BitsPerSample",
    259: "Compression",
    262: "PhotometricInterpretation",
    273: "StripOffsets",
    274: "Orientation",
    277: "SamplesPerPixel",
    278: "RowsPerStrip",
    279: "StripByteCounts",
    282: "XResolution",
    283: "YResolution",
    284: "PlanarConfiguration",
    296: "ResolutionUnit",
    305: "Software",
    306: "DateTime",
    330: "SubIFDs",
    317: "Predictor",
    700: "XMP",
    34665: "Exif IFD Pointer",
    50706: "DNGVersion",
    50707: "DNGBackwardVersion",
    50708: "UniqueCameraModel",
    50721: "ColorMatrix1",
    50727: "AnalogBalance",
    50729: "AsShotWhiteXY",
    50730: "BaselineExposure",
    50731: "BaselineNoise",
    50732: "BaselineSharpness",
    50734: "LinearResponseLimit",
    50739: "ShadowScale",
    50778: "CalibrationIlluminant1",
    50781: "RawDataUniqueID",
    50879: "ColorimetricReference",
    50936: "ProfileName",
    50941: "ProfileEmbedPolicy",
    50966: "PreviewApplicationName",
    50967: "PreviewApplicationVersion",
    50969: "PreviewSettingsDigest",
    50970: "PreviewColorSpace",
    50971: "PreviewDateTime",
    51111: "NewRawImageDigest",

    # Add more tag codes as needed
}

ifd_codes = dict(map(reversed, ifd_descriptions.items()))

field_types_names = {
    1: "BYTE",
    2: "ASCII",
    3: "SHORT",
    4: "LONG",
    5: "RATIONAL",
    6: "SBYTE",
    7: "UNDEFINED",
    8: "SSHORT",
    9: "SLONG",
    10: "SRATIONAL",
    11: "FLOAT",
    12: "DOUBLE",
}
type_sizes = {
    1: 1,  # BYTE
    2: 1,  # ASCII
    3: 2,  # SHORT
    4: 4,  # LONG
    5: 8,  # RATIONAL
    6: 1,  # SBYTE
    7: 1,  # UNDEFINED
    8: 2,  # SSHORT
    9: 4,  # SLONG
    10: 8,  # SRATIONAL
    11: 4,  # FLOAT
    12: 8,  # DOUBLE
}
filed_types_to_unpack = {
    1: 'B',  # BYTE
    2: 's',  # ASCII
    3: 'H',  # SHORT
    4: 'I',  # LONG
    5: 'II',  # RATIONAL
    6: 'b',  # SBYTE
    7: 'B',  # UNDEFINED
    8: 'h',  # SSHORT
    9: 'i',  # SLONG
    10: 'ii',  # SRATIONAL
    11: 'f',  # FLOAT
    12: 'd',  # DOUBLE
}
