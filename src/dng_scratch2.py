import datetime
from construct import Struct, Int32ul, Int16ul, Int8ul, Bytes, Array, Padding, Const

def create_dng(output_file_path):
    dng_struct = Struct(
        "header" / Bytes(4),
        "ifd_offset" / Int32ul,
        "ifd" / Struct(
            "count" / Int16ul,
            "tags" / Array(lambda ctx: ctx.count, Struct(
                "tag" / Int16ul,
                "field_type" / Int16ul,
                "field_count" / Int32ul,
                "value_offset" / Int32ul,
                Padding(4),  # Padding to align the structure
            ))
        ),
        "zero" / Const(b'\x00\x00\x00\x00'),
        "image_data" / Bytes(lambda ctx: ctx.ifd_offset - 16),  # Dynamic field based on ifd_offset
    )

    # DNG metadata (replace with actual metadata)
    metadata = {
        0x010F: "Adobe",
        0x0110: "DNG Example",
        0x8769: [
            {0x9003: datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')}  # DateTime
        ]
    }

    # Convert metadata to the IFD structure
    ifd_tags = []
    for tag, values in metadata.items():
        if isinstance(values, list):
            for value in values:
                ifd_tags.append({"tag": tag, "field_type": 2, "field_count": len(value), "value_offset": 0})
        else:
            ifd_tags.append({"tag": tag, "field_type": 2, "field_count": len(values), "value_offset": 0})

    # Calculate the offset for the image data
    ifd_offset = 16 + len(ifd_tags) * 12  # 16 bytes for header + 12 bytes per IFD entry

    # Create the DNG data structure
    dng_data = dng_struct.build({
        "header": b'DNG\x01',
        "ifd_offset": ifd_offset,
        "ifd": {
            "count": len(ifd_tags),
            "tags": ifd_tags
        }
    })

    # Write to the output file
    with open(output_file_path, 'wb') as f:
        f.write(dng_data)


if __name__ == '__main__':
    create_dng(r'F:\stills\test_from_scratch2.dng')