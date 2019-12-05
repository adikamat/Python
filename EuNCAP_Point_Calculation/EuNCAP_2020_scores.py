import numpy as np
#
TEST_SPD = range(10, 85, 5)
OVERLAP = ['-50', '-75', '100', '75', '50']
COLOR_SCORE = {0: ["Green", 1.0], 1: ["Yellow", 0.75], 2: ["Orange", 0.5], 3: ["Brown", 0.25], 4: ["Red", 0.0]}

AEB_VRU_TS_SPD_TH = 40  # km/hr
AEB_VRU_MIN_SPD_REDUCTION = 20  # km/hr
FCW_TTC_TH = 1.70  # seconds

# Scenarios to run for EuNCAP 2020
scenarios_to_run = ['CCRs', 'CCRm', 'CCRs_FCW',
                    'CBNA', 'CBLA_50', 'CBLA_25', 'CBNAO', 'CBFA',
                    'CPFA_50', 'CPNA_25_Day', 'CPNA_25_Night',
                    'CPNC_50', 'CPNA_75_Day', 'CPNA_75_Night',
                    'CPLA_50_Day', 'CPLA_50_Night',
                    'CPRTO', 'CPLTO',
                    'CPRA_Static', 'CPRA_Moving',
                    'CPLA_25_Day', 'CPLA_25_Night']

# Dictionary with speed as key and list as values
# List contains thresholds (impact speed) for [Green, Yellow, Orange, Brown, Red] range
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

# Points Table
# Car-To-Car scenarios
CCRs_points_AEB = {10: 1, 15: 2, 20: 2, 25: 2, 30: 2, 35: 2, 40: 1, 45: 1, 50: 1}
CCRs_points_FCW = {30: 2, 35: 2, 40: 2, 45: 2, 50: 3, 55: 2, 60: 1, 65: 1, 70: 1, 75: 1, 80: 1}
CCRm_points_AEB = {30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1, 65: 2, 70: 2, 75: 2, 80: 2}
AEB_CCR_scenario_wt = {"AEB": 2.0, "FCW": 1.5}

# Car-To-Bicycle scenarios
CBNA_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}
CBFA_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}
CBNAO_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 1, 40: 1, 45: 1, 50: 1, 55: 1, 60: 1}
CBLA_points_AEB = {25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 1}
CBLA_points_FCW = {50: 3, 55: 3, 60: 1, 65: 1, 70: 1, 75: 1, 80: 1}
AEB_Cyclist_scenario_wt = {"CBFA": 3.0, "CBNA": 1.5, "CBNAO": 1.5, "CBLA": 3.0}

# Car-To-Pedestrian scenarios
CPFA_50_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}
CPNA_25_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}
CPNA_25_Night_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}
CPNA_75_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}
CPNA_75_Night_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}
CPNC_50_Day_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 2, 35: 3, 40: 3, 45: 3, 50: 2, 55: 2, 60: 1}
CPLA_50_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 3, 50: 3, 55: 3, 60: 2}
CPLA_25_points_AEB = {50: 3, 55: 3, 60: 2, 65: 1, 70: 1, 75: 1, 80: 1}
CPTA_Farside_points_AEB = {10: 1, 15: 1, 20: 1}
CPTA_Nearside_points_AEB = {10: 1}
CPRA_Static_points_AEB = {4: 1, 8: 1}
CPRA_Moving_points_AEB = {4: 1, 8: 1}
AEB_Pedestrian_scenario_wt = {"CPFA_50": 0.5,
                              "CPNA_25_Day": 0.25,
                              "CPNA_75_Day": 0.25,
                              "CPNC_50": 1.0,
                              "CPLA_Day": 1.0,
                              "CPTA": 1.0,
                              "CPRA": 2.0,
                              "CPNA_25_Night": 1.5,
                              "CPNA_75_Night": 1.5,
                              "CPLA_Night": 3.0}

# Dictionary for scenario name and points table mapping
points_table_dict = {"CBLA_50": CBLA_points_AEB,
                     "CBLA_25": CBLA_points_FCW,
                     "CBNA": CBNA_points_AEB,
                     "CBNAO": CBNAO_points_AEB,
                     "CBFA": CBFA_points_AEB,
                     "CPFA_50": CPFA_50_Day_points_AEB,
                     "CPNA_25_Day": CPNA_25_Day_points_AEB,
                     "CPNA_25_Night": CPNA_25_Night_points_AEB,
                     "CPNA_75_Day": CPNA_75_Day_points_AEB,
                     "CPNA_75_Night": CPNA_75_Night_points_AEB,
                     "CPNC_50": CPNC_50_Day_points_AEB,
                     "CPLA_50_Day": CPLA_50_points_AEB,
                     "CPLA_50_Night": CPLA_50_points_AEB,
                     "CPLA_25_Day": CPLA_25_points_AEB,
                     "CPLA_25_Night": CPLA_25_points_AEB,
                     "CPRTO": CPTA_Farside_points_AEB,
                     "CPLTO": CPTA_Nearside_points_AEB,
                     "CPRA_Static": CPRA_Static_points_AEB,
                     "CPRA_Moving": CPRA_Moving_points_AEB}


# Function to get the bin for given impact and test speed
def Car_to_Car_get_bin_score(impact_speed, test_speed, test_scenario):
    
    if impact_speed > test_speed:
        return COLOR_SCORE[4]
    
    if test_scenario == "CCRs" or test_scenario == "CCRs_FCW":
        threshold_dict = CCRs_impact_vel_th
    elif test_scenario == "CCRm":
        # Need to use relative impact speed for CCRm scenario
        # Speed of target vehicle is 20 kmph in same direction of motion of vehice under test
        impact_speed -= 20
        threshold_dict = CCRm_impact_vel_th
    elif test_scenario == "CCRb":
        # TODO
        threshold_dict = {}
    else:
        print "Unknown scenario " + test_scenario + " in EuNCAP 2020 Car_to_Car_get_bin_score"
        threshold_dict = {}
           
    if test_speed in threshold_dict.keys():
        impact_sp_threshold = threshold_dict[test_speed]
    else:
        print "Invalid test speed ", str(test_speed), " For scenario ", test_scenario
        impact_sp_threshold = {}
    
    try:
        index = next(x[0] for x in enumerate(impact_sp_threshold) if x[1] > impact_speed)
        # print index
        
    except StopIteration:
        # When no item found, return score 0, color red
        index = 4

    return COLOR_SCORE[index]
    
    
def Car_to_Vru_get_bin_score(impact_speed, test_speed, test_scenario):
    """
    For CBLA_FCW case, points are calculated from Warning TTC value. This value must be passed through the
    "impact_speed" function parameter.
    For all other Vru scenarios, impact speed is used for point calculation.
    """
    if test_scenario in ["CBLA_25", "CPLA_25_Day", "CPLA_25_Night"]:

        if test_scenario in points_table_dict:
            points_table = points_table_dict[test_scenario]
        else:
            print "Unexpected test scenario: " + test_scenario + " in EuNCAP 2020 Car_to_Vru_get_bin_score function"
            points_table = {}
        
        if impact_speed >= FCW_TTC_TH:
            score = points_table[test_speed]
        else:
            score = 0

    elif test_scenario in ["CPRTO", "CPLTO", "CPRA_Static", "CPRA_Moving"]:

        if test_scenario in points_table_dict:
            points_table = points_table_dict[test_scenario]
        else:
            print "Unexpected test scenario: " + test_scenario + " in EuNCAP 2020 Car_to_Vru_get_bin_score function"
            points_table = {}

        if impact_speed == 0:
            score = points_table[test_speed]
        else:
            score = 0
    else:
                                
        if test_scenario in points_table_dict:
            points_table = points_table_dict[test_scenario]
        else:
            print "Unexpected test scenario: " + test_scenario + " in EuNCAP 2020 Car_to_Vru_get_bin_score function"
            points_table = {}
            
        if test_speed <= AEB_VRU_TS_SPD_TH:
            score = ((test_speed - impact_speed) / test_speed) * points_table[test_speed]
        else: 
            score = points_table[test_speed] if (test_speed - impact_speed) >= AEB_VRU_MIN_SPD_REDUCTION else 0

    return ["NoColor", score]


def calculate_AEB_Pedestrian(testcase_datset):
    """
    :param testcase_datset: Dictionary with scenario string as keys and list of scores.
                            The elements in the list of scores is a dictionary with "SimScore" as key containing
                            list of scenario points for each run and "SimMaxScore" as key containing max available
                            points
    :return: The AEB pedestrian score for each simulation run
    """

    score_day = 0
    score_night = 0
    warn_list = []

    # Calculate and add pts for CPFA_50 scenario
    if "CPFA_50" in testcase_datset.keys():
        score_day = np.add(score_day, np.multiply(
            np.true_divide(testcase_datset["CPFA_50"]["SimScore"], testcase_datset["CPFA_50"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPFA_50"]))
    else:
        print "CPFA_50 scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPFA_50 scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPNA [25% and 75%] Day scenario
    if "CPNA_25_Day" in testcase_datset.keys():
        score_day = np.add(score_day, np.multiply(
            np.true_divide(testcase_datset["CPNA_25_Day"]["SimScore"], testcase_datset["CPNA_25_Day"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPNA_25_Day"]))
    else:
        print "CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPNA_25_Day scenario scores are missing for Pedestrian AEB calculation.")

    if "CPNA_75_Day" in testcase_datset.keys():
        score_day = np.add(score_day, np.multiply(
            np.true_divide(testcase_datset["CPNA_75_Day"]["SimScore"], testcase_datset["CPNA_75_Day"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPNA_75_Day"]))
    else:
        print "CPNA_75_Day scenario scores are missing for Pedestrian AEB calculation."

    # Calculate and add pts for CPNC_50 scenario
    if "CPNC_50" in testcase_datset.keys():
        score_day = np.add(score_day, np.multiply(
            np.true_divide(testcase_datset["CPNC_50"]["SimScore"], testcase_datset["CPNC_50"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPNC_50"]))
    else:
        print "CPNC_50 scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPNC_50 scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPLA [50% and 25%] Day scenario
    if "CPLA_50_Day" in testcase_datset.keys():
        cpla_total_pts = np.add(testcase_datset["CPLA_50_Day"]["SimScore"], testcase_datset["CPLA_25_Day"]["SimScore"])
        cpla_max_pts = testcase_datset["CPLA_50_Day"]["SimMaxScore"] + testcase_datset["CPLA_25_Day"]["SimMaxScore"]

        score_day = np.add(score_day,
                           np.multiply(np.true_divide(cpla_total_pts, cpla_max_pts),
                                       AEB_Pedestrian_scenario_wt["CPLA_Day"]))
    else:
        print "CPLA_50_Day scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPLA_50_Day scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPTA scenario
    if "CPRTO" in testcase_datset.keys() and "CPLTO" in testcase_datset.keys():
        cpta_score = np.add(testcase_datset["CPRTO"]["SimScore"], testcase_datset["CPLTO"]["SimScore"])
        cpta_max_score = np.add(testcase_datset["CPRTO"]["SimMaxScore"], testcase_datset["CPLTO"]["SimMaxScore"])
        score_day = np.add(score_day, np.multiply(np.true_divide(cpta_score, cpta_max_score),
                                                  AEB_Pedestrian_scenario_wt["CPTA"]))
    else:
        print "CPTA scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPTA scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPRA scenario
    if "CPRA" in testcase_datset.keys():
        cpra_score = np.add(testcase_datset["CPRA_Static"]["SimScore"], testcase_datset["CPRA_Moving"]["SimScore"])
        cpra_max_score = np.add(testcase_datset["CPRA_Static"]["SimMaxScore"], testcase_datset["CPTA_Moving"]["SimMaxScore"])
        score_day = np.add(score_day, np.multiply(np.true_divide(cpra_score, cpra_max_score),
                                                  AEB_Pedestrian_scenario_wt["CPRA"]))
    else:
        print "CPRA scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPRA scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPNA [25% and 75%] Night scenario
    if "CPNA_25_Night" in testcase_datset.keys():
        score_night = np.add(score_night, np.multiply(
            np.true_divide(testcase_datset["CPNA_25_Night"]["SimScore"],
                           testcase_datset["CPNA_25_Night"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPNA_25_Night"]))
    else:
        print "CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPNA_25_Night scenario scores are missing for Pedestrian AEB calculation.")

    if "CPNA_75_Night" in testcase_datset.keys():
        score_night = np.add(score_night, np.multiply(
            np.true_divide(testcase_datset["CPNA_75_Night"]["SimScore"],
                           testcase_datset["CPNA_75_Night"]["SimMaxScore"]),
            AEB_Pedestrian_scenario_wt["CPNA_75_Night"]))
    else:
        print "CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPNA_75_Night scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CPLA [50% and 25%] Night scenario
    if "CPLA_50_Night" in testcase_datset.keys():
        cpla_total_pts = np.add(testcase_datset["CPLA_50_Night"]["SimScore"],
                                testcase_datset["CPLA_25_Night"]["SimScore"])

        cpla_max_pts = testcase_datset["CPLA_50_Night"]["SimMaxScore"] + testcase_datset["CPLA_25_Night"]["SimMaxScore"]

        score_night = np.add(score_night, np.multiply(np.true_divide(cpla_total_pts, cpla_max_pts),
                                                      AEB_Pedestrian_scenario_wt["CPLA_Night"]))
    else:
        print "CPLA_50_Night scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CPLA_50_Night scenario scores are missing for Pedestrian AEB calculation.")

    return [np.add(score_day, score_night), 9, warn_list]  # Max 9 points available (6 for day, 3 for night)


def calculate_AEB_Cyclist(testcase_datset):
    """
        :param testcase_datset: Dictionary with scenario string as keys and list of scores.
                                The elements in the list of scores is a dictionary with "SimScore" as key containing
                                list of scenario points for each run and "SimMaxScore" as key containing max available
                                points
        :return: The AEB cyclist score for each simulation run
        """

    score = 0.0
    warn_list = []

    # Calculate and add pts for CBFA scenario
    if "CBFA" in testcase_datset.keys():
        score = np.add(score, np.multiply(
            np.true_divide(testcase_datset["CBFA"]["SimScore"], testcase_datset["CBFA"]["SimMaxScore"]),
            AEB_Cyclist_scenario_wt["CBFA"]))
    else:
        print "CBFA scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CBFA scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CBNA scenario
    if "CBNA" in testcase_datset.keys():
        score = np.add(score, np.multiply(
            np.true_divide(testcase_datset["CBNA"]["SimScore"], testcase_datset["CBNA"]["SimMaxScore"]),
            AEB_Cyclist_scenario_wt["CBNA"]))
    else:
        print "CBNA scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CBNA scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CBNAO scenario
    if "CBNAO" in testcase_datset.keys():
        score = np.add(score, np.multiply(
            np.true_divide(testcase_datset["CBNAO"]["SimScore"], testcase_datset["CBNAO"]["SimMaxScore"]),
            AEB_Cyclist_scenario_wt["CBNAO"]))
    else:
        print "CBNAO scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CBNAO scenario scores are missing for Pedestrian AEB calculation.")

    # Calculate and add pts for CBLA AEB and FCW scenario
    if "CBLA" in testcase_datset.keys():
        cbla_total_pts = np.add(testcase_datset["CBLA"]["SimScore"], testcase_datset["CBLA_25"]["SimScore"])
        cbla_max_pts = testcase_datset["CBLA"]["SimMaxScore"] + testcase_datset["CBLA_FCW"]["SimMaxScore"]

        score = np.add(score,
                       np.multiply(np.true_divide(cbla_total_pts, cbla_max_pts), AEB_Cyclist_scenario_wt["CBLA"]))
    else:
        print "CBLA scenario scores are missing for Pedestrian AEB calculation."
        warn_list.append("CBLA scenario scores are missing for Pedestrian AEB calculation.")

    return [score, 9, warn_list]  # Max 9 points available
