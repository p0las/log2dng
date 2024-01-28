import struct


def write_tiff(filename, width, height, data):
    # TIFF Header
    tiff_header = b'II*\x00'  # Little-endian byte order, TIFF identifier and TIFF version (always 42)

    # Image File Directory (IFD)
    ifd_offset = 8  # Offset to the IFD
    num_entries = 39
    ifd = struct.pack('<H', num_entries)  # Number of directory entries (including one entry for the end of the IFD)
    # field type
    # ifd_entry = struct.pack('<HHIHH', tag, field_type, field_count, field_value, 0)
    # 4 Type: Long (32-bit unsigned integer) - I
    # 3 Type: Short (16-bit unsigned integer) - H

    ifd += struct.pack('<HHII', 254, 4, 1, 1)  # NewSubfileType 1: Reduced-resolution image (often used for thumbnails or previews).

    ifd += struct.pack('<HHII', 256, 4, 1, width)
    ifd += struct.pack('<HHII', 257, 4, 1, height)
    # 02 01 03 00 03 00 00 00
    ifd += struct.pack('<HHIHH', 258, 3, 3, 482, 0)  # bits per sample - 482 is the offset to the actual data. TODO: store the index to set the value later
    bits_per_sample_index = len(ifd) #TODO: not sure about this
    print(bits_per_sample_index)
    ifd += struct.pack('<HHII', 259, 3, 1, 1)  # Compression: Uncompressed
    ifd += struct.pack('<HHII', 262, 3, 1, 2)  # PhotometricInterpretation: RGB. RGB value of (0,0,0) represents black, and (255,255,255) represents white, assuming 8-bit components. The components are stored in the indicated order: first Red, then Green, then Blue.
    ifd += struct.pack('<HHII', 273, 4, 1, 8180)  # StripOffsets: The offset to the beginning of the image data. 	N = StripsPerImage for PlanarConfiguration equal to 1; N = SamplesPerPixel * StripsPerImage for PlanarConfiguration equal to 2 #TODO: how do I know that number



    #274
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
    # # End of IFD
    # ifd += struct.pack('<I', 0)

    # Write TIFF file
    with open(filename, 'wb') as f:
        f.write(tiff_header)
        f.write(struct.pack('<I', ifd_offset))
        f.write(ifd)

        # Write the image data as a single strip
        # for row in data:
        #     f.write(struct.pack(f'<{width}B', *row))


if __name__ == "__main__":
    width = 2
    height = 2
    data = [[0, 0], [0, 0]]  # Black and white 2x2 image

    tiff_filename = "f:/stills/output.dng"
    write_tiff(tiff_filename, width, height, data)

    print(f"TIFF file '{tiff_filename}' created successfully.")
