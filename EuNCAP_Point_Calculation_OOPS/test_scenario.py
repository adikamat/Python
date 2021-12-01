import os, sys
import bz2
import base64
import traceback
import fractions
import struct
import string
import io
import csv
from abc import ABCMeta, abstractmethod
import scenario_score_calculation as ScoreCalculation
import impact_speed_calculation as ImpactSpeedCalc
from Write_Output import *
from common import *
from main import SIM_RUN_LENGTH, EXPORT_TO_CSV

class TestScenario:
    __metaclass__ = ABCMeta

    EXPORT_TO_CSV = True
    MONTE_CARLO_ITERATIONS = 1000

    def __init__(self):
        self.ScenarioName = ""
        self.TEST_CASES = []
        self.ScoreCalculator = None
        self.ImpactSpeedCalculator = None
        self.TargetSpeed = 0
        self.SimScore = 0
        self.SimMaxScore = 0
        self.EXPORT_TO_CSV = EXPORT_TO_CSV
        self.MONTE_CARLO_ITERATIONS = SIM_RUN_LENGTH
        self.monte_carlo_method = None
        self.points_table = None
        self.overlap_table = None
        self.warning_list = []

    @abstractmethod
    def prepare_test_list(self):
        pass

    def run_monte_carlo(self):
        """

        :return:
        """
        testcase_list = self.prepare_test_list()

        [points, max_points, warnings_list, csv_rows] = self.monte_carlo_method(self.MONTE_CARLO_ITERATIONS,
                                                                                testcase_list,
                                                                                self.ScenarioName,
                                                                                self.points_table,
                                                                                self.overlap_table)

        self.warning_list.extend(warnings_list)

        if self.EXPORT_TO_CSV:
            out_logger = WriteOutput.instance()
            out_logger.write_to_csv(csv_rows, self.ScenarioName)
            out_logger.add_to_warn_list(warnings_list)

        self.SimScore = points
        self.SimMaxScore = max_points

    @classmethod
    def set_monte_carlo_iteration(cls, num_iterations):
        cls.MONTE_CARLO_ITERATIONS = num_iterations

    @classmethod
    def set_export_to_csv(cls, export_to_csv):
        cls.EXPORT_TO_CSV = export_to_csv

    def add_test_case(self, testcase):
        """

        :param testcase: Test case dictionary
        :return: None
        """

        if self.ImpactSpeedCalculator is None:
            raise AttributeError("Score Calculator for scenario " + self.ScenarioName + " is not set")
        else:
            testcase["ImpactSpeed"] = self.ImpactSpeedCalculator.calc_impact_speed(testcase["MeasuredTTC"],
                                                                                   testcase["TestSpeed"],
                                                                                   self.TargetSpeed)

        if self.ScoreCalculator is None:
            raise AttributeError("Score Calculator for scenario " + self.ScenarioName + " is not set")
        else:
            score_color, score_value = self.ScoreCalculator.calc_bin_score(testcase["ImpactSpeed"],
                                                                           testcase["TestSpeed"])

            # Store the color bin and points to test case
            testcase["ColorScore"] = score_value
            testcase["Color"] = score_color

        self.TEST_CASES.append(testcase)


###########################################
#         CAR TO CAR SCENARIOS
###########################################
class CCRs(TestScenario):

    CCRs_impact_vel_th = {10: [1, 1, 1, 1, 10],
                          15: [1, 1, 1, 1, 15],
                          20: [1, 1, 1, 1, 20],
                          25: [5, 5, 15, 15, 25],
                          30: [5, 15, 25, 25, 30],
                          35: [5, 15, 25, 25, 35],
                          40: [5, 15, 25, 35, 40],
                          45: [5, 15, 25, 35, 45],
                          50: [5, 15, 30, 40, 50],
                          55: [5, 15, 30, 45, 55],
                          60: [5, 20, 35, 50, 60],
                          65: [5, 20, 40, 55, 65],
                          70: [5, 20, 40, 60, 70],
                          75: [5, 25, 45, 65, 75],
                          80: [5, 25, 50, 70, 80]}

    CCRs_points_AEB = {10: 1, 15: 2, 20: 2, 25: 2, 30: 2, 35: 2, 40: 1, 45: 1, 50: 1}

    OVERLAP = ['-50', '-75', '100', '75', '50']

    def __init__(self):
        super(CCRs, self).__init__()
        self.ScenarioName = 'CCRs'
        self.ScoreCalculator = ScoreCalculation.LUTBased(self.CCRs_impact_vel_th)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_car
        self.points_table = self.CCRs_points_AEB
        self.overlap_table = self.OVERLAP

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_overlap_based(self.CCRs_impact_vel_th, self.OVERLAP, self.TEST_CASES)
        return testcase_lists


class CCRs_FCW(TestScenario):

    CCRs_impact_vel_th = {10: [1, 1, 1, 1, 10],
                          15: [1, 1, 1, 1, 15],
                          20: [1, 1, 1, 1, 20],
                          25: [5, 5, 15, 15, 25],
                          30: [5, 15, 25, 25, 30],
                          35: [5, 15, 25, 25, 35],
                          40: [5, 15, 25, 35, 40],
                          45: [5, 15, 25, 35, 45],
                          50: [5, 15, 30, 40, 50],
                          55: [5, 15, 30, 45, 55],
                          60: [5, 20, 35, 50, 60],
                          65: [5, 20, 40, 55, 65],
                          70: [5, 20, 40, 60, 70],
                          75: [5, 25, 45, 65, 75],
                          80: [5, 25, 50, 70, 80]}

    CCRs_points_FCW = {30: 2, 35: 2, 40: 2, 45: 2, 50: 3, 55: 2, 60: 1, 65: 1, 70: 1, 75: 1, 80: 1}

    OVERLAP = ['-50', '-75', '100', '75', '50']

    def __init__(self):
        super(CCRs_FCW, self).__init__()
        self.ScenarioName = 'CCRs_FCW'
        self.ScoreCalculator = ScoreCalculation.LUTBased(self.CCRs_impact_vel_th)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_car
        self.points_table = self.CCRs_points_FCW
        self.overlap_table = self.OVERLAP

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_overlap_based(self.CCRs_points_FCW, self.OVERLAP, self.TEST_CASES)
        return testcase_lists


class CCRm(TestScenario):

    CCRm_impact_vel_th = {30: [5, 5, 5, 5, 10],
                          35: [5, 5, 5, 5, 15],
                          40: [5, 5, 15, 15, 20],
                          45: [5, 5, 15, 15, 25],
                          50: [5, 15, 25, 25, 30],
                          55: [5, 15, 25, 25, 35],
                          60: [5, 15, 25, 35, 40],
                          65: [5, 15, 25, 35, 45],
                          70: [5, 15, 30, 40, 50],
                          75: [5, 15, 30, 45, 55],
                          80: [5, 20, 35, 50, 60]}

    CCRm_points_AEB = {30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1, 65: 2, 70: 2, 75: 2, 80: 2}

    OVERLAP = ['-50', '-75', '100', '75', '50']

    def __init__(self):
        super(CCRm, self).__init__()
        self.ScenarioName = 'CCRm'
        self.ScoreCalculator = ScoreCalculation.LUTBased(self.CCRm_impact_vel_th)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.TargetSpeed = 20  # kph
        self.monte_carlo_method = monte_carlo_run_car_to_car
        self.points_table = self.CCRm_points_AEB
        self.overlap_table = self.OVERLAP

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_overlap_based(self.CCRm_impact_vel_th, self.OVERLAP, self.TEST_CASES)
        return testcase_lists

###########################################
#       CAR TO BICYCLE SCENARIOS
###########################################
class CBNA(TestScenario):

    CBNA_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}

    def __init__(self):
        super(CBNA, self).__init__()
        self.ScenarioName = 'CBNA'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CBNA_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CBNA_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CBNA_points_AEB, self.TEST_CASES)
        return testcase_lists


class CBNAO(TestScenario):

    CBNAO_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}

    def __init__(self):
        super(CBNAO, self).__init__()
        self.ScenarioName = 'CBNAO'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CBNAO_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CBNAO_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CBNAO_points_AEB, self.TEST_CASES)
        return testcase_lists


class CBFA(TestScenario):

    CBFA_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}

    def __init__(self):
        super(CBFA, self).__init__()
        self.ScenarioName = 'CBFA'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CBFA_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CBFA_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CBFA_points_AEB, self.TEST_CASES)
        return testcase_lists


class CBLA_AEB(TestScenario):

    CBLA_points_AEB = {25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 1}

    def __init__(self):
        super(CBLA_AEB, self).__init__()
        self.ScenarioName = 'CBLA_AEB'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CBLA_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CBLA_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CBLA_points_AEB, self.TEST_CASES)
        return testcase_lists


class CBLA_FCW(TestScenario):

    CBLA_points_FCW = {50: 3, 55: 3, 60: 1, 65: 1, 70: 1, 75: 1, 80: 1}

    def __init__(self):
        super(CBLA_FCW, self).__init__()
        self.ScenarioName = 'CBLA_FCW'
        self.ScoreCalculator = ScoreCalculation.ThresholdBased(self.CBLA_points_FCW)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CBLA_points_FCW

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CBLA_points_FCW, self.TEST_CASES)
        return testcase_lists

###########################################
#       CAR TO PEDESTRIAN SCENARIOS
###########################################
class CPFA_50_Day(TestScenario):

    CPFA_50_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}

    def __init__(self):
        super(CPFA_50_Day, self).__init__()
        self.ScenarioName = 'CPFA_50_Day'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPFA_50_Day_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPFA_50_Day_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPFA_50_Day_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPNA_25_Day(TestScenario):

    CPNA_25_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}

    def __init__(self):
        super(CPNA_25_Day, self).__init__()
        self.ScenarioName = 'CPNA_25_Day'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPNA_25_Day_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPNA_25_Day_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPNA_25_Day_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPNA_25_Night(TestScenario):

    CPNA_25_Night_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}

    def __init__(self):
        super(CPNA_25_Night, self).__init__()
        self.ScenarioName = 'CPNA_25_Night'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPNA_25_Night_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPNA_25_Night_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPNA_25_Night_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPNA_75_Day(TestScenario):

    CPNA_75_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}

    def __init__(self):
        super(CPNA_75_Day, self).__init__()
        self.ScenarioName = 'CPNA_75_Day'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPNA_75_Day_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPNA_75_Day_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPNA_75_Day_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPNA_75_Night(TestScenario):

    CPNA_75_Night_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}

    def __init__(self):
        super(CPNA_75_Night, self).__init__()
        self.ScenarioName = 'CPNA_75_Night'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPNA_75_Night_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPNA_75_Night_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPNA_75_Night_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPNC_50_Day(TestScenario):

    CPNC_50_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}

    def __init__(self):
        super(CPNC_50_Day, self).__init__()
        self.ScenarioName = 'CPNC_50_Day'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPNC_50_Day_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPNC_50_Day_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPNC_50_Day_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPLA_50_Day(TestScenario):

    CPLA_50_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}

    def __init__(self):
        super(CPLA_50_Day, self).__init__()
        self.ScenarioName = 'CPLA_50_Day'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPLA_50_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPLA_50_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPLA_50_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPLA_50_Night(TestScenario):

    CPLA_50_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}

    def __init__(self):
        super(CPLA_50_Night, self).__init__()
        self.ScenarioName = 'CPLA_50_Night'
        self.ScoreCalculator = ScoreCalculation.SpeedReductionBased(self.CPLA_50_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPLA_50_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPLA_50_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPLA_25_Day(TestScenario):

    CPLA_25_points_AEB = {50: 3, 55: 3, 60: 2, 65: 1, 70: 1, 75: 1, 80: 1}

    def __init__(self):
        super(CPLA_25_Day, self).__init__()
        self.ScenarioName = 'CPLA_25_Day'
        self.ScoreCalculator = ScoreCalculation.ThresholdBased(self.CPLA_25_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPLA_25_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPLA_25_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPLA_25_Night(TestScenario):

    CPLA_25_points_AEB = {50: 3, 55: 3, 60: 2, 65: 1, 70: 1, 75: 1, 80: 1}

    def __init__(self):
        super(CPLA_25_Night, self).__init__()
        self.ScenarioName = 'CPLA_25_Night'
        self.ScoreCalculator = ScoreCalculation.ThresholdBased(self.CPLA_25_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPLA_25_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPLA_25_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPLTO(TestScenario):

    CPLTO_points_AEB = {10: 1, 15: 1, 20: 1}

    def __init__(self):
        super(CPLTO, self).__init__()
        self.ScenarioName = 'CPLTO'
        self.ScoreCalculator = ScoreCalculation.ZeroImpactBased(self.CPLTO_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPLTO_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPLTO_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPRTO(TestScenario):

    CPRTO_points_AEB = {10: 1}

    def __init__(self):
        super(CPRTO, self).__init__()
        self.ScenarioName = 'CPRTO'
        self.ScoreCalculator = ScoreCalculation.ZeroImpactBased(self.CPRTO_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPRTO_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPRTO_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPRA_Static(TestScenario):

    CPRA_Static_points_AEB = {4: 1, 8: 1}

    def __init__(self):
        super(CPRA_Static, self).__init__()
        self.ScenarioName = 'CPRA_Static'
        self.ScoreCalculator = ScoreCalculation.ZeroImpactBased(self.CPRA_Static_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPRA_Static_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPRA_Static_points_AEB, self.TEST_CASES)
        return testcase_lists


class CPRA_Moving(TestScenario):

    CPRA_Moving_points_AEB = {4: 1, 8: 1}

    def __init__(self):
        super(CPRA_Moving, self).__init__()
        self.ScenarioName = 'CPRA_Moving'
        self.ScoreCalculator = ScoreCalculation.ZeroImpactBased(self.CPRA_Moving_points_AEB)
        self.ImpactSpeedCalculator = ImpactSpeedCalc.LinearMotionIterativeCalc()
        self.monte_carlo_method = monte_carlo_run_car_to_vru
        self.points_table = self.CPRA_Moving_points_AEB

    def prepare_test_list(self):
        testcase_lists = prepare_testcase_speed_based(self.CPRA_Moving_points_AEB, self.TEST_CASES)
        return testcase_lists

