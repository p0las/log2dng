from log2dng import dngConvert


def test_performConversion():
    dngConvert(r"F:\stills\lego_car\aces_cc_5k_panasonic.tif", r"F:\stills\lego_car\aces_cc_5k_panasonic.dng", "ACES - ACEScc")
