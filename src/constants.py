class field_types:
    BYTE =  1
    ASCII =  2
    SHORT =  3
    LONG = 4
    RATIONAL =5
    SBYTE = 6
    UNDEFINED =7
    SSHORT = 8
    SLONG = 9
    SRATIONAL =10
    FLOAT = 11
    DOUBLE = 12

class IfdField:
    code = -1
    field_type = -1
    @property
    def name(self):
        return self.__class__.__name__


class SubIFDs(IfdField):
    code = 330
    field_type = field_types.LONG
class SampleFormat(IfdField):
    code = 339
    field_type = field_types.SHORT

class NewSubfileType(IfdField):
    code = 254
    field_type = field_types.LONG

class ImageWidth(IfdField):
    code = 256
    field_type = field_types.LONG

class ImageHeight(IfdField):
    code = 257
    field_type = field_types.LONG

class BitsPerSample(IfdField):
    code = 258
    field_type = field_types.SHORT

class Compression(IfdField):
    code = 259
    field_type = field_types.SHORT

class PhotometricInterpretation(IfdField):
    code = 262
    field_type = field_types.SHORT

class StripOffsets(IfdField):
    code = 273
    field_type = field_types.LONG

class Orientation(IfdField):
    code = 274
    field_type = field_types.SHORT

class SamplesPerPixel(IfdField):
    code = 277
    field_type = field_types.SHORT

class RowsPerStrip(IfdField):
    code = 278
    field_type = field_types.LONG

class StripByteCounts(IfdField):
    code = 279
    field_type = field_types.LONG

class PlanarConfiguration(IfdField):
    code = 284
    field_type = field_types.SHORT

class DNGVersion(IfdField):
    code = 50706
    field_type = field_types.BYTE

class ColorMatrix1(IfdField):
    code = 50721
    field_type = field_types.SRATIONAL

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
