import struct
import datetime

def create_dng(output_file_path):
    # DNG header
    dng_header = b'DNG\x01\x00\x00\x00'

    # DNG Image Data
    image_data = b'\x00' * 1000  # Placeholder for image data

    # DNG metadata (you need to fill in the actual metadata)
    metadata = {
        'DateTime': datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S'),
        # Add other required metadata fields here
    }

    # Serialize metadata
    metadata_bytes = serialize_metadata(metadata)

    # Write to the output file
    with open(output_file_path, 'wb') as f:
        f.write(dng_header)
        f.write(metadata_bytes)
        f.write(image_data)

def serialize_metadata(metadata):
    metadata_bytes = b''

    for tag, value in metadata.items():
        # Assuming that all tags are ASCII strings
        tag_bytes = tag.encode('ascii') + b'\x00'
        value_bytes = str(value).encode('ascii') + b'\x00'

        entry = struct.pack('<HHI', len(tag_bytes), len(value_bytes), 0)
        metadata_bytes += entry + tag_bytes + value_bytes

    return metadata_bytes

if __name__ == '__main__':
    create_dng(r'F:\stills\test_from_scratch.dng')