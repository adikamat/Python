import os, sys
import bz2
import base64
import traceback
import fractions
import struct
import string
import io
import StringIO
from abc import ABCMeta, abstractmethod


class ScenarioScoreCalc:
    __metaclass__ = ABCMeta

    @abstractmethod
    def calc_bin_score(self, impact_speed, test_speed):
        """

        :param impact_speed:  Impact speed of Ego at the time of collision in kph
        :param test_speed:  Speed of Ego at the start of test in kph
        :return: [Color (String), score (float)]m for e.g. ["Green", 1.0]
        """
        pass


class LUTBased(ScenarioScoreCalc):

    COLOR_SCORE = {0: ["Green", 1.0], 1: ["Yellow", 0.75], 2: ["Orange", 0.5], 3: ["Brown", 0.25], 4: ["Red", 0.0]}

    def __init__(self, table):
        """

        :param table: Dictionary with test speed (kph) as key and list of impact speed threshold (kph) as values
        """
        self.LUT = table

    def calc_bin_score(self, impact_speed, test_speed):

        if test_speed in self.LUT.keys():
            impact_sp_threshold = self.LUT[test_speed]
        else:
            print "Invalid test speed ", str(test_speed), ". Valid speeds are ", self.LUT.keys()
            impact_sp_threshold = {}

        try:
            index = next(x[0] for x in enumerate(impact_sp_threshold) if x[1] > impact_speed)
            # print index

        except StopIteration:
            # When no item found, return score 0, color red
            index = 4

        return self.COLOR_SCORE[index]


class SpeedReductionBased(ScenarioScoreCalc):

    AEB_VRU_MIN_SPD_REDUCTION = 20  # kph
    AEB_VRU_TS_SPD_TH = 40  # kph

    def __init__(self, table):
        """

        :param table: Dictionary with test speed (kph) as key and list of impact speed threshold (kph) as values
        """
        self.points_table = table

    def calc_bin_score(self, impact_speed, test_speed):

        if test_speed <= self.AEB_VRU_TS_SPD_TH:
           score = ((test_speed - impact_speed) / test_speed) * self.points_table[test_speed]

        else:
            score = self.points_table[test_speed] if (test_speed - impact_speed) >= self.AEB_VRU_MIN_SPD_REDUCTION else 0

        return ["NoColor", score]


class ThresholdBased(ScenarioScoreCalc):

    FCW_TTC_TH = 1.70  # seconds

    def __init__(self, table):
        """

        :param table: Dictionary with test speed (kph) as key and list of impact speed threshold (kph) as values
        """
        self.points_table = table

    def calc_bin_score(self, impact_speed, test_speed):

        if impact_speed >= self.FCW_TTC_TH:
            score = self.points_table[test_speed]
        else:
            score = 0

        return ["NoColor", score]


class ZeroImpactBased(ScenarioScoreCalc):

    FCW_TTC_TH = 1.70  # seconds

    def __init__(self, table):
        """

        :param table: Dictionary with test speed (kph) as key and list of impact speed threshold (kph) as values
        """
        self.points_table = table

    def calc_bin_score(self, impact_speed, test_speed):

        if impact_speed == 0:
            score = self.points_table[test_speed]
        else:
            score = 0

        return ["NoColor", score]
