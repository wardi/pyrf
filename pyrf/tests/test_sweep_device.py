import unittest

from pyrf.sweep_device import plan_sweep
from pyrf.devices.thinkrf import WSA4000
from pyrf.units import M


class WSA42(object):
    """
    An imaginary device for testing plan sweep
    """
    FULL_BW = 128*M
    USABLE_BW = 66*M
    MIN_TUNABLE = 64*M
    MAX_TUNABLE = 2048*M
    MIN_DECIMATION = 2
    MAX_DECIMATION = 256
    DECIMATED_USABLE = 0.75
    DC_OFFSET_BW = 2*M

class TestPlanSweep(unittest.TestCase):
    def _plan42(self, start, stop, count, expected):
        """
        Develop a plan for sweeping with a WSA42, verify that
        it matches the expected plan
        """
        result = plan_sweep(WSA42, start, stop, count)
        self.assertEquals(result, expected)

    def test_simple_within_sweep_single(self):
        self._plan42(100*M, 164*M, 64,
            [(165*M, 165*M, 0, 0, 1, 256, 126, 64, 1)])


    #def test_vlow_plus_normal(self):
    #    self._plan4k(30*M, 67*M, 50*K,
    #        [(0, 37187500, 4, 2048, 553, 983, 312),
    #         (90*M, 0, 1, 8192, 655, 1507, 460),])

