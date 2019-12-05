import numpy as np

DAY_REPRESENTATIVE_SPD = 40
NIGHT_REPRESENTATIVE_SPD = 40  # 45 <- Currently using 40 as per usecase reports

LAP_RATIO = 0.6
PED_SPEED = 0.9
TARGET = 0.9
AEB_FCW = 'AEB+FCW'
AEB_WT = 1 if AEB_FCW == "AEB+FCW" else 0.5

# Scenarios to run for JNCAP 2020
# Do not change order. Order is set as per full test range run test-cases first, then only for representative speed
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

# Re-mapping of scenarios (workaround) for JNCAP testcases
remapped_name = {'CCRs_FCW': 'CCRs',
                 'CCRm_FCW': 'CCRm',
                 'CPNA_5_75_Day': 'CPNA_5_25_Day',
                 'CPNA_8_50_Day': 'CPNA_5_25_Day',
                 'CPNC_5_50_Day': 'CPNA_5_25_Day',
                 'CPFA_15LX_5_25_Night': 'CPFA_50',
                 'CPFA_15LX_5_75_Night': 'CPFA_50',
                 'CPFA_15LX_8_50_Night': 'CPFA_50',
                 'CPFA_15LX_5_50_Night': 'CPFA_50',
                 'CPFA_1LX_5_50_Night': 'CPFA_50',
                 'CPFAO_15LX_5_50_Night': 'CPFA_50',
                 'CPFAO_1LX_5_50_Night': 'CPFA_50',
                 }

# Points Table
# Car-To-Car scenarios
CCRs_points_AEB = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 1.5, 50: 1}
CCRs_points_FCW = {10: 1, 15: 1, 20: 1, 25: 1, 30: 1, 35: 2, 40: 2, 45: 1.5, 50: 1, 55: 0.5, 60: 0.5}
CCRm_points_AEB = {35: 0.5, 40: 0.5, 45: 1, 50: 1, 55: 0.5, 60: 0.5}
CCRm_points_FCW = {35: 0.5, 40: 0.5, 45: 1, 50: 1, 55: 0.5, 60: 0.5}

# Car-To-Pedestrian scores
CPN_Day = {10: 1, 15: 1, 20: 2, 25: 2, 30: 2, 35: 3, 40: 3, 45: 2, 50: 2, 55: 1, 60: 1}
CPNO_Day = {25: 1, 30: 1, 35: 1, 40: 1, 45: 1}
CPF_Night_15LX = {30: 2, 35: 4, 40: 6, 45: 6, 50: 6, 55: 5, 60: 3}
CPFO_Night_15LX = {30: 1, 35: 1, 40: 1, 45: 2, 50: 1, 55: 1, 60: 1}
CPF_Night_1LX = {30: 1, 35: 2, 40: 2, 45: 2, 50: 2, 55: 2, 60: 1}
CPFO_Night_1LX = {40: 1, 45: 1, 50: 1}

#
# Dictionary for scenario name and points table mapping
points_table_dict = {"CCRs": CCRs_points_AEB,
                     "CCRs_FCW": CCRs_points_FCW,
                     "CCRm": CCRm_points_AEB,
                     "CCRm_FCW": CCRm_points_FCW,
                     "CPNA_5_50_Day": CPN_Day,
                     "CPNA_5_25_Day": CPN_Day,
                     "CPNA_5_75_Day": CPN_Day,
                     "CPNA_8_50_Day": CPN_Day,
                     "CPNC_5_50_Day": CPN_Day,
                     "CPNAO_5_50_Day": CPNO_Day,
                     "CPNAO_5_25_Day": CPNO_Day,
                     "CPNAO_5_75_Day": CPNO_Day,
                     "CPNAO_8_50_Day": CPNO_Day,
                     "CPNCO_5_50_Day": CPNO_Day,
                     "CPFA_1LX_5_50_Night": CPF_Night_1LX,
                     "CPFA_1LX_5_25_Night": CPF_Night_1LX,
                     "CPFA_1LX_5_75_Night": CPF_Night_1LX,
                     "CPFA_1LX_8_50_Night": CPF_Night_1LX,
                     "CPFAO_1LX_5_50_Night": CPFO_Night_1LX,
                     "CPFAO_1LX_5_25_Night": CPFO_Night_1LX,
                     "CPFAO_1LX_5_75_Night": CPFO_Night_1LX,
                     "CPFAO_1LX_8_50_Night": CPFO_Night_1LX,
                     "CPFA_15LX_5_50_Night": CPF_Night_15LX,
                     "CPFA_15LX_5_25_Night": CPF_Night_15LX,
                     "CPFA_15LX_5_75_Night": CPF_Night_15LX,
                     "CPFA_15LX_8_50_Night": CPF_Night_15LX,
                     "CPFAO_15LX_5_50_Night": CPFO_Night_15LX,
                     "CPFAO_15LX_5_25_Night": CPFO_Night_15LX,
                     "CPFAO_15LX_5_75_Night": CPFO_Night_15LX,
                     "CPFAO_15LX_8_50_Night": CPFO_Night_15LX}


# Scenario Weights
scenario_wt_dict = {'CPNA_5_25_Day': 0.2,
                    'CPNA_5_75_Day': 0.2,
                    'CPNA_8_50_Day': 0.1,
                    'CPNC_5_50_Day': 0.1,
                    'CPNAO_5_25_Day': 0.2,
                    'CPNAO_5_75_Day': 0.2,
                    'CPNAO_8_50_Day': 0.1,
                    'CPNCO_5_50_Day': 0.1,
                    'CPFA_1LX_5_25_Night': 0.2,
                    'CPFA_1LX_5_75_Night': 0.2,
                    'CPFA_1LX_8_50_Night': 0.1,
                    'CPFAO_1LX_5_25_Night': 0.2,
                    'CPFAO_1LX_5_75_Night': 0.2,
                    'CPFAO_1LX_8_50_Night': 0.1,
                    'CPFA_15LX_5_25_Night': 0.2,
                    'CPFA_15LX_5_75_Night': 0.2,
                    'CPFA_15LX_8_50_Night': 0.1,
                    'CPFAO_15LX_5_25_Night': 0.2,
                    'CPFAO_15LX_5_75_Night': 0.2,
                    'CPFAO_15LX_8_50_Night': 0.1}


# Function to get the bin for given impact and test speed
def get_bin_score(rel_coll_spd, initial_speed, test_scenario):

    decel_rate = (initial_speed - rel_coll_spd) / initial_speed

    if test_scenario in points_table_dict.keys():
        tc_score = decel_rate * points_table_dict[test_scenario][initial_speed]
    else:
        print "Unexpected test scenario: " + test_scenario + " in JNCAP Car_to_Vru_get_bin_score function"
        tc_score = 0

    return [decel_rate, tc_score]


def Car_to_Car_get_bin_score(rel_coll_spd, initial_speed, test_scenario):
    decel_rate, score = get_bin_score(rel_coll_spd, initial_speed, test_scenario)
    return [decel_rate, score]


# Function to get the score for given impact and test speed
def Car_to_Vru_get_bin_score(rel_coll_spd, initial_speed, test_scenario):
    decel_rate, score = get_bin_score(rel_coll_spd, initial_speed, test_scenario)
    return [decel_rate, score]


def calculate_car_to_car_score(sim_run_results):
    """
        :param sim_run_results: Dictionary with scenario string as keys and dict of scores.
                                The elements in the dict of scores are key containing
                                speed and value is again a dictionary with "Decel" and "ColorScore"
        :return: The AEB pedestrian score for each simulation run
        """

    CCRs_res = sim_run_results['CCRs']
    CCRs_AEB_points = sum([tc_res["ColorScore"] for tc_res in CCRs_res.values()])

    CCRs_FCW_res = sim_run_results['CCRs_FCW']
    CCRs_FCW_points = sum([tc_res["ColorScore"] for tc_res in CCRs_FCW_res.values()])

    CCRs_final_score =  CCRs_AEB_points + CCRs_FCW_points

    CCRm_res = sim_run_results['CCRm']
    CCRm_AEB_points = sum([tc_res["ColorScore"] for tc_res in CCRm_res.values()])

    CCRm_FCW_res = sim_run_results['CCRm_FCW']
    CCRm_FCW_points = sum([tc_res["ColorScore"] for tc_res in CCRm_FCW_res.values()])

    CCRm_final_score = CCRm_AEB_points + CCRm_FCW_points

    return [CCRs_final_score, CCRm_final_score]



def calculate_score(adult_50_5_res, adult_25_5_res, adult_75_5_res, adult_50_8_res, child_50_5_res):

    adult_50_5_sum = sum([tc_res["ColorScore"] for tc_res in adult_50_5_res.values()]) * AEB_WT
    adult_25_5_sum = sum([tc_res["ColorScore"] for tc_res in adult_25_5_res.values()]) * AEB_WT
    adult_75_5_sum = sum([tc_res["ColorScore"] for tc_res in adult_75_5_res.values()]) * AEB_WT
    adult_50_8_sum = sum([tc_res["ColorScore"] for tc_res in adult_50_8_res.values()]) * AEB_WT

    partial_lap_ratio = (adult_50_5_sum * LAP_RATIO) + adult_25_5_sum + adult_75_5_sum
    partial_ped_score = (adult_50_5_sum * PED_SPEED) + adult_50_8_sum

    if child_50_5_res is not None:
        child_50_5_sum = sum([tc_res["ColorScore"] for tc_res in child_50_5_res.values()]) * AEB_WT
        partial_ped_type = (adult_50_5_sum * TARGET) + child_50_5_sum
    else:
        partial_ped_type = 1

    if adult_50_5_sum == 0:
        final_score = 0
    else:
        final_score = partial_lap_ratio * partial_ped_score * partial_ped_type / adult_50_5_sum**2

    return final_score


# AEBS Pedestrian at Daytime
def calculate_ped_day_score(sim_run_results):
    """
    :param sim_run_results: Dictionary with scenario string as keys and dict of scores.
                            The elements in the dict of scores are key containing
                            speed and value is again a dictionary with "Decel" and "ColorScore"
    :return: The AEB pedestrian score for each simulation run
    """
    warn_list = []

    # try:

    cpn_day_score = calculate_score(sim_run_results["CPNA_5_50_Day"],
                                    sim_run_results["CPNA_5_25_Day"],
                                    sim_run_results["CPNA_5_75_Day"],
                                    sim_run_results["CPNA_8_50_Day"],
                                    sim_run_results["CPNC_5_50_Day"])

    cpno_day_score = calculate_score(sim_run_results["CPNAO_5_50_Day"],
                                     sim_run_results["CPNAO_5_25_Day"],
                                     sim_run_results["CPNAO_5_75_Day"],
                                     sim_run_results["CPNAO_8_50_Day"],
                                     sim_run_results["CPNCO_5_50_Day"])

    # except Exception as e:
    #     print 'Exception: ' + e.message

    return cpn_day_score + cpno_day_score


# AEBS Pedestrian at Night time with streetlights
def calculate_ped_night_with_streetlights_score(sim_run_results):
    """
    :param sim_run_results: Dictionary with scenario string as keys and dict of scores.
                            The elements in the dict of scores are key containing
                            speed and value is again a dictionary with "Decel" and "ColorScore"
    :return: The AEB pedestrian score for each simulation run
    """

    # try:
    cpf_15lx_score = calculate_score(sim_run_results["CPFA_15LX_5_50_Night"],
                                     sim_run_results["CPFA_15LX_5_25_Night"],
                                     sim_run_results["CPFA_15LX_5_75_Night"],
                                     sim_run_results["CPFA_15LX_8_50_Night"],
                                     None)

    cpfo_15lx_score = calculate_score(sim_run_results["CPFAO_15LX_5_50_Night"],
                                      sim_run_results["CPFAO_15LX_5_25_Night"],
                                      sim_run_results["CPFAO_15LX_5_75_Night"],
                                      sim_run_results["CPFAO_15LX_8_50_Night"],
                                      None)

    # except Exception as e:
    #     print 'Exception: ' + e.message

    return cpf_15lx_score + cpfo_15lx_score


# AEBS Pedestrian at Night time without streetlights
def calculate_ped_night_wo_streetlights_score(sim_run_results):
    """
    :param sim_run_results: Dictionary with scenario string as keys and dict of scores.
                            The elements in the dict of scores are key containing
                            speed and value is again a dictionary with "Decel" and "ColorScore"
    :return: The AEB pedestrian score for each simulation run
    """

    # try:
    cpf_15lx_score = calculate_score(sim_run_results["CPFA_1LX_5_50_Night"],
                                     sim_run_results["CPFA_1LX_5_25_Night"],
                                     sim_run_results["CPFA_1LX_5_75_Night"],
                                     sim_run_results["CPFA_1LX_8_50_Night"],
                                     None)

    cpfo_15lx_score = calculate_score(sim_run_results["CPFAO_1LX_5_50_Night"],
                                      sim_run_results["CPFAO_1LX_5_25_Night"],
                                      sim_run_results["CPFAO_1LX_5_75_Night"],
                                      sim_run_results["CPFAO_1LX_8_50_Night"],
                                      None)

    # except Exception as e:
    #     print 'Exception: ' + e.message

    return cpf_15lx_score + cpfo_15lx_score

