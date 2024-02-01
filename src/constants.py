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
