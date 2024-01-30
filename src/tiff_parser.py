import struct

from src.constants import ifd_descriptions, field_types_names, type_sizes, filed_types_to_unpack


class Tag():
    def __init__(self, tag_code, field_type, field_count, field_value, unpacked_value=None):
        self.tag_code = tag_code
        self.field_type = field_type
        self.field_count = field_count
        self.field_value = field_value
        self.unpacked_value = unpacked_value

    def __str__(self):
        return f"Tag: {self.tag_code}, Field Type: {self.field_type}, Field Count: {self.field_count}, Value: {self.field_value}, Unpacked Value: {self.unpacked_value}"

    def __repr__(self):
        return f"Tag: {self.tag_code}, Field Type: {self.field_type}, Field Count: {self.field_count}, Value: {self.field_value}, Unpacked Value: {self.unpacked_value}"


def readTag(file):
    tag_code, field_type, field_count, field_value = struct.unpack('<HHII', file.read(12))
    unpacked_value = None
    if field_type in [5,10,12] or (field_count>1 and field_type in [4,9,11]) or (field_count>2 and field_type in [3,8] or (field_count>4 and field_type in [1,2,6,7])):
        current = file.tell()
        file.seek(field_value)
        data_size = type_sizes[field_type] * field_count
        # print("data2")
        # # print(f"description: {desc}")
        # # print(f"field description: {fdesc}")
        # print(f"field_count: {field_count}")
        # print(f"field_type: {field_type}")
        # print(data_size)
        unpack_type = filed_types_to_unpack[field_type]
        # print(f"unpack_type: {unpack_type}")
        data2 = file.read(data_size)
        # print(data2)
        try:
            unpacked_value = struct.unpack(f'<{field_count}{unpack_type}', data2)
            if len(unpacked_value)>40:
                unpacked_value = unpacked_value[:40]
        except struct.error as e:
            print(f"Error: {e}")
            # print(len(data2))
            unpacked_value = data2

        file.seek(current)


    return Tag(tag_code, field_type, field_count, field_value, unpacked_value)


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
            try:
                name = ifd_descriptions[tag.tag_code]
            except KeyError:
                name = f"Unknown: {tag.tag_code}"
            if name in tags:
                raise Exception(f"Tag {tag.tag_code} already exists")

            tags[name] = tag

        # if subifds are present in tags read them too
        #TODO
        if "SubIFDs" in tags:
            print("SubIFDs found")
            subifds = tags["SubIFDs"].unpacked_value
            for i,subifd in enumerate(subifds):
                file.seek(subifd)
                num_entries = struct.unpack('<H', file.read(2))[0]
                print(f"Number of SubIFD entries: {num_entries}")
                for entry_index in range(num_entries):
                    tag = readTag(file)
                    try:
                        name = ifd_descriptions[tag.tag_code]
                    except KeyError:
                        name = f"Unknown: {tag.tag_code}"
                    if name+f"({i})" in tags:
                        raise RuntimeError(f"Tag {tag.tag_code} already exists")

                    tags[name+f"({i})"] = tag

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
        desc = ifd_descriptions.get(tag_code, "Unknown")
        fdesc = field_types_names.get(field_type, "Unknown")

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
                value_field = "error. "+data2

            file.seek(current)

        print(f"Tag: {tag_code} ({desc}), Field Type: {field_type} ({fdesc}), Field Count: {field_count}, Value: {value_field}")


if __name__ == "__main__":
    car_small = r"F:\stills\sample_arriLogC_1.4.1.dng"
    tiff_filename = r"F:\stills\2x2-example-8bit.dng"
    generated = "F:\stills\minimalistic_dng_test.dng"
    example = r"F:\stills\dng_samples\01_jxl_linear_raw_integer.dng"

    linear_float = r"F:\stills\dng_samples\02_jxl_linear_raw_float.dng"
    tags = read_tiff_tags(linear_float)
    for name, tag in tags.items():
        print(f"{name}: {tag}")
