import struct

field_descriptions = {
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
field_types = {
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


class Tag():
    def __init__(self, tag_code, field_type, field_count, field_value):
        self.tag_code = tag_code
        self.field_type = field_type
        self.field_count = field_count
        self.field_value = field_value

    def __str__(self):
        return f"Tag: {self.tag_code}, Field Type: {self.field_type}, Field Count: {self.field_count}, Value: {self.field_value}"

    def __repr__(self):
        return f"Tag: {self.tag_code}, Field Type: {self.field_type}, Field Count: {self.field_count}, Value: {self.field_value}"


def readTag(file):
    tag_code, field_type, field_count, field_value = struct.unpack('<HHII', file.read(12))
    return Tag(tag_code, field_type, field_count, field_value)


def read_tiff_tags(filename):
    tags = {}
    with open(filename, 'rb') as file:
        # Read TIFF header
        tiff_identifier = file.read(2)
        if tiff_identifier != b'II':
            print("Error: Not a valid TIFF file.")
            return

        # Read TIFF version (always 42)
        tiff_version = struct.unpack('<H', file.read(2))[0]
        if tiff_version != 42:
            print("Error: Unsupported TIFF version.")
            return

        # Read offset to IFD
        ifd_offset = struct.unpack('<I', file.read(4))[0]

        # Seek to IFD
        file.seek(ifd_offset)

        # Read number of directory entries
        num_entries = struct.unpack('<H', file.read(2))[0]

        print(f"Number of IFD entries: {num_entries}")

        # Read and print each IFD entry
        for entry_index in range(num_entries):
            tag = readTag(file)
            name = field_descriptions[tag.tag_code]
            if name in tags:
                raise Exception(f"Tag {tag.tag_code} already exists")

            tags[name] = tag

        return tags


        print("------------------------")
        print(entry_index)
        tag_read = file.read(8)
        print(tag_read)
        tag_code, field_type, field_count = struct.unpack('<HHI', tag_read)

        # field_count = 1
        # # Calculate the size of the value field
        # if field_type == 3:  # Short (16-bit) values
        #     value_size = field_count * 2
        #     value_type='H'
        # elif field_type == 4:  # Long (32-bit) values

        # else:
        #     print(f"Unsupported field type: {field_type}")
        #     return

        # Read the value field
        data = file.read(4)

        print(data)

        value_field = struct.unpack(f'<I', data)
        desc = field_descriptions.get(tag_code, "Unknown")
        fdesc = field_types.get(field_type, "Unknown")

        if value_field[0] > 100:  # TODO it is a value if it can fit into the value field size which is 4 bytes otherwise it is an offset
            current = file.tell()
            file.seek(value_field[0])
            data_size = type_sizes[field_type] * field_count
            # print("data2")
            # print(f"description: {desc}")
            # print(f"field description: {fdesc}")
            # print(f"field_count: {field_count}")
            # print(f"field_type: {field_type}")
            # print(data_size)
            unpack_type = filed_types_to_unpack[field_type]
            print(f"unpack_type: {unpack_type}")
            data2 = file.read(data_size)
            try:
                value_field = struct.unpack(f'<{field_count}{unpack_type}', data2)
            except struct.error as e:
                print(f"Error: {e}")
                print(len(data2))
                value_field = "error"

            file.seek(current)

        print(f"Tag: {tag_code} ({desc}), Field Type: {field_type} ({fdesc}), Field Count: {field_count}, Value: {value_field}")


if __name__ == "__main__":
    tiff_filename = r"F:\stills\2x2-example-8bit.dng"
    tags = read_tiff_tags(tiff_filename)
    for name, tag in tags.items():
        print(f"{name}: {tag}")
