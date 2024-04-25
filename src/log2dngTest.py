import pytest

from log2dng import dngConvert
from matrices import CATs

@pytest.mark.skip("not a test but a conversion for manual inspection")
def test_performConversion():
    dngConvert(r"F:\stills\log2dng_raw_compare2\ACEScg_daylight.tif", r"F:\stills\log2dng_raw_compare2\ACEScg_daylight.dng", "ACES - ACEScc")




