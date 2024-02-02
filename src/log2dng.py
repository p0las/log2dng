import argparse
import logging

from dng import writeDNG
from loader import loadImage

logger = logging.getLogger('log2dng')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Converts a log file to a DNG file')
    parser.add_argument('--input_file', '-i', type=str, required=True, help='The log file to convert')
    parser.add_argument('--output_file', '-o', type=str, help='The output DNG file. Default is the input file name with a .dng extension.')
    parser.add_argument('--input_colour_space', '-s', type=str, help='The input colour space. Default is ACES - ACEScc.')
    args = parser.parse_args()

    if not args.input_colour_space:
        space = "ACES - ACEScc"
    else:
        space = args.input_colour_space

    logger.info(f"Converting log file '{args.input_file}' to DNG file...")
    logger.info(f"Input colour space: {space}")

    if not args.output_file:
        name = args.input_file + '.dng'
    else:
        name = args.output_file

    logger.info(f"Output file: {name}")

    img = loadImage(args.input_file, space)

    height, width, _ = img.shape

    logger.info(f"Image dimensions: {width}x{height}")

    writeDNG(name, width, height, img)

    logger.info(f"DNG file '{name}' created successfully.")
