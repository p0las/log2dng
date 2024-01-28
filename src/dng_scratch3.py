import datetime
import struct

def create_minimal_dng(output_file_path):
    width, height = 10, 10

    # DNG metadata (replace with actual metadata)
    metadata = {
        0x010F: "Adobe",
        0x0110: "DNG Example",
        0x8769: [
            {0x0103: 1},  # Compression: Uncompressed
            {0x0111: height},  # Image height
            {0x0112: width},  # Image width
            {0x0117: 1},  # Strip offsets
            {0x0118: 1},  # Rows per strip
            {0x0119: height * width},  # Strip byte counts
            {0x8769: [
                {0xC612: b'\x01\x00\x00\x00'}  # Black level
            ]}
        ]
    }

    # Calculate the offset for the image data
    ifd_offset = 16 + len(metadata) * 12  # 16 bytes for header + 12 bytes per IFD entry

    # Create the DNG header
    dng_header = b'DNG\x01' + struct.pack('<I', ifd_offset)

    # Create the IFD entries
    ifd_entries = b''
    for tag, values in metadata.items():
        field_type = 4 if isinstance(values, int) else 2
        field_count = len(values) if isinstance(values, list) else 1
        value_offset = 0 if field_type == 2 else values[0]
        ifd_entries += struct.pack('<HHII', tag, field_type, field_count, value_offset)

    # Create the image data (black image)
    image_data = b'\x00' * (width * height * 3)  # Assuming RGB with 8 bits per channel

    # Create the DNG data structure
    dng_data = dng_header + ifd_entries + image_data

    # Write to the output file
    with open(output_file_path, 'wb') as f:
        f.write(dng_data)



if __name__ == '__main__':
    create_minimal_dng(r'F:\stills\test_from_scratch3.dng')
