import os
import csv
import random
import math

import matplotlib.pyplot as plt
import numpy as np

import EuNCAP_2020_scores as ncap2020
import EuNCAP_2018_scores as ncap2018

import TestCase_Data_Extract as TC_DE

from pyHTMLReport.htmlReport import cHTMLReport, cHTMLReportTable, cHTMLReportTableRow, cHTMLReportTableCell, \
    cHTMLReportGraph, cHTMLReportGraphYData, cHTMLReportImage, cHTMLReportLink, cHTMLReportVideo, \
    cHTMLReportVerticalLine, cHTMLReportCode

#############################################################
# INPUT SECTION
#############################################################
# input_files = ['51_new_testcase_name_changed.csv',
#                'UCReport_AL_EuNCAP18_Radar_FT2_19W04.csv']

input_files = ['INT_47/20190703_AL_ARS510TA19_03.01.00_INT-47_EU18.csv']

output_folder = './output'
output_file = 'Data.csv'
sim_run_scores = 'Simulation_score_scenario_wise.csv'
sim_run_output_prefix = 'TestCase_sim_'  # File name will be 'TestCase_sim_scenarioname.csv',e.g. TestCase_sim_CCRs.csv

SIM_RUN_LENGTH = 1000  # 0
ncap_standard_to_run = 2018

#####################################################################

if ncap_standard_to_run == 2018:
    ncap = ncap2018
else:
    ncap = ncap2020

scenarios_to_run = ncap.scenarios_to_run

warnings_list = []

# Helper functions
def extract_key_value_pair(key, val, my_list):

    extracted_list = []
    for d in my_list:
        for k, v in d.items(): 
            # do something with the key, value pair
            if v == val:
                extracted_list.append(d)         
                
    return extracted_list


def monte_carlo_run_car_to_car(testcases, scenario):

    MINIMUM_TST_SPD_TO_PASS = 20  # kph

    # Get the point table
    if scenario == 'CCRs':
        points_table = ncap.CCRs_points_AEB
    elif scenario == 'CCRs_FCW':
        points_table = ncap.CCRs_points_FCW
    elif scenario == 'CCRm':
        points_table = ncap.CCRm_points_AEB
    else:
        print "Unknown scenario " + scenario + " in monte_carlo_run_car_to_car function"
        points_table = {}

    # Loop over different overlap and speed to create test bed for calculating score_color
    testcase_lists = {}
    for o in ncap.OVERLAP:
        overlap_list = extract_key_value_pair("Overlap", o, testcases)
        for spd in ncap.TEST_SPD:
            spd_list = extract_key_value_pair("TestSpeed", spd, overlap_list)
            testcase_lists['o' + o + '_s' + str(spd)] = spd_list

    # print testcase_lists

    # Generate HTML report for scenario runs
    title_str = scenario + " Monte-Carlo Simulation Run results"
    scenario_sim_report = cHTMLReport(title=title_str, theme="contimodern", toc=True)

    # Initialize table element to store the simulation run result
    csv_rows = []
    csv_hdr = ["Run", "Test Speed", "Overlap", "TestCase Score", "Point Score", "Recording"]
    csv_rows.append(csv_hdr)

    # Run points calculation several times
    scenario_point_list = []
    for run in range(SIM_RUN_LENGTH):
        scenario_sim_report.SectionBegin("Run " + str(run+1))
        simResTable = cHTMLReportTable("First Table", sortable=False)
        simResTable.setHeaderRow(cHTMLReportTableRow(cells=["Test Speed", "Overlap", "TestCase Score", "Recording"]))

        tc_list = []
        # Randomly pick a test case for each speed and each overlap and sum the points for each speed over all
        # overlap ranges
        scenario_test_score = {}
        for spd in sorted(points_table.keys()):
            scenario_test_score.setdefault(spd, 0.0)
            
            for o in ncap.OVERLAP:
                key = 'o' + o + '_s' + str(spd)
                if key in testcase_lists.keys() and len(testcase_lists[key]) > 0:
                    index = random.randint(0, len(testcase_lists[key]) - 1)
                    
                    tc = testcase_lists[key][index]                    
                    
                else:
                    # Display print message only once
                    if run == 0:
                        w_str = 'Overlap and speed combination ' + key + ' does not exist in  scenario ' + scenario
                        print w_str
                        warnings_list.append(w_str)
                    tc = {}
                    tc["TestSpeed"] = spd
                    tc["Overlap"] = o
                    tc["ColorScore"] = 0
                    tc["Recording"] = "No test case found"
                    
                tc_list.append(tc)
                    
                # Need to Count 100% overlap case twice
                scale = 2 if tc["Overlap"] == "100" else 1
    
                scenario_test_score[spd] += (tc["ColorScore"] * scale) / 6

        # Loop over each test speed and multiply the weight factor
        scenario_score = 0.0    
        for test_speed in sorted(points_table.keys()):
            if test_speed < MINIMUM_TST_SPD_TO_PASS and scenario_test_score[test_speed] == 0:
                print "Test speed " + str(test_speed) + " in scenario " + scenario + " has failed."
                print "Setting scenario score to 0"
                warnings_list.append("Test speed " + str(test_speed) + " in scenario " + scenario + " has failed.")
                scenario_score = 0
                break
            scenario_score += (scenario_test_score[test_speed] * points_table[test_speed])
        # scenario_score = scenario_score * 4 / 14
        scenario_point_list.append(scenario_score)
        
        # Write to csv file
        for entry in tc_list:
            # print "TC_SPD: " + str(entry["TestSpeed"]) + " TC_OVLAP: " + entry["Overlap"] + \
            #     " TC_SCORE: " + str(entry["ColorScore"])
            simResTable.addRow(cHTMLReportTableRow(
                cells=[str(entry["TestSpeed"]), entry["Overlap"], str(entry["ColorScore"]), entry["Recording"]]))
            csv_rows.append(["", entry["TestSpeed"], entry["Overlap"], entry["ColorScore"], "", entry["Recording"]])
        csv_rows.append(["", "", "", "", "", ""])
        
        csv_rows[len(csv_rows)-2][0] = run + 1
        csv_rows[len(csv_rows)-2][4] = scenario_score

        # Add table to report
        scenario_sim_report.AddText("Run Score: " + str(scenario_score) + " / " + str(sum(points_table.values())))
        scenario_sim_report.AddTable(simResTable)
        scenario_sim_report.SectionEnd()
    
    # Write CSV file
    with open(os.path.join(output_folder, sim_run_output_prefix + scenario + '.csv'), 'wb') as my_csv_file:
        my_csv_writer = csv.writer(my_csv_file, delimiter=';')
        my_csv_writer.writerows(csv_rows)

    scenario_sim_report.Save(os.path.join(output_folder, 'HTMLReport', sim_run_output_prefix + scenario + ".html"))

    return [scenario_point_list, sum(points_table.values())]


def monte_carlo_run_car_to_vru(testcases, scenario):

    # Loop over different overlap and speed to create test bed for calculating score_color
    testcase_lists = {}
    for spd in ncap.TEST_SPD:
        spd_list = extract_key_value_pair("TestSpeed", spd, testcases)
        testcase_lists['s' + str(spd)] = spd_list
            
    # print testcase_lists
    
    # Get the point table
    points_table_dict = ncap.points_table_dict
                                
    if scenario in points_table_dict:
        points_table = points_table_dict[scenario]
    else:
        print "Unknown scenario " + scenario + " in monte_carlo_run_car_to_vru function"
        
    # Run points calculation several times
    scenario_point_list = []
    csv_rows = []
    csv_hdr = ["Run", "Test Speed", "Overlap", "TestCase Score", "Score", "Recording"]
    csv_rows.append(csv_hdr)
    for run in range(SIM_RUN_LENGTH):
        
        tc_list = []
        # Randomly pick a test case for each speed and each overlap and sum the points for each speed over all
        # overlap ranges
        scenario_test_score = 0
        for spd in sorted(points_table.keys()):
                            
            key = 's' + str(spd)
            if key in testcase_lists.keys() and len(testcase_lists[key]) > 0:
                index = random.randint(0, len(testcase_lists[key]) - 1)
                
                tc = testcase_lists[key][index]                    
                
            else:
                # Display print message only once
                if run == 0:
                    w_str = 'Test case for speed ' + key[1:] + ' does not exist in scenario ' + scenario
                    print w_str
                    warnings_list.append(w_str)
                tc = {}
                tc["TestSpeed"] = spd
                tc["Overlap"] = 100  # Not used in car-to-bicycle scenario
                tc["ColorScore"] = 0
                tc["Recording"] = "No test case found"
                
            tc_list.append(tc)
                
            scenario_test_score += tc["ColorScore"]

        # Loop over each test speed and multiply the weight factor
        # scenario_score = scenario_test_score * 100 / sum(points_table.values())
        scenario_point_list.append(scenario_test_score)               
        
        # Write to csv file
        for entry in tc_list:
            # print "TC_SPD: " + str(entry["TestSpeed"]) + " TC_OVLAP: " + entry["Overlap"] + \
            #     " TC_SCORE: " + str(entry["ColorScore"])
            csv_rows.append(["",entry["TestSpeed"], entry["Overlap"], entry["ColorScore"], "", tc["Recording"]])
        csv_rows.append(["", "", "", "", "", ""])
        
        csv_rows[len(csv_rows)-2][0] = run + 1
        csv_rows[len(csv_rows)-2][4] = scenario_test_score
    
    # Write CSV file
    with open(os.path.join(output_folder, sim_run_output_prefix + scenario + '.csv'), 'wb') as my_csv_file:
        my_csv_writer = csv.writer(my_csv_file, delimiter=';')
        my_csv_writer.writerows(csv_rows)

    return [scenario_point_list, sum(points_table.values())]      


def calculate_AEB_Car(testcase_datset):

    AEB_score = 0.0

    # Calculate and add pts for CBFA scenario
    #ccrs_correction_factor =
    if "CCRs" in testcase_datset.keys():
        AEB_score = np.add(AEB_score, np.multiply(
            np.true_divide(testcase_datset["CCRs"]["SimScore"], testcase_datset["CCRs"]["SimMaxScore"]),
            ncap.AEB_CCR_scenario_wt["CCRs"]))
    else:
        print "CCRs scenario scores are missing for Car-To-Car AEB calculation."
        warnings_list.append("CCRs scenario scores are missing for Car-To-Car AEB calculation.")

    # Calculate and add pts for CBNA scenario
    if "CCRm" in testcase_datset.keys():
        AEB_score = np.add(AEB_score, np.multiply(
            np.true_divide(testcase_datset["CCRm"]["SimScore"], testcase_datset["CCRm"]["SimMaxScore"]),
            ncap.AEB_Cyclist_scenario_wt["CCRm"]))
    else:
        print "CCRm scenario scores are missing for Car-To-Car AEB calculation."
        warnings_list.append("CCRm scenario scores are missing for Car-To-Car AEB calculation.")

    # Calculate and add pts for CBNAO scenario
    if "CCRb" in testcase_datset.keys():
        AEB_score = np.add(AEB_score, np.multiply(
            np.true_divide(testcase_datset["CCRb"]["SimScore"], testcase_datset["CCRb"]["SimMaxScore"]),
            ncap.AEB_Cyclist_scenario_wt["CCRb"]))
    else:
        print "CCRb scenario scores are missing for Car-To-Car AEB calculation."
        warnings_list.append("CCRb scenario scores are missing for Car-To-Car AEB calculation.")

    return AEB_score


# def calculate_CCR_AEB_scores(testcases, test_scenario):
if __name__ == "__main__":

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    if not os.path.isdir(os.path.join(output_folder, 'HTMLReport')):
        os.makedirs(os.path.join(output_folder, 'HTMLReport'))

    report = cHTMLReport(title="EuNCAP " + str(ncap_standard_to_run) + " Point Calculation",
                         theme="contimodern", toc=True)

    csv_hdr = ["TestCaseID", "Recording", "Scenario",  "TestSpeed", "Overlap", "MeasuredWarnTTC", "MeasuredTTC",
               "ImpactSpeed", "ColorScore", "Color"]

    # Read Test case data from excel sheet
    testcase_dataset = TC_DE.read_testcase_data(input_files)

    # Write to HTML Report
    report.SectionBegin("Test Case Details")
    report.AddText("Input Filename: " + ',\n'.join(input_files))
    numTests = [len(testcase_dataset[k]) for k in testcase_dataset.keys()]
    testcaseListTable = cHTMLReportTable("Test Case per scenario", sortable=False)
    testcaseListTable.setHeaderRow(cHTMLReportTableRow(cells=["Scenario", "No. of Test Cases"]))
    for i, k in enumerate(testcase_dataset.keys()):
        testcaseListTable.addRow(cHTMLReportTableRow(cells=[k, str(numTests[i])]))
    report.AddTable(testcaseListTable)
    report.SectionEnd()

    # Store rows for each testcase evaluation
    rows = list()
    rows.append(csv_hdr)

    # Store rows for scenario score for all runs
    run_row = ["Run"]
    run_row.extend(range(1, SIM_RUN_LENGTH+1))
    sim_csv_run = [run_row]

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

    for scenario in scenarios_to_run:

        if scenario in testcase_dataset.keys():
            testcases = testcase_dataset[scenario]
        else:
            print "Scenario " + scenario + " missing in test case CSV-file"
            warnings_list.append("Scenario " + scenario + " missing in test case CSV-file")
            testcases = []

        testcase_results.setdefault(scenario, {})
        # Loop over testcases
        for testcase in testcases:

            # Get the score for each test case
            if scenario in ['CCRs', 'CCRm', 'CCRb', 'CCRs_FCW']:
                # Car-to-Car scenarios
                score_color, score_value = ncap.Car_to_Car_get_bin_score(testcase["ImpactSpeed"],
                                                                         testcase["TestSpeed"], scenario)

            elif scenario in ['CBLA_50', 'CBNA', 'CBFA', 'CBNAO', 'CPFA_50', 'CPNA_75_Day',
                              'CPNA_75_Night', 'CPNA_25_Day', 'CPNA_25_Night',
                              'CPNC_50', 'CPLA_50_Day', 'CPLA_50_Night',
                              'CPRTO', 'CPLTO', 'CPRA_Static', 'CPRA_Moving']:
                # Car-To-Vru scenarios using impact speed criteria
                score_color, score_value = ncap.Car_to_Vru_get_bin_score(testcase["ImpactSpeed"],
                                                                         testcase["TestSpeed"], scenario)

            elif scenario in ['CBLA_25', 'CPLA_25_Day', 'CPLA_25_Night']:
                # Car-To-Vru scenarios using warning TTC (FCW) criteria
                try:
                    fcw_ttc = float(testcase["MeasuredWarnTTC"])

                except ValueError:
                    # For entries with blanks or "N/A", TTC is set to 0.0
                    # This means that the testcase is failed and will be awarded 0 points (red region).
                    fcw_ttc = 0.0

                score_color, score_value = ncap.Car_to_Vru_get_bin_score(fcw_ttc, testcase["TestSpeed"], scenario)

            else:
                print "Unexpected scenario: " + scenario + " in main function"
                warnings_list.append("Unexpected scenario: " + scenario + " in main function")
                score_color = "NoColor"
                score_value = 0

            # Store the color bin and points to test case
            testcase["ColorScore"] = score_value
            testcase["Color"] = score_color

            row = []
            for hdr_col in csv_hdr:
                if hdr_col == "Scenario":
                    row.append(scenario)
                else:
                    row.append(testcase[hdr_col])

            rows.append(row)

        # Monte carlo simulation
        if scenario in ['CCRs', 'CCRm', 'CCRb', 'CCRs_FCW']:
            # Copy test cases for speed 30 kmph to 80 kmph from 'CCRs" scenario
            if scenario == 'CCRs_FCW':
                for spd in range(30, 85, 5):
                    testcase_30_to_50_kph = extract_key_value_pair("TestSpeed", spd, testcase_dataset["CCRs"])
                    testcases.extend(testcase_30_to_50_kph)

            points, max_points = monte_carlo_run_car_to_car(testcases, scenario)

        elif scenario in ['CBLA_50', 'CBNA', 'CBFA', 'CBNAO', 'CBLA_25', 'CPFA_50', 'CPNA_75_Day',
                          'CPNA_75_Night','CPNA_25_Day', 'CPNA_25_Night', 'CPNC_50', 'CPLA_50_Day',
                          'CPLA_50_Night', 'CPLA_25_Day', 'CPLA_25_Night',
                          'CPRTO', 'CPLTO', 'CPRA_Static', 'CPRA_Moving']:
            points, max_points = monte_carlo_run_car_to_vru(testcases, scenario)

        else:
            print "Unknown scenario " + scenario + " for monte-carlo simulation run"
            warnings_list.append("Unknown scenario " + scenario + " for monte-carlo simulation run")
            points = 0.0
            max_points = 0.0

        # Store rows for scenario score for all runs
        scenario_run_row = [scenario]
        scenario_run_row.extend(points)
        sim_csv_run.append(scenario_run_row)

        final_score_str += '\n' + '{0: <15}: {1} out of {2}'.format(scenario, np.median(points), max_points)
        meanScoreTable.addRow(cHTMLReportTableRow(cells=[scenario, str(np.percentile(points, 10)),
                                                         str(np.median(points)), str(np.percentile(points, 90)),
                                                         str(max_points)]))

        # Store the simulation run score for each scenario
        testcase_results[scenario] = {"SimScore": points, "SimMaxScore": max_points}

        # # Plot the points
        # plt.figure()
        # # plt.clf()
        # # plt.plot(points, label=scenario)
        # plt.boxplot(points)
        # # axes = plt.gca()
        # # axes.set_ylim([0, 20])
        # # plt.xlabel('Run')
        # # plt.ylabel('Points')
        # # plt.legend(loc='best')
        # # plt.title('Scenario Points over multiple runs')
        # plt.title('Scenario : ' + scenario.replace('_', '-'))
        #
        # Plot the histogram of points
        # the histogram of the data
        plt.figure()
        min_pts = np.min(points)
        max_pts = np.max(points)
        # Points upto 3 decimal places are important
        n, bins, patches = plt.hist(points)

        plt.xlabel('Points (Max Points =' + str(max_points) + ')')
        plt.ylabel('Count')
        plt.title('Histogram of Points for ' + scenario.replace('_', '-'))
        # plt.axis([40, 160, 0, 0.03])
        plt.grid(True)
        filename = scenario + '_histogram.png'
        plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', filename))
        hist_images_filenames[scenario] = filename
        plt.close()
        # plt.show()

    # Write each test case wise data to csv file
    with open(os.path.join(output_folder, output_file), 'wb') as my_csv_file:
        my_csv_writer = csv.writer(my_csv_file, delimiter=';')
        my_csv_writer.writerows(rows)

    # Write each run data for all scenarios to csv file
    with open(os.path.join(output_folder, sim_run_scores), 'wb') as my_csv_file:
        my_csv_writer = csv.writer(my_csv_file, delimiter=';')
        my_csv_writer.writerows(zip(*sim_csv_run))

    # Draw Plots and save plot figure,
    ccr_box_plots = [testcase_results["CCRs"]["SimScore"],
                     testcase_results["CCRm"]["SimScore"],
                     testcase_results["CCRs_FCW"]["SimScore"]]
    labels = ["CCRs", "CCRm", "CCRs_FCW"]

    # Save box plot figures
    plt.figure()
    plt.boxplot(ccr_box_plots)
    ax = plt.gca()
    ax.set_xticklabels(("CCRs", "CCRm", "CCRs_FCW"))
    # plt.legend(labels)
    plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', 'car_to_car_scenario_boxplots.png'))

    print "\nCombining scores for Bicycle scenarios"
    # Calculate AEB score for Bicycle
    AEB_Cyclist, AEB_Cyclist_max, Cyclist_warnings = ncap.calculate_AEB_Cyclist(testcase_results)
    if len(Cyclist_warnings) > 0:
        warnings_list.extend(Cyclist_warnings)

    print "\nCombining scores for Pedestrian scenarios"
    # Calculate AEB score for Pedestrian
    AEB_Pedestrian, AEB_Pedestrian_max, Ped_warnings = ncap.calculate_AEB_Pedestrian(testcase_results)
    if len(Ped_warnings) > 0:
        warnings_list.extend(Ped_warnings)

    # AEB_Cyclist_total_score = np.multiply(np.true_divide(AEB_Cyclist_score, AEB_cyclist_total_available_scores), 6.0)
    # Plot AEB cyclist total score
    plt.figure()
    plt.plot(AEB_Cyclist)
    axes = plt.gca()
    axes.set_ylim([0, 20])
    plt.xlabel('Run')
    plt.ylabel('Points')
    plt.title('AEB cyclist combined over multiple scenarios')

    # AEB_Pedestrian_score = np.multiply(
    #     np.true_divide(AEB_Pedestrian_Day_score, AEB_Pedestrian_Day_total_available_scores), 3.0) + \
    #     np.multiply(np.true_divide(AEB_Pedestrian_Night_score, AEB_Pedestrian_Night_total_available_scores), 3.0)

    # Plot AEB pedestrian total score
    plt.figure()
    plt.plot(AEB_Pedestrian)
    axes = plt.gca()
    axes.set_ylim([0, 20])
    plt.xlabel('Run')
    plt.ylabel('Points')
    plt.title('AEB pedestrian combined over multiple scenarios')

    plt.show()

    # Save bar chart for mean scores
    ax = plt.subplots()
    numScenarios = len(scenarios_to_run)
    index = np.arange(numScenarios)
    values = [np.median(testcase_results[scenarios_to_run[n]]["SimScore"]) /
              testcase_results[scenarios_to_run[n]]["SimMaxScore"] * 100
              for n in range(numScenarios)]
    bar_width = 0.35
    opacity = 0.8

    plt.bar(index, values, bar_width, alpha=opacity, color='b')
    plt.title('Scenario Results')
    plt.xticks(index, scenarios_to_run)
    plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='left')
    plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', 'median_scores_barchart.png'))

    # Save Radar chart
    ax = plt.subplot(111, polar=True)
    # Generate data in required format
    numScenarios = len(scenarios_to_run)
    angles = [n / float(numScenarios) * 2 * math.pi for n in range(numScenarios)]
    angles += angles[:1]
    values = [np.median(testcase_results[scenarios_to_run[n]]["SimScore"]) /
              testcase_results[scenarios_to_run[n]]["SimMaxScore"]
              for n in range(numScenarios)]
    values += values[:1]

    ax.plot(angles, values)
    ax.fill(angles, values, 'teal', alpha=0.1)

    # Add the attribute labels to our axes
    plt.xticks(angles[:-1], scenarios_to_run)
    # plt.title("Mean Values for different scenarios")
    plt.savefig(os.path.join(output_folder, 'HTMLReport', 'gfx', 'median_scores_chart.png'))

    print "\n\nScores Scenario-wise:"
    print "========================================"
    print final_score_str
    print "========================================"
    report.SectionBegin("Scores Scenario-wise")
    report.AddText("The following table contains mean scores for each scenario")
    report.AddTable(meanScoreTable)
    rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    report.AddImage(cHTMLReportImage(os.path.join(rp, "median_scores_barchart.png"),
                                     'Scenario Median Scores', 1024, 800))
    rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    report.AddImage(cHTMLReportImage(os.path.join(rp, "median_scores_chart.png"),
                                     'Scenario Median Scores', 1024, 800))
    report.SectionEnd()

    # Add the histogram plots for each scenario
    report.SectionBegin("Histogram Plots for Scenario-wise")
    report.AddText("The following table contains the histogram of scenario scores after Monte Carlo simulation")
    rp = os.path.relpath(os.path.join(output_folder, 'HTMLReport', 'gfx'), os.path.join(output_folder, 'HTMLReport'))
    for scenario in scenarios_to_run:
        report.AddImage(cHTMLReportImage(os.path.join(rp, hist_images_filenames[scenario]),
                                         "Histogram for " + scenario + " scores", 1024, 800))
    report.SectionEnd()

    # Write Final scenario score to HTML Report
    report.SectionBegin("Scenario Results")
    report.AddText("AEB Pedestrian = " + str(np.median(AEB_Pedestrian)) + " out of " + str(AEB_Pedestrian_max))
    report.AddText("AEB Cyclist = " + str(np.median(AEB_Cyclist)) + " out of " + str(AEB_Cyclist_max))
    report.SectionEnd()

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

    print "AEB Pedestrian = " + str(np.median(AEB_Pedestrian)) + " out of " + str(AEB_Pedestrian_max)
    print "AEB Cyclist = " + str(np.median(AEB_Cyclist)) + " out of " + str(AEB_Cyclist_max)
    print "Done"
