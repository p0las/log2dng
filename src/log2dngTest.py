import pytest

from log2dng import dngConvert
from matrices import CATs

def test_performConversion():
    dngConvert(r"F:\stills\log2dng_raw_compare2\ACEScg_daylight.tif", r"F:\stills\log2dng_raw_compare2\ACEScg_daylight.dng", "ACES - ACEScc")
    # dngConvert(r"F:\stills\log2dng_raw_compare2\ACEScg_shade.tif", r"F:\stills\log2dng_raw_compare2\ACEScg_shade.dng", "ACES - ACEScc")

@pytest.mark.parametrize("cat", CATs)
def test_cats(mocker, cat):

    mocker.patch('dng.DNG_MATRIX', cat)

    dngConvert(r"F:\stills\log2dng_raw_compare2\ACEScg_daylight.tif", r"F:\stills\log2dng_raw_compare2\cat{0}.dng".format(cat[0][0]), "ACES - ACEScc")



