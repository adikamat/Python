import os
import csv
import random
import math

import JNCAP_2018_scores as jncap

import matplotlib.pyplot as plt
import numpy as np

import TestCase_Data_Extract as TC_DE

from pyHTMLReport.htmlReport import cHTMLReport, cHTMLReportTable, cHTMLReportTableRow, cHTMLReportTableCell, \
    cHTMLReportGraph, cHTMLReportGraphYData, cHTMLReportImage, cHTMLReportLink, cHTMLReportVideo, \
    cHTMLReportVerticalLine, cHTMLReportCode

#############################################################
# INPUT SECTION
#############################################################
# input_files = ['51_new_testcase_name_changed.csv',
#                'UCReport_AL_EuNCAP18_Radar_FT2_19W04.csv']

input_files = ['INT45_1/20190622_AL_ARS510TA19_03.01.00_INT-45_1_TP.csv',
               'INT45_1/20190622_AL_ARS510TA19_03.01.00_INT-45_1_CPFO.csv']

output_folder = './output'
output_file = 'Data.csv'
sim_run_scores = 'Simulation_score_scenario_wise.csv'
sim_run_output_prefix = 'TestCase_sim_'  # File name will be 'TestCase_sim_scenarioname.csv',e.g. TestCase_sim_CCRs.csv

SIM_RUN_LENGTH = 1000  # 0
jncap_standard_to_run = 2018

#####################################################################

ncap = jncap
scenarios_to_run = ncap.scenarios_to_run
warnings_list = []


def extract_key_value_pair(key, val, my_list):
    extracted_list = []
    for d in my_list:
        for k, v in d.items():
            # do something with the key, value pair
            if v == val:
                extracted_list.append(d)

    return extracted_list


if __name__ == "__main__":

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    if not os.path.isdir(os.path.join(output_folder, 'HTMLReport')):
        os.makedirs(os.path.join(output_folder, 'HTMLReport'))

    report = cHTMLReport(title="JNCAP " + str(jncap_standard_to_run) + " Point Calculation",
                         theme="contimodern", toc=True)

    # csv_hdr = ["TestCaseID", "Recording", "Scenario", "TestSpeed", "Overlap", "MeasuredWarnTTC", "MeasuredTTC",
    #            "ImpactSpeed", "ColorScore", "Color"]

    # Read Test case data from excel sheet
    testcase_dataset = TC_DE.read_testcase_data(input_files)

    # Write to HTML Report
    report.SectionBegin("Test Case Details")
    report.AddText("Input Filename: " + ',\n'.join(input_files))
    numTests = [len(testcase_dataset[k]) for k in testcase_dataset.keys()]
    testcaseListTable = cHTMLReportTable("Test Case per scenario", sortable=False)
    testcaseListTable.setHeaderRow(cHTMLReportTableRow(cells=["Scenario", "No. of Test Cases"]))
    # for i, k in enumerate(testcase_dataset.keys()):
    #     testcaseListTable.addRow(cHTMLReportTableRow(cells=[k, str(numTests[i])]))
    for i, k in enumerate(ncap.scenarios_to_run):
        if k in testcase_dataset.keys():
            numTC = len(testcase_dataset[k])
        else:
            numTC = 0
        testcaseListTable.addRow(cHTMLReportTableRow(cells=[k, str(numTC)]))

    report.AddTable(testcaseListTable)
    report.SectionEnd()

    # Store rows for each testcase evaluation
    # rows = list()
    # rows.append(csv_hdr)

    # Store rows for scenario score for all runs
    # run_row = ["Run"]
    # run_row.extend(range(1, SIM_RUN_LENGTH + 1))
    # sim_csv_run = [run_row]

    # String to print the result in tabular fashion
    final_score_str = '{0: <15}: {1}'.format('Scenario', 'Mean Score')

    # Store mean score for each scenario
    meanScoreTable = cHTMLReportTable("Point Scores Scenario-wise", sortable=False)
    meanScoreTable.setHeaderRow(cHTMLReportTableRow(cells=["Scenario", "10th-Percentile", "Median Score",
                                                           "90th-Percentile", "Max Score"]))

    # Dictionary to hold test case point run from monte-carlo
    testcase_results = {}

    # List to hold filenames of saved histogram figures
    hist_images_filenames = {}

    cpn_day_scores = []
    cpf_with_streetlight_scores = []
    cpf_no_streetlight_scores = []
    ccrs_scores = []
    ccrm_scores = []
    total_asv_scores = []
    for run in range(SIM_RUN_LENGTH):
        sim_run_results = {}

        for scenario in scenarios_to_run:
            # Get all test cases for current scenario
            if scenario in testcase_dataset.keys():
                    testcases = testcase_dataset[scenario]
            elif scenario in ncap.remapped_name.keys():
                testcases = testcase_dataset[ncap.remapped_name[scenario]]
            else:
                print "Scenario " + scenario + " missing in test case CSV-file"
                warnings_list.append("Scenario " + scenario + " missing in test case CSV-file")
                testcases = []

            # Loop over different test speeds
            if scenario in ncap.points_table_dict.keys():

                # Car-to-Car scenarios
                if scenario in ['CCRs', 'CCRm', 'CCRb', 'CCRs_FCW', 'CCRm_FCW']:
                    scenario_spd_wise_res = {}
                    for spd in ncap.points_table_dict[scenario]:
                        tc_res = {}
                        # extract testcases with current speed
                        testcase_spd_list = extract_key_value_pair("TestSpeed", spd, testcases)
                        if len(testcase_spd_list) > 0:
                            # Randomly select one testcase
                            index = random.randint(0, len(testcase_spd_list) - 1)
                            testcase = testcase_spd_list[index]

                            # Calculate Decel Rate and test score as per scenario
                            decel_val, score_value = ncap.Car_to_Car_get_bin_score(testcase["ImpactSpeed"],
                                                                                   testcase["TestSpeed"], scenario)
                            # Store the color bin and points to test case
                            tc_res["ColorScore"] = score_value
                            tc_res["Decel"] = decel_val

                        else:
                            print 'No testcase found for scenario ' + scenario + ' with test speed ' + str(spd)
                            warnings_list.append('No testcase found for scenario ' + scenario + ' with test speed ' +
                                                 str(spd))

                            tc_res["ColorScore"] = 0.0
                            tc_res["Decel"] = 0.0

                        scenario_spd_wise_res[spd] = tc_res

                    # Store the results for one scenario in sim_run_results
                    sim_run_results[scenario] = scenario_spd_wise_res

                # Car-To-Ped scenarios with full test speed range
                elif scenario in ['CPNA_5_50_Day', 'CPNAO_5_50_Day', 'CPFA_1LX_5_50_Night',
                                  'CPFA_15LX_5_50_Night', 'CPFAO_1LX_5_50_Night', 'CPFAO_15LX_5_50_Night']:

                    scenario_spd_wise_res = {}
                    for spd in ncap.points_table_dict[scenario]:
                        tc_res = {}
                        # extract testcases with current speed
                        testcase_spd_list = extract_key_value_pair("TestSpeed", spd, testcases)
                        if len(testcase_spd_list) > 0:
                            # Randomly select one testcase
                            index = random.randint(0, len(testcase_spd_list) - 1)
                            testcase = testcase_spd_list[index]

                            # Calculate Decel Rate and test score as per scenario
                            decel_val, score_value = ncap.Car_to_Vru_get_bin_score(testcase["ImpactSpeed"],
                                                                                   testcase["TestSpeed"], scenario)
                            # Store the color bin and points to test case
                            tc_res["ColorScore"] = score_value
                            tc_res["Decel"] = decel_val


                        else:
                            print 'No testcase found for scenario ' + scenario + ' with test speed ' + str(spd)
                            warnings_list.append('No testcase found for scenario ' + scenario + ' with test speed ' +
                                                 str(spd))

                            tc_res["ColorScore"] = 0.0
                            tc_res["Decel"] = 0.0

                        scenario_spd_wise_res[spd] = tc_res

                    # Store the results for one scenario in sim_run_results
                    sim_run_results[scenario] = scenario_spd_wise_res

                # Car-To-Ped scenarios with only representative speeds
                elif scenario in ['CPNA_5_25_Day', 'CPNA_5_75_Day', 'CPNA_8_50_Day', 'CPNC_5_50_Day',
                    'CPNAO_5_25_Day', 'CPNAO_5_75_Day', 'CPNAO_8_50_Day', 'CPNCO_5_50_Day',
                    'CPFA_15LX_5_25_Night', 'CPFA_15LX_5_75_Night', 'CPFA_15LX_8_50_Night',
                    'CPFAO_15LX_5_25_Night', 'CPFAO_15LX_5_75_Night', 'CPFAO_15LX_8_50_Night',
                    'CPFA_1LX_5_25_Night', 'CPFA_1LX_5_75_Night', 'CPFA_1LX_8_50_Night',
                    'CPFAO_1LX_5_25_Night', 'CPFAO_1LX_5_75_Night', 'CPFAO_1LX_8_50_Night']:

                    scenario_spd_wise_res = {}

                    if scenario in ['CPNA_5_25_Day', 'CPNA_5_75_Day', 'CPNA_8_50_Day', 'CPNC_5_50_Day',
                        'CPNAO_5_25_Day', 'CPNAO_5_75_Day', 'CPNAO_8_50_Day', 'CPNCO_5_50_Day']:
                        # For day scenarios, use day representative speed
                        rep_speed = ncap.DAY_REPRESENTATIVE_SPD
                    else:
                        # For night scenarios, use night representative speed
                        rep_speed = ncap.NIGHT_REPRESENTATIVE_SPD

                    # extract testcases with representative speed
                    testcase_spd_list = extract_key_value_pair("TestSpeed", rep_speed, testcases)
                    if len(testcase_spd_list) > 0:
                        # Randomly select one testcase
                        index = random.randint(0, len(testcase_spd_list) - 1)
                        testcase = testcase_spd_list[index]

                        # Calculate Decel Rate and test score as per scenario
                        decel_val, score_value = ncap.Car_to_Vru_get_bin_score(testcase["ImpactSpeed"],
                                                                               testcase["TestSpeed"], scenario)
                        score_value = score_value * ncap.scenario_wt_dict[scenario]
                        # Store the color bin and points to test case
                        scenario_spd_wise_res[rep_speed] = {'ColorScore': score_value,
                                                            'Decel': decel_val}

                        # Get the full speed range test case name
                        scenario_split_str = scenario.split('_')
                        scenario_split_str[len(scenario_split_str) - 3] = '5'
                        scenario_split_str[len(scenario_split_str) - 2] = '50'
                        if scenario_split_str[0] == 'CPNC':
                            scenario_split_str[0] = 'CPNA'
                        elif scenario_split_str[0] == 'CPNCO':
                            scenario_split_str[0] = 'CPNAO'
                        base_sc_name = '_'.join(scenario_split_str)
                        base_sc_res = sim_run_results[base_sc_name]
                        decel_base_sc_rep_spd = base_sc_res[rep_speed]["Decel"]
                        decel_curr_sc_rep_speed = scenario_spd_wise_res[rep_speed]["Decel"]
                        if decel_base_sc_rep_spd > 0.0:
                            scale = decel_curr_sc_rep_speed / decel_base_sc_rep_spd
                        else:
                            scale = 0.0

                        for spd in ncap.points_table_dict[scenario]:
                            tc_res = {}
                            if spd != rep_speed:
                                # Calculate the scaled Decel Rate and test score as per scenario
                                decel_curr_sc = min(1, base_sc_res[spd]["Decel"] * scale)
                                score_value = decel_curr_sc * ncap.points_table_dict[scenario][spd] * \
                                              ncap.scenario_wt_dict[scenario]

                                # Store the color bin and points to test case
                                tc_res["ColorScore"] = score_value
                                tc_res["Decel"] = decel_curr_sc
                                scenario_spd_wise_res[spd] = tc_res

                    else:
                        print 'No testcase found for scenario ' + scenario + ' with test speed ' + str(spd)
                        warnings_list.append('No testcase found for scenario ' + scenario + ' with test speed ' +
                                             str(spd))

                        tc_res["ColorScore"] = 0.0
                        tc_res["Decel"] = 0.0
                        for spd in ncap.points_table_dict[scenario]:
                            scenario_spd_wise_res[spd] = tc_res

                    # Store the results for one scenario in sim_run_results
                    sim_run_results[scenario] = scenario_spd_wise_res

            else:
                print "Scenario " + scenario + " missing in JNCAP points table dictionary"
                warnings_list.append("Scenario " + scenario + " missing in JNCAP points table dictionary")

        # Calculate final scores - outside for loop of scenario. This is score for one simulation run
        cpn_day_score = ncap.calculate_ped_day_score(sim_run_results)
        cpn_day_scores.append(cpn_day_score)

        cpf_no_streetlight_score = ncap.calculate_ped_night_wo_streetlights_score(sim_run_results)
        cpf_no_streetlight_scores.append(cpf_no_streetlight_score)

        cpf_with_streetlight_score = ncap.calculate_ped_night_with_streetlights_score(sim_run_results)
        cpf_with_streetlight_scores.append(cpf_with_streetlight_score)

        ccrs_score, ccrm_score = ncap.calculate_car_to_car_score(sim_run_results)
        ccrs_scores.append(ccrs_score)
        ccrm_scores.append(ccrm_score)

        total_asv_score = ccrs_score + ccrm_score + cpn_day_score + \
                          cpf_with_streetlight_score + cpf_no_streetlight_score
        total_asv_scores.append(total_asv_score)

    # Store rows for scenario score for all runs
    # scenario_run_row = [scenario]
    # scenario_run_row.extend(points)
    # sim_csv_run.append(scenario_run_row)

    # final_score_str += '\n' + '{0: <15}: {1} out of {2}'.format(scenario, np.median(points), max_points)
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['CCRs', str(np.percentile(ccrs_scores, 10)),
                                                     str(np.median(ccrs_scores)), str(np.percentile(ccrs_scores, 90)),
                                                     '24']))
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['CCRm', str(np.percentile(ccrm_scores, 10)),
                                                     str(np.median(ccrm_scores)), str(np.percentile(ccrm_scores, 90)),
                                                     '8']))
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['AEBS Pedestrian at Daytime',
                                                     str(np.percentile(cpn_day_scores, 10)),
                                                     str(np.median(cpn_day_scores)),
                                                     str(np.percentile(cpn_day_scores, 90)),
                                                     '25']))
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['AEBS Pedestrian at Night with Streetlights',
                                                     str(np.percentile(cpf_with_streetlight_scores, 10)),
                                                     str(np.median(cpf_with_streetlight_scores)),
                                                     str(np.percentile(cpf_with_streetlight_scores, 90)),
                                                     '40']))
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['AEBS Pedestrian at Night without Streetlights',
                                                     str(np.percentile(cpf_no_streetlight_scores, 10)),
                                                     str(np.median(cpf_no_streetlight_scores)),
                                                     str(np.percentile(cpf_no_streetlight_scores, 90)),
                                                     '15']))
    meanScoreTable.addRow(cHTMLReportTableRow(cells=['Total ASV Score (For Above Scenarios)',
                                                     str(np.percentile(total_asv_scores, 10)),
                                                     str(np.median(total_asv_scores)),
                                                     str(np.percentile(total_asv_scores, 90)),
                                                     '112']))

    # Draw Plots and save plot figure,
    # ccr_box_plots = [testcase_results["CCRs"]["SimScore"],
    #                  testcase_results["CCRm"]["SimScore"],
    #                  testcase_results["CCRs_FCW"]["SimScore"]]
    # labels = ["CCRs", "CCRm", "CCRs_FCW"]

    # Save bar chart for mean scores
    # ax = plt.subplots()
    # numScenarios = len(scenarios_to_run)
    # index = np.arange(numScenarios)
    # values = [np.median(testcase_results[scenarios_to_run[n]]["SimScore"]) /
    #           testcase_results[scenarios_to_run[n]]["SimMaxScore"] * 100
    #           for n in range(numScenarios)]
    # bar_width = 0.35
    # opacity = 0.8
    #
    # plt.bar(index, values, bar_width, alpha=opacity, color='b')
    # plt.title('Scenario Results')
    # plt.xticks(index, scenarios_to_run)
    # plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='left')
    # plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', 'median_scores_barchart.png'))
    #
    # # Save Radar chart
    # ax = plt.subplot(111, polar=True)
    # # Generate data in required format
    # numScenarios = len(scenarios_to_run)
    # angles = [n / float(numScenarios) * 2 * math.pi for n in range(numScenarios)]
    # angles += angles[:1]
    # values = [np.median(testcase_results[scenarios_to_run[n]]["SimScore"]) /
    #           testcase_results[scenarios_to_run[n]]["SimMaxScore"]
    #           for n in range(numScenarios)]
    # values += values[:1]
    #
    # ax.plot(angles, values)
    # ax.fill(angles, values, 'teal', alpha=0.1)
    #
    # # Add the attribute labels to our axes
    # plt.xticks(angles[:-1], scenarios_to_run)
    # # plt.title("Mean Values for different scenarios")
    # plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', 'median_scores_chart.png'))

    # print "\n\nScores Scenario-wise:"
    # print "========================================"
    # print final_score_str
    # print "========================================"
    report.SectionBegin("Scores Scenario-wise")
    report.AddText("The following table contains mean scores for each scenario")
    report.AddTable(meanScoreTable)
    # rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    # report.AddImage(cHTMLReportImage(os.path.join(rp, "median_scores_barchart.png"),
    #                                  'Scenario Median Scores', 1024, 800))
    # rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    # report.AddImage(cHTMLReportImage(os.path.join(rp, "median_scores_chart.png"),
    #                                  'Scenario Median Scores', 1024, 800))
    report.SectionEnd()

    # # Add the histogram plots for each scenario
    # report.SectionBegin("Histogram Plots for Scenario-wise")
    # report.AddText("The following table contains the histogram of scenario scores after Monte Carlo simulation")
    # rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    # for scenario in scenarios_to_run:
    #     report.AddImage(cHTMLReportImage(os.path.join(rp, hist_images_filenames[scenario]),
    #                                      "Histogram for " + scenario + " scores", 1024, 800))
    # report.SectionEnd()
    #
    # # Write Final scenario score to HTML Report
    # report.SectionBegin("Scenario Results")
    # report.AddText("AEB Pedestrian = " + str(np.median(ccrs_scores)) + " out of 24")
    # report.AddText("AEB Cyclist = " + str(np.median(ccrm_scores)) + " out of 8")
    # report.SectionEnd()

    # Write to HTML Report
    report.SectionBegin("Warnings and Errors")
    report.AddText("List of Errors and Problems when running the script")

    warnListTable = cHTMLReportTable("Warnings and Errors", sortable=False)
    warnListTable.setHeaderRow(cHTMLReportTableRow(cells=["Sr. No.", "Warnings"]))
    for i, w in enumerate(warnings_list):
        warnListTable.addRow(cHTMLReportTableRow(cells=[str(i), w]))
    report.AddTable(warnListTable)
    report.SectionEnd()

    report.Save(os.path.join(output_folder, 'HTMLReport', "test_report.html"))

    print "Done"

