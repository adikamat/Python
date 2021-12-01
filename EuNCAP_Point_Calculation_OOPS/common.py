import random
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

def extract_key_value_pair(key, val, my_list):

    extracted_list = []
    for d in my_list:
        for k, v in d.items():
            # do something with the key, value pair
            if v == val:
                extracted_list.append(d)

    return extracted_list


def prepare_testcase_speed_based(points_table_dict, testcases):
    # Loop over different overlap and speed to create test bed for calculating score_color
    test_spd_list = points_table_dict.keys()
    testcase_lists = {}
    for spd in test_spd_list:
        spd_list = extract_key_value_pair("TestSpeed", spd, testcases)
        testcase_lists['s' + str(spd)] = spd_list

    return testcase_lists


def prepare_testcase_speed_overlap_based(points_table_dict, overlap, testcases):
    test_spd_list = points_table_dict.keys()
    testcase_lists = {}
    for o in overlap:
        overlap_list = extract_key_value_pair("Overlap", o, testcases)
        for spd in test_spd_list:
            spd_list = extract_key_value_pair("TestSpeed", spd, overlap_list)
            testcase_lists['o' + o + '_s' + str(spd)] = spd_list

    return testcase_lists


def monte_carlo_run_car_to_car(num_iterations, testcase_lists, scenario, points_table, OVERLAP):

    MINIMUM_TST_SPD_TO_PASS = 20  # kph

    # Initialize table element to store the simulation run result
    csv_rows = []
    csv_hdr = ["Run", "Test Speed", "Overlap", "TestCase Score", "Point Score", "Recording"]
    csv_rows.append(csv_hdr)

    # Run points calculation several times
    scenario_point_list = []
    warnings_list = []
    for run in range(num_iterations):

        tc_list = []
        # Randomly pick a test case for each speed and each overlap and sum the points for each speed over all
        # overlap ranges
        scenario_test_score = {}
        for spd in sorted(points_table.keys()):
            scenario_test_score.setdefault(spd, 0.0)

            for o in OVERLAP:
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
            csv_rows.append(["", entry["TestSpeed"], entry["Overlap"], entry["ColorScore"], "", entry["Recording"]])
        csv_rows.append(["", "", "", "", "", ""])

        csv_rows[len(csv_rows) - 2][0] = run + 1
        csv_rows[len(csv_rows) - 2][4] = scenario_score

    # # Write CSV file
    # with open(os.path.join(output_folder, sim_run_output_prefix + scenario + '.csv'), 'wb') as my_csv_file:
    #     my_csv_writer = csv.writer(my_csv_file, delimiter=';')
    #     my_csv_writer.writerows(csv_rows)

    return [scenario_point_list, sum(points_table.values()), warnings_list, csv_rows]


def monte_carlo_run_car_to_vru(num_iterations, testcase_lists, scenario, points_table, OVERLAP=None):

    # Run points calculation several times
    scenario_point_list = []
    warnings_list = []
    csv_rows = []
    csv_hdr = ["Run", "Test Speed", "Overlap", "TestCase Score", "Score", "Recording"]
    csv_rows.append(csv_hdr)
    for run in range(num_iterations):

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
            csv_rows.append(["", entry["TestSpeed"], entry["Overlap"], entry["ColorScore"], "", tc["Recording"]])
        csv_rows.append(["", "", "", "", "", ""])

        csv_rows[len(csv_rows) - 2][0] = run + 1
        csv_rows[len(csv_rows) - 2][4] = scenario_test_score

    # # Write CSV file
    # with open(os.path.join(output_folder, sim_run_output_prefix + scenario + '.csv'), 'wb') as my_csv_file:
    #     my_csv_writer = csv.writer(my_csv_file, delimiter=';')
    #     my_csv_writer.writerows(csv_rows)

    return [scenario_point_list, sum(points_table.values()), warnings_list, csv_rows]
