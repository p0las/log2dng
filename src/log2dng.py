import argparse
import logging

from dng import writeDNG
from loader import loadImage

logger = logging.getLogger('log2dng')


def dngConvert(input_file, output_file, input_colour_space):
    img = loadImage(input_file, input_colour_space)
    height, width, _ = img.shape
    logger.info(f"Image dimensions: {width}x{height}")
    writeDNG(output_file, width, height, img)


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Converts a log file to a DNG file')
    parser.add_argument('--input_file', '-i', type=str, required=True, help='The log file to convert')
    parser.add_argument('--output_file', '-o', type=str, help='The output DNG file. Default is the input file name with a .dng extension.')
    parser.add_argument('--input_colour_space', '-s', type=str, help='The input colour space. Default is ACES - ACEScc.')
    parser.add_argument('--debug', action='store_true', default=False, help='log debug information to the console. Default is False.')

    args = parser.parse_args()

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if not args.input_colour_space:
        space = "ACES - ACEScc"
    else:
        space = args.input_colour_space

    if not args.output_file:
        name = args.input_file + '.dng'
    else:
        name = args.output_file

    logger.info(f"Converting log file '{args.input_file}' to DNG file...")
    logger.info(f"Input colour space: {space}")
    logger.info(f"Output file: {name}")

    dngConvert(args.input_file, name, space)

    logger.info(f"DNG file '{name}' created successfully.")
