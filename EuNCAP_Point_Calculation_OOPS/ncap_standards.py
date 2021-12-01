import numpy as np
import re
import traceback
from collections import OrderedDict
from abc import ABCMeta, abstractmethod
from test_scenario import *
from testcase_name_ID_map import *
from Write_Output import *


def report_get_col_indices(row):

    REPORT_HEADER_STR_PREBRAKE = 'Measured activation TTC for PreBrakeLevel>=2'
    REPORT_HEADER_STR_DYNWARN = 'Measured activation TTC for DynAcuteWarning'
    REPORT_HEADER_STR_RESULT = 'Result'
    REPORT_HEADER_STR_TC_ID = 'Testcase ID'
    REPORT_HEADER_STR_TC_NAME = 'Testcase Name'
    REPORT_HEADER_STR_RECORDING = 'Recording'

    try:
        ttc_prebrake_idx = row.index(REPORT_HEADER_STR_PREBRAKE)
    except ValueError:
        print "Could not find the index for Prebrake TTC activation. " \
              "Change the header text to match the string used in the report file"

        raise RuntimeError("Column Heading Names for Prebrake TTC needs to be adapted "
                           "in script as per csv report")


    try:
        result_idx = row.index(REPORT_HEADER_STR_RESULT)
    except ValueError:
        print "Could not find the index for Result. " \
              "Change the header text to match the string used in the report file"

        raise RuntimeError("Column Heading Names need tobe adapted in script as per csv report")


    try:
        tc_id_idx = row.index(REPORT_HEADER_STR_TC_ID)
    except ValueError:
        print "Could not find the index for Testcase ID. " \
              "Change the header text to match the string used in the report file"

        raise RuntimeError("Column Heading Names for testcase ID needs to be adapted "
                           "in script as per csv report")


    try:
        testcase_name_idx = row.index(REPORT_HEADER_STR_TC_NAME)
    except ValueError:
        print "Could not find the index for Testcase Name. " \
              "Change the header text to match the string used in the report file"

        raise RuntimeError("Column Heading Names for Test case name needs to be adapted "
                           "in script as per csv report")


    try:
        rec_idx = row.index(REPORT_HEADER_STR_RECORDING)
    except ValueError:
        print "Could not find the index for Recording. " \
              "Change the header text to match the string used in the report file"

        raise RuntimeError("Column Heading Names for Recording Name needs to be adapted "
                           "in script as per csv report")


    try:
        dynAcWarn_idx = row.index(REPORT_HEADER_STR_DYNWARN)
    except ValueError:
        print "Could not find the index for Measured activation TTC for DynAcuteWarning." \
              "Change the header text to match the string used in the report file"
        # break

        dynAcWarn_idx = ttc_prebrake_idx
        # raise RuntimeError("Column Heading Names for DynAcute Warning TTC needs to be adapted "
        #                    "in script as per csv report")

    return [ttc_prebrake_idx,
            result_idx,
            tc_id_idx,
            testcase_name_idx,
            rec_idx,
            dynAcWarn_idx]


class NCAP_Standard:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = ''
        self.input_files = []
        self.AEB_Cyclist = 0
        self.AEB_Cyclist_max = 0
        self.AEB_Pedestrian = 0
        self.AEB_Pedestrian_max = 0
        self.list_of_scenarios = OrderedDict()
        self.missing_scenarios = []

    @abstractmethod
    def calc_stats(self):
        pass

    def print_stats(self):
        meanScoreTable = [["Scenario", "Minimum Points Scored", "Median Point",
                           "Maximum Points Scored", "Maximum Available Score"]]
        # String to print the result in tabular fashion
        final_score_str = '{0: <15}: {1}'.format('Scenario', 'Mean Score')
        for scenario_name, scenario_obj in self.list_of_scenarios.items():
            points = scenario_obj.SimScore
            max_points = scenario_obj.SimMaxScore
            final_score_str += '\n' + '{0: <15}: {1} out of {2}'.format(scenario_name, np.median(points), max_points)
            meanScoreTable.append([scenario_name, str(np.min(points)), str(np.median(points)),
                                   str(np.max(points)), str(max_points)])

        print "\n\nScores Scenario-wise:"
        print "========================================"
        print final_score_str
        print "========================================"

        print "AEB Pedestrian = " + str(np.median(self.AEB_Pedestrian)) + " out of " + str(self.AEB_Pedestrian_max)
        print "AEB Cyclist = " + str(np.median(self.AEB_Cyclist)) + " out of " + str(self.AEB_Cyclist_max)

        out_writer = WriteOutput.instance()
        out_writer.add_table_to_report("Scores Scenario-wise", "Point Scores Scenario-wise", meanScoreTable)
        out_writer.add_table_to_report("AEB Scores", "", [["Name", "Score"],
                                                          ["AEB Pedestrian",
                                                           str(np.median(self.AEB_Pedestrian)) + " out of " +
                                                           str(self.AEB_Pedestrian_max)],
                                                           ["AEB Cyclist",
                                                           str(np.median(self.AEB_Pedestrian)) + " out of " +
                                                           str(self.AEB_Pedestrian_max)]
                                                          ])

    def run_monte_carlo_sim(self):

        for scenario_name, scenario_obj in self.list_of_scenarios.items():
            scenario_obj.run_monte_carlo()

    # For CCRs_FCW, test cases for speed 30 kph to 50 kph are copied from CCRs scenario
    def copy_CCRs_testcases_to_CCRsFCW(self):
        for spd in range(30, 85, 5):
            testcase_30_to_50_kph = extract_key_value_pair("TestSpeed", spd,
                                                           self.list_of_scenarios["CCRs"].TEST_CASES)

            self.list_of_scenarios["CCRs_FCW"].TEST_CASES.extend(testcase_30_to_50_kph)

    def read_csv_report(self, input_files):

        testcases = {}
        missed_scenarios = []
        self.input_files = input_files
        for input_file in input_files:
            with open(input_file, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                line_count = 0

                for row in csv_reader:

                    if line_count == 0:
                        # Get the indices for all required columns
                        [ttc_prebrake_idx, result_idx, tc_id_idx,
                         testcase_name_idx, rec_idx, dynAcWarn_idx] = report_get_col_indices(row)

                    # First line is the header row. Start reading data from second row onwards
                    if line_count > 0:
                        # print row[testcase_name_idx]

                        if row[result_idx] != 'NOT ASSESSED':

                            # Get testcase name
                            if row[tc_id_idx] in TC_ID_MAP.keys():
                                tc_string = TC_ID_MAP[row[tc_id_idx]]
                            else:
                                print 'Missing entry for ID: ', row[tc_id_idx]
                                tc_string = ''

                            # Match regex to extract test case scenario, test speed, and overlap percentage
                            tc_scenario_res = re.search(TC_SCENARIO_REGEX, tc_string)
                            tc_fcw_res = re.search(TC_FCW_REGEX, tc_string)
                            tc_speed_res = re.search(TC_SPEED_REGEX, tc_string)
                            tc_overlap_res = re.search(TC_OVERLAP_REGEX, tc_string)
                            tc_day_night_res = re.search(TC_DAY_NIGHT_REGEX, tc_string)

                            # For each scenario, make a list of dictionary with all data
                            if tc_scenario_res is not None and tc_speed_res is not None:

                                # Read the test case scenario details
                                tc_scenario = tc_scenario_res.group(1)
                                tc_scenario = tc_scenario.replace('-', '_')
                                # tc_fcw = tc_fcw_res.group(1)
                                test_speed = tc_speed_res.group(1)
                                # tc_overlap_res = tc_scenario_res.group(2)
                                if tc_overlap_res is not None:
                                    # Read the whole match (e.g. 'pos50', 'neg75')
                                    tc_overlap = tc_overlap_res.group(1)
                                    # if '-' not in tc_overlap:
                                    #     tc_overlap = '+' + tc_overlap
                                    # Replace 'neg' with '-' and 'pos' with "+"
                                    # tc_overlap = tc_overlap.replace('pos', '+')
                                    # tc_overlap = tc_overlap.replace('neg', '-')
                                else:
                                    tc_overlap = '100'

                                if tc_fcw_res is not None:
                                    tc_scenario = tc_scenario + "_FCW"

                                if tc_day_night_res is not None:
                                    if tc_day_night_res.group(1) is not None:
                                        tc_scenario = tc_scenario + "_Day"
                                    elif tc_day_night_res.group(2) is not None:
                                        tc_scenario = tc_scenario + "_Night"

                                testcases.setdefault(tc_scenario, [])

                                try:
                                    prebrake_ttc = float(row[ttc_prebrake_idx])

                                except ValueError:
                                    # For entries with blanks or "N/A", prebrake_ttc is set to 0
                                    # This means that the testcase will fail and will be awarded 0 points (red region).
                                    prebrake_ttc = 0

                                try:
                                    warn_TTC = float(row[dynAcWarn_idx])

                                except ValueError:
                                    # For entries with blanks or "N/A", prebrake_ttc is set to 0
                                    # This means that the testcase will fail and will be awarded 0 points (red region).
                                    warn_TTC = 0

                                tc_dict = {"TestSpeed": float(test_speed),
                                           "Overlap": tc_overlap,
                                           "ImpactSpeed": float(test_speed),
                                           "TestCaseID": row[tc_id_idx],
                                           "Recording": row[rec_idx],
                                           "MeasuredTTC": prebrake_ttc,
                                           "MeasuredWarnTTC": warn_TTC}

                                testcases[tc_scenario].append(tc_dict)
                                if tc_scenario in self.list_of_scenarios.keys():
                                    self.list_of_scenarios[tc_scenario].add_test_case(tc_dict)
                                else:
                                    if tc_scenario not in self.missing_scenarios:
                                        self.missing_scenarios.append(tc_scenario)
                            else:
                                print "Testcase name does not match regex: " + row[testcase_name_idx]

                        # print row[1]
                    line_count += 1
                    # break

            print 'Processed  ', str(line_count), ' lines from', input_file
            # print 'Found ', str(ccr_scenario_count) , ' car-to-car scenarios'

        self.copy_CCRs_testcases_to_CCRsFCW()

        # Get Output writer instance
        out_writer = WriteOutput.instance()

        # Print list of test scenario with no. of test cases
        numTests = [len(testcases[k]) for k in testcases.keys()]
        table_rows = [["Scenario", "No. of Test Cases"]]
        print "\nScenario       : No. of Test Cases"
        for i, k in enumerate(testcases.keys()):
            print '{0: <21}: {1}'.format(k, numTests[i])
            table_rows.append([str(k), str(numTests[i])])
        print "\n"
        out_writer.add_table_to_report("Test Case Details", "Test Case per scenario", table_rows)

        print "Following scenarios were found in report but not included in scenario list for", self.name, "standard"
        table_rows = [["Sr No.", "Scenario Name"]]
        for i, k in enumerate(self.missing_scenarios):
            print '{0:}: {1}'.format(i+1, k)
            table_rows.append([str(i+1), str(k)])
        print "\n"
        if len(table_rows) > 0:
            out_writer.add_table_to_report("Extra Scenario",
                                           "Following scenarios were found in report but not included in "
                                           "scenario list for" + self.name + "standard",
                                           table_rows)

        # return testcases


class EuNCAP_2018(NCAP_Standard):

    def __init__(self):

        super(EuNCAP_2018, self).__init__()
        self.name = 'EuNCAP_2018'
        self.list_of_scenarios = OrderedDict([('CCRs', CCRs()),
                                              ('CCRm', CCRm()),
                                              ('CCRs_FCW', CCRs_FCW()),
                                              ('CBNA', CBNA()),
                                              ('CBLA_50', CBLA_AEB()),
                                              ('CBLA_25', CBLA_FCW()),
                                              ('CPFA_50', CPFA_50_Day()),
                                              ('CPNA_25_Day', CPNA_25_Day()),
                                              ('CPNA_25_Night', CPNA_25_Night()),
                                              ('CPNC_50', CPNC_50_Day()),
                                              ('CPNA_75_Day', CPNA_75_Day()),
                                              ('CPNA_75_Night', CPNA_75_Night()),
                                              ('CPLA_50_Day', CPLA_50_Day()),
                                              ('CPLA_50_Night', CPLA_50_Night()),
                                              ('CPLA_25_Day', CPLA_25_Day()),
                                              ('CPLA_25_Night', CPLA_25_Night())
                                              ])

        self.AEB_Cyclist = 0
        self.AEB_Cyclist_max = 0
        self.AEB_Pedestrian = 0
        self.AEB_Pedestrian_max = 0

    def calculate_AEB_Pedestrian(self):
        """

        :return: The AEB pedestrian score for each simulation run
        """

        score_day = 0
        score_night = 0
        warn_list = []

        # Calculate and add pts for CPFA_50 scenario
        if "CPFA_50" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPFA_50'].SimScore
            max_points = self.list_of_scenarios['CPFA_50'].SimMaxScore
            score_day = np.add(score_day, np.true_divide(points, max_points))
        else:
            print "CPFA_50 scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPFA_50 scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPNA [25% and 75%] Day scenario
        if "CPNA_25_Day" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Day'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Day'].SimMaxScore
            score_day = np.add(score_day, np.true_divide(points, max_points))
        else:
            print "CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation.")

        if "CPNA_75_Day" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_75_Day'].SimScore
            max_points = self.list_of_scenarios['CPNA_75_Day'].SimMaxScore
            score_day = np.add(score_day, np.true_divide(points, max_points))
        else:
            print "CPNA_75_Day scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_75_Day scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPNC_50 scenario
        if "CPNC_50" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNC_50'].SimScore
            max_points = self.list_of_scenarios['CPNC_50'].SimMaxScore
            score_day = np.add(score_day, np.true_divide(points, max_points))
        else:
            print "CPNC_50 scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNC_50 scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPLA [50% and 25%] Day scenario
        if "CPLA_50_Day" in self.list_of_scenarios.keys() and "CPLA_25_Day" in self.list_of_scenarios.keys():
            points_50 = self.list_of_scenarios['CPLA_50_Day'].SimScore
            max_points_50 = self.list_of_scenarios['CPLA_50_Day'].SimMaxScore
            points_25 = self.list_of_scenarios['CPLA_25_Day'].SimScore
            max_points_25 = self.list_of_scenarios['CPLA_25_Day'].SimMaxScore

            cpla_total_pts = np.add(points_50, points_25)
            cpla_max_pts = max_points_50 + max_points_25

            score_day = np.add(score_day, np.true_divide(cpla_total_pts, cpla_max_pts))
        else:
            print "CPLA_50_Day scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPLA_50_Day scenario scores are missing for Pedestrian AEB calculation.")

        score_day_avg = score_day * 3 / 5  # 3 maximum points for night test cases and averaged over 5 scenarios

        # Calculate and add pts for CPNA [25% and 75%] Night scenario
        if "CPNA_25_Night" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore
            score_night = np.add(score_night, np.true_divide(points, max_points))
        else:
            print "CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation.")

        if "CPNA_75_Night" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore
            score_night = np.add(score_night, np.true_divide(points, max_points))
        else:
            print "CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPLA [50% and 25%] Night scenario
        if "CPLA_50_Night" in self.list_of_scenarios.keys() and "CPLA_25_Day" in self.list_of_scenarios.keys():
            points_50 = self.list_of_scenarios['CPLA_50_Night'].SimScore
            max_points_50 = self.list_of_scenarios['CPLA_50_Night'].SimMaxScore
            points_25 = self.list_of_scenarios['CPLA_25_Day'].SimScore
            max_points_25 = self.list_of_scenarios['CPLA_25_Day'].SimMaxScore

            cpla_total_pts = np.add(points_50, points_25)
            cpla_max_pts = max_points_50 + max_points_25

            score_night = np.add(score_night, np.true_divide(cpla_total_pts, cpla_max_pts))
        else:
            print "CPLA_50_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPLA_50_Night scenario scores are missing for Pedestrian AEB calculation.")

        score_night_avg = score_night * 3 / 3  # 3 maximum points for night test cases and averaged over 3 scenarios

        return [np.add(score_day_avg, score_night_avg), 6, warn_list]

    def calculate_AEB_Cyclist(self):
        """

        :return:
        """
        score = 0.0
        warn_list = []

        # Calculate and add pts for CBNA scenario
        if "CBNA" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore
            score = np.add(score, np.true_divide(points, max_points))
        else:
            print "CBNA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBNA scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CBLA AEB and FCW scenario
        if "CBLA_50" in self.list_of_scenarios.keys() and "CBLA_25" in self.list_of_scenarios.keys():
            points_50 = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points_50 = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore
            points_25 = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points_25 = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore

            cbla_total_pts = np.add(points_50, points_25)
            cbla_max_pts = max_points_50 + max_points_25

            score = np.add(score, np.true_divide(cbla_total_pts, cbla_max_pts))
        else:
            print "CBLA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBLA scenario scores are missing for Pedestrian AEB calculation.")

        return [score * 6 / 2, 6,
                warn_list]  # 6 maximum points for AEB Cyclist and score averaged over CBNA and CBLA scenarios

    def calc_stats(self):
        print "\nRunning Monte-Carlo Simulations for each scenario"
        self.run_monte_carlo_sim()

        out_writer = WriteOutput.instance()

        print "\nCombining scores for Bicycle scenarios"
        # Calculate AEB score for Bicycle
        self.AEB_Cyclist, self.AEB_Cyclist_max, Cyclist_warnings = self.calculate_AEB_Cyclist()
        if len(Cyclist_warnings) > 0:
            out_writer.add_to_warn_list(Cyclist_warnings)

        print "\nCombining scores for Pedestrian scenarios"
        # Calculate AEB score for Pedestrian
        self.AEB_Pedestrian, self.AEB_Pedestrian_max, Ped_warnings = self.calculate_AEB_Pedestrian()
        if len(Ped_warnings) > 0:
            out_writer.add_to_warn_list(Ped_warnings)


class EuNCAP_2020(NCAP_Standard):

    def __init__(self):

        super(EuNCAP_2020, self).__init__()
        self.name = 'EuNCAP_2020'
        self.list_of_scenarios = OrderedDict([('CCRs', CCRs()),
                                              ('CCRm', CCRm()),
                                              ('CCRs_FCW', CCRs_FCW()),
                                              ('CBNA', CBNA()),
                                              ('CBLA_50', CBLA_AEB()),
                                              ('CBLA_25', CBLA_FCW()),
                                              ('CBNAO', CBNAO()),
                                              ('CBFA', CBFA()),
                                              ('CPFA_50', CPFA_50_Day()),
                                              ('CPNA_25_Day', CPNA_25_Day()),
                                              ('CPNA_25_Night', CPNA_25_Night()),
                                              ('CPNC_50', CPNC_50_Day()),
                                              ('CPNA_75_Day', CPNA_75_Day()),
                                              ('CPNA_75_Night', CPNA_75_Night()),
                                              ('CPLA_50_Day', CPLA_50_Day()),
                                              ('CPLA_50_Night', CPLA_50_Night()),
                                              ('CPRTO', CPRTO()),
                                              ('CPLTO', CPLTO()),
                                              ('CPLA_25_Day', CPLA_25_Day()),
                                              ('CPLA_25_Night', CPLA_25_Night()),
                                              ('CPRA_Static', CPRA_Static()),
                                              ('CPRA_Moving', CPRA_Moving())
                                              ])

        self.AEB_Pedestrian_scenario_wt = {"CPFA_50": 0.5,
                                           "CPNA_25_Day": 0.25,
                                           "CPNA_75_Day": 0.25,
                                           "CPNC_50": 1.0,
                                           "CPLA_Day": 1.0,
                                           "CPTA": 1.0,
                                           "CPRA": 2.0,
                                           "CPNA_25_Night": 1.0,
                                           "CPNA_75_Night": 1.0,
                                           "CPLA_Night": 1.0}

        self.AEB_Cyclist_scenario_wt = {"CBFA": 3.0, "CBNA": 1.5, "CBNAO": 1.5, "CBLA": 3.0}

        self.AEB_Cyclist = 0
        self.AEB_Cyclist_max = 0
        self.AEB_Pedestrian = 0
        self.AEB_Pedestrian_max = 0

    def calculate_AEB_Pedestrian(self):
        """
        :return: The AEB pedestrian score for each simulation run
        """

        score_day = 0.0
        score_night = 0.0
        warn_list = []

        # Calculate and add pts for CPFA_50 scenario
        if "CPFA_50" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPFA_50'].SimScore
            max_points = self.list_of_scenarios['CPFA_50'].SimMaxScore
            score_day = np.add(score_day, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPFA_50"]))
        else:
            print "CPFA_50 scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPFA_50 scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPNA [25% and 75%] Day scenario
        if "CPNA_25_Day" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Day'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Day'].SimMaxScore
            score_day = np.add(score_day, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPNA_25_Day"]))
        else:
            print "CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation.")

        if "CPNA_75_Day" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_75_Day'].SimScore
            max_points = self.list_of_scenarios['CPNA_75_Day'].SimMaxScore
            score_day = np.add(score_day, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPNA_75_Day"]))
        else:
            print "CPNA_75_Day scenario scores are missing for Pedestrian AEB calculation."

        # Calculate and add pts for CPNC_50 scenario
        if "CPNC_50" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNC_50'].SimScore
            max_points = self.list_of_scenarios['CPNC_50'].SimMaxScore
            score_day = np.add(score_day, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPNC_50"]))
        else:
            print "CPNC_50 scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNC_50 scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPLA [50% and 25%] Day scenario
        if "CPLA_50_Day" in self.list_of_scenarios.keys() and "CPLA_25_Day" in self.list_of_scenarios.keys():
            points_50 = self.list_of_scenarios['CPLA_50_Day'].SimScore
            max_points_50 = self.list_of_scenarios['CPLA_50_Day'].SimMaxScore
            points_25 = self.list_of_scenarios['CPLA_25_Day'].SimScore
            max_points_25 = self.list_of_scenarios['CPLA_25_Day'].SimMaxScore

            cpla_total_pts = np.add(points_50, points_25)
            cpla_max_pts = max_points_50 + max_points_25

            score_day = np.add(score_day,
                               np.multiply(np.true_divide(cpla_total_pts, cpla_max_pts),
                                           self.AEB_Pedestrian_scenario_wt["CPLA_Day"]))
        else:
            print "CPLA_Day scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPLA_Day scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPTA scenario
        if "CPRTO" in self.list_of_scenarios.keys() and "CPLTO" in self.list_of_scenarios.keys():

            points_r = self.list_of_scenarios['CPRTO'].SimScore
            max_points_r = self.list_of_scenarios['CPRTO'].SimMaxScore
            points_l = self.list_of_scenarios['CPLTO'].SimScore
            max_points_l = self.list_of_scenarios['CPLTO'].SimMaxScore

            cpta_score = np.add(points_r, points_l)
            cpta_max_score = np.add(max_points_r, max_points_l)
            score_day = np.add(score_day, np.multiply(np.true_divide(cpta_score, cpta_max_score),
                                                      self.AEB_Pedestrian_scenario_wt["CPTA"]))
        else:
            print "CPTA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPTA scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPRA scenario
        if "CPRA_Static" in self.list_of_scenarios.keys() and "CPRA_Moving" in self.list_of_scenarios.keys():
            points_static = self.list_of_scenarios['CPRA_Static'].SimScore
            max_points_static = self.list_of_scenarios['CPRA_Static'].SimMaxScore
            points_moving = self.list_of_scenarios['CPRA_Moving'].SimScore
            max_points_moving = self.list_of_scenarios['CPRA_Moving'].SimMaxScore

            cpra_score = np.add(points_static, points_moving)
            cpra_max_score = np.add(max_points_static, max_points_moving)

            score_day = np.add(score_day, np.multiply(np.true_divide(cpra_score, cpra_max_score),
                                                      self.AEB_Pedestrian_scenario_wt["CPRA"]))
        else:
            print "CPRA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPRA scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPNA [25% and 75%] Night scenario
        if "CPNA_25_Night" in self.list_of_scenarios.keys():
            points = self.list_of_scenarios['CPNA_25_Night'].SimScore
            max_points = self.list_of_scenarios['CPNA_25_Night'].SimMaxScore
            score_night = np.add(score_night, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPNA_25_Night"]))
        else:
            print "CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation.")

        if "CPNA_75_Night" in self.list_of_scenarios.keys():

            points = self.list_of_scenarios['CPNA_75_Night'].SimScore
            max_points = self.list_of_scenarios['CPNA_75_Night'].SimMaxScore
            score_night = np.add(score_night, np.multiply(
                np.true_divide(points, max_points), self.AEB_Pedestrian_scenario_wt["CPNA_75_Night"]))

        else:
            print "CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CPLA [50% and 25%] Night scenario
        if "CPLA_50_Night" in self.list_of_scenarios.keys() and \
                'CPLA_25_Night' in self.list_of_scenarios.keys():

            points_50 = self.list_of_scenarios['CPLA_50_Night'].SimScore
            max_points_50 = self.list_of_scenarios['CPLA_50_Night'].SimMaxScore
            points_25 = self.list_of_scenarios['CPLA_25_Night'].SimScore
            max_points_25 = self.list_of_scenarios['CPLA_25_Night'].SimMaxScore

            cpla_total_pts = np.add(points_50, points_25)
            cpla_max_pts = max_points_50 + max_points_25

            score_night = np.add(score_night, np.multiply(np.true_divide(cpla_total_pts, cpla_max_pts),
                                                          self.AEB_Pedestrian_scenario_wt["CPLA_Night"]))
        else:
            print "CPLA_Night scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CPLA_Night scenario scores are missing for Pedestrian AEB calculation.")

        AEB_ped_max_pts = sum(self.AEB_Pedestrian_scenario_wt.values())
        return [np.add(score_day, score_night), AEB_ped_max_pts, warn_list]  # Max 9 points available (6 for day, 3 for night)

    def calculate_AEB_Cyclist(self):
        """

        :return: The AEB cyclist score for each simulation run
        """
        score = 0.0
        warn_list = []

        # Calculate and add pts for CBFA scenario
        if "CBFA" in self.list_of_scenarios.keys():

            points = self.list_of_scenarios['CBFA'].SimScore
            max_points = self.list_of_scenarios['CBFA'].SimMaxScore
            score = np.add(score, np.multiply(
                np.true_divide(points, max_points), self.AEB_Cyclist_scenario_wt["CBFA"]))
        else:
            print "CBFA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBFA scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CBNA scenario
        if "CBNA" in self.list_of_scenarios.keys():

            points = self.list_of_scenarios['CBNA'].SimScore
            max_points = self.list_of_scenarios['CBNA'].SimMaxScore
            score = np.add(score, np.multiply(
                np.true_divide(points, max_points), self.AEB_Cyclist_scenario_wt["CBNA"]))
        else:
            print "CBNA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBNA scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CBNAO scenario
        if "CBNAO" in self.list_of_scenarios.keys():

            points = self.list_of_scenarios['CBNAO'].SimScore
            max_points = self.list_of_scenarios['CBNAO'].SimMaxScore
            score = np.add(score, np.multiply(
                np.true_divide(points, max_points), self.AEB_Cyclist_scenario_wt["CBNAO"]))
        else:
            print "CBNAO scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBNAO scenario scores are missing for Pedestrian AEB calculation.")

        # Calculate and add pts for CBLA AEB and FCW scenario
        if "CBLA_50" in self.list_of_scenarios.keys() and "CBLA_25" in self.list_of_scenarios.keys():

            points_50 = self.list_of_scenarios['CBLA_50'].SimScore
            max_points_50 = self.list_of_scenarios['CBLA_50'].SimMaxScore
            points_25 = self.list_of_scenarios['CBLA_25'].SimScore
            max_points_25 = self.list_of_scenarios['CBLA_25'].SimMaxScore

            cbla_total_pts = np.add(points_50, points_25)
            cbla_max_pts = max_points_50 + max_points_25

            score = np.add(score, np.multiply(
                np.true_divide(cbla_total_pts, cbla_max_pts), self.AEB_Cyclist_scenario_wt["CBLA"]))
        else:
            print "CBLA scenario scores are missing for Pedestrian AEB calculation."
            warn_list.append("CBLA scenario scores are missing for Pedestrian AEB calculation.")

        AEB_cyc_max_pts = sum(self.AEB_Cyclist_scenario_wt.values())
        return [score, AEB_cyc_max_pts, warn_list]  # Max 9 points available

    def calc_stats(self):
        print "\nRunning Monte-Carlo Simulations for each scenario"
        self.run_monte_carlo_sim()

        out_writer = WriteOutput.instance()

        print "\nCombining scores for Bicycle scenarios"
        # Calculate AEB score for Bicycle
        self.AEB_Cyclist, self.AEB_Cyclist_max, Cyclist_warnings = self.calculate_AEB_Cyclist()
        if len(Cyclist_warnings) > 0:
            out_writer.add_to_warn_list(Cyclist_warnings)

        print "\nCombining scores for Pedestrian scenarios"
        # Calculate AEB score for Pedestrian
        self.AEB_Pedestrian, self.AEB_Pedestrian_max, Ped_warnings = self.calculate_AEB_Pedestrian()
        if len(Ped_warnings) > 0:
            out_writer.add_to_warn_list(Ped_warnings)


class JNCAP_2018(NCAP_Standard):

    def __init__(self):

        super(JNCAP_2018, self).__init__()
        self.name = 'JNCAP_2018'
        scenarios_to_run = ['CCRs', 'CCRm', 'CCRs_FCW', 'CCRm_FCW',
                            'CPNA_5_50_Day', 'CPNAO_5_50_Day',
                            'CPFA_1LX_5_50_Night', 'CPFA_15LX_5_50_Night',
                            'CPFAO_1LX_5_50_Night', 'CPFAO_15LX_5_50_Night',
                            'CPNA_5_25_Day', 'CPNA_5_75_Day', 'CPNA_8_50_Day', 'CPNC_5_50_Day',
                            'CPNAO_5_25_Day', 'CPNAO_5_75_Day', 'CPNAO_8_50_Day', 'CPNCO_5_50_Day',
                            'CPFA_15LX_5_25_Night', 'CPFA_15LX_5_75_Night', 'CPFA_15LX_8_50_Night',
                            'CPFAO_15LX_5_25_Night', 'CPFAO_15LX_5_75_Night', 'CPFAO_15LX_8_50_Night',
                            'CPFA_1LX_5_25_Night', 'CPFA_1LX_5_75_Night', 'CPFA_1LX_8_50_Night',
                            'CPFAO_1LX_5_25_Night', 'CPFAO_1LX_5_75_Night', 'CPFAO_1LX_8_50_Night',
                            ]

        self.list_of_scenarios = {'CCRs': CCRs(),
                                  'CCRm': CCRm(),
                                  'CCRs_FCW': CCRs(),
                                  'CBNA': CBNA(),
                                  'CBLA_50': CBLA_AEB(),
                                  'CBLA_25': CBLA_FCW(),
                                  'CBFA': CBFA(),
                                  'CPFA_50': CPFA_50_Day(),
                                  'CPNA_25_Day': CPNA_25_Day(),
                                  'CPNA_25_Night': CPNA_25_Night(),
                                  'CPNC_50': CPNC_50_Day(),
                                  'CPNA_75_Day': CPNA_75_Day(),
                                  'CPNA_75_Night': CPNA_75_Night(),
                                  'CPLA_50_Day': CPLA_50_Day(),
                                  'CPLA_50_Night': CPLA_50_Night(),
                                  'CPRTO': CPRTO(),
                                  'CPLTO': CPLTO(),
                                  'CPLA_25_Day': CPLA_25_Day(),
                                  'CPLA_25_Night': CPLA_25_Night(),
                                  'CPRA_Static': CPRA_Static(),
                                  'CPRA_Moving': CPRA_Moving(),
                                  'CBNAO': CBNAO()
                                  }

    def calc_stats(self):
        pass