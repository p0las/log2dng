import numpy as np

from dng import DNG
from loader import loadImage

img = loadImage(f"F:/stills/lego_car/aces_cc_5k_panasonic.tif", "ACES - ACEScc")


import zlib

def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
            compresslevel,        # level: 0-9
            zlib.DEFLATED,        # method: must be DEFLATED
            -zlib.MAX_WBITS,      # window size in bits:
                                  #   -15..-8: negate, suppress header
                                  #   8..15: normal
                                  #   16..30: subtract 16, gzip header
            zlib.DEF_MEM_LEVEL,   # mem level: 1..8/9
            0                     # strategy:
                                  #   0 = Z_DEFAULT_STRATEGY
                                  #   1 = Z_FILTERED
                                  #   2 = Z_HUFFMAN_ONLY
                                  #   3 = Z_RLE
                                  #   4 = Z_FIXED
    )
    deflated = compress.compress(data)
    deflated += compress.flush()
    return deflated


print(float(len(img))/float(len(deflate(img,1))))
# compress(np.array(img.flatten(), dtype=f'<{DNG.image_data_type.short_code}').tobytes(), out)
