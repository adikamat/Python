import os
import csv
import re
from calculation_brake_model import calculate_impact_velocity

TC_ID_MAP = {'EBA_TC_100_009': 'CBNA_60kph',
             'EBA_TC_100_004': 'CBNA_35kph',
             'EBA_TC_100_007': 'CBNA_50kph',
             'EBA_TC_100_003': 'CBNA_30kph',
             'EBA_TC_100_002': 'CBNA_25kph',
             'EBA_TC_100_005': 'CBNA_40kph',
             'EBA_TC_100_001': 'CBNA_20kph',
             'EBA_TC_100_006': 'CBNA_45kph',
             'EBA_TC_100_008': 'CBNA_55kph',

             'EBA_TC_100_017': 'CBLA_50%_30kph',
             'EBA_TC_100_018': 'CBLA_50%_35kph',
             'EBA_TC_100_019': 'CBLA_50%_40kph',
             'EBA_TC_100_020': 'CBLA_50%_45kph',
             'EBA_TC_100_021': 'CBLA_50%_50kph',
             'EBA_TC_100_022': 'CBLA_50%_55kph',
             'EBA_TC_100_023': 'CBLA_50%_60kph',
             'EBA_TC_100_024': 'CBLA_25%_65kph',
             'EBA_TC_100_025': 'CBLA_25%_70kph',
             'EBA_TC_100_026': 'CBLA_25%_75kph',
             'EBA_TC_100_027': 'CBLA_25%_80kph',
             'EBA_TC_100_028': 'CBLA_50%_25kph',
             'EBA_TC_100_029': 'CBLA_25%_55kph',
             'EBA_TC_100_030': 'CBLA_25%_60kph',
             'EBA_TC_100_031': 'CBLA_50%_20kph',
             'EBA_TC_100_049': 'CBLA_25%_50kph',

             'EBA_TC_215_097': 'CCRs_-75%_10kph',
             'EBA_TC_215_098': 'CCRs_-75%_15kph',
             'EBA_TC_215_099': 'CCRs_-75%_20kph',
             'EBA_TC_215_100': 'CCRs_-75%_25kph',
             'EBA_TC_215_101': 'CCRs_-75%_30kph',
             'EBA_TC_215_102': 'CCRs_-75%_35kph',
             'EBA_TC_215_103': 'CCRs_-75%_40kph',
             'EBA_TC_215_104': 'CCRs_-75%_45kph',
             'EBA_TC_215_105': 'CCRs_-75%_50kph',
             'EBA_TC_215_111': 'CCRs_-75%_55kph',
             'EBA_TC_215_112': 'CCRs_-75%_60kph',
             'EBA_TC_215_113': 'CCRs_-75%_65kph',
             'EBA_TC_215_114': 'CCRs_-75%_70kph',
             'EBA_TC_215_115': 'CCRs_-75%_75kph',
             'EBA_TC_215_116': 'CCRs_-75%_80kph',

             'EBA_TC_215_046': 'CCRs_75%_10kph',
             'EBA_TC_215_047': 'CCRs_75%_15kph',
             'EBA_TC_215_048': 'CCRs_75%_20kph',
             'EBA_TC_215_049': 'CCRs_75%_25kph',
             'EBA_TC_215_050': 'CCRs_75%_30kph',
             'EBA_TC_215_051': 'CCRs_75%_35kph',
             'EBA_TC_215_052': 'CCRs_75%_40kph',
             'EBA_TC_215_053': 'CCRs_75%_45kph',
             'EBA_TC_215_054': 'CCRs_75%_50kph',
             'EBA_TC_215_060': 'CCRs_75%_55kph',
             'EBA_TC_215_061': 'CCRs_75%_60kph',
             'EBA_TC_215_062': 'CCRs_75%_65kph',
             'EBA_TC_215_063': 'CCRs_75%_70kph',
             'EBA_TC_215_064': 'CCRs_75%_75kph',
             'EBA_TC_215_065': 'CCRs_75%_80kph',

             'EBA_TC_215_001': 'CCRs_100%_10kph',
             'EBA_TC_215_002': 'CCRs_100%_15kph',
             'EBA_TC_215_003': 'CCRs_100%_20kph',
             'EBA_TC_215_004': 'CCRs_100%_25kph',
             'EBA_TC_215_005': 'CCRs_100%_30kph',
             'EBA_TC_215_008': 'CCRs_100%_35kph',
             'EBA_TC_215_009': 'CCRs_100%_40kph',
             'EBA_TC_215_010': 'CCRs_100%_45kph',
             'EBA_TC_215_011': 'CCRs_100%_50kph',
             'EBA_TC_215_071': 'CCRs_100%_55kph',
             'EBA_TC_215_072': 'CCRs_100%_60kph',
             'EBA_TC_215_073': 'CCRs_100%_65kph',
             'EBA_TC_215_074': 'CCRs_100%_70kph',
             'EBA_TC_215_075': 'CCRs_100%_75kph',
             'EBA_TC_215_076': 'CCRs_100%_80kph',

             'EBA_TC_215_077': 'CCRs_-50%_10kph',
             'EBA_TC_215_078': 'CCRs_-50%_15kph',
             'EBA_TC_215_079': 'CCRs_-50%_20kph',
             'EBA_TC_215_080': 'CCRs_-50%_25kph',
             'EBA_TC_215_081': 'CCRs_-50%_30kph',
             'EBA_TC_215_082': 'CCRs_-50%_35kph',
             'EBA_TC_215_083': 'CCRs_-50%_40kph',
             'EBA_TC_215_084': 'CCRs_-50%_45kph',
             'EBA_TC_215_085': 'CCRs_-50%_50kph',
             'EBA_TC_215_091': 'CCRs_-50%_55kph',
             'EBA_TC_215_092': 'CCRs_-50%_60kph',
             'EBA_TC_215_093': 'CCRs_-50%_65kph',
             'EBA_TC_215_094': 'CCRs_-50%_70kph',
             'EBA_TC_215_095': 'CCRs_-50%_75kph',
             'EBA_TC_215_096': 'CCRs_-50%_80kph',

             'EBA_TC_215_026': 'CCRs_50%_10kph',
             'EBA_TC_215_027': 'CCRs_50%_15kph',
             'EBA_TC_215_028': 'CCRs_50%_20kph',
             'EBA_TC_215_029': 'CCRs_50%_25kph',
             'EBA_TC_215_031': 'CCRs_50%_35kph',
             'EBA_TC_215_030': 'CCRs_50%_30kph',
             'EBA_TC_215_033': 'CCRs_50%_45kph',
             'EBA_TC_215_032': 'CCRs_50%_40kph',
             'EBA_TC_215_034': 'CCRs_50%_50kph',
             'EBA_TC_215_040': 'CCRs_50%_55kph',
             'EBA_TC_215_041': 'CCRs_50%_60kph',
             'EBA_TC_215_042': 'CCRs_50%_65kph',
             'EBA_TC_215_043': 'CCRs_50%_70kph',
             'EBA_TC_215_044': 'CCRs_50%_75kph',
             'EBA_TC_215_045': 'CCRs_50%_80kph',

             'EBA_TC_213_002': 'CCRm_100%_30kph',
             'EBA_TC_213_003': 'CCRm_100%_35kph',
             'EBA_TC_213_005': 'CCRm_100%_40kph',
             'EBA_TC_213_006': 'CCRm_100%_45kph',
             'EBA_TC_213_008': 'CCRm_100%_50kph',
             'EBA_TC_213_010': 'CCRm_100%_55kph',
             'EBA_TC_213_011': 'CCRm_100%_60kph',
             'EBA_TC_213_013': 'CCRm_100%_65kph',
             'EBA_TC_213_015': 'CCRm_100%_70kph',
             'EBA_TC_213_115': 'CCRm_100%_75kph',
             'EBA_TC_213_104': 'CCRm_100%_80kph',

             'EBA_TC_213_036': 'CCRm_75%_30kph',
             'EBA_TC_213_037': 'CCRm_75%_35kph',
             'EBA_TC_213_038': 'CCRm_75%_40kph',
             'EBA_TC_213_039': 'CCRm_75%_45kph',
             'EBA_TC_213_040': 'CCRm_75%_50kph',
             'EBA_TC_213_041': 'CCRm_75%_55kph',
             'EBA_TC_213_042': 'CCRm_75%_60kph',
             'EBA_TC_213_043': 'CCRm_75%_65kph',
             'EBA_TC_213_044': 'CCRm_75%_70kph',
             'EBA_TC_213_113': 'CCRm_75%_75kph',
             'EBA_TC_213_114': 'CCRm_75%_80kph',

             'EBA_TC_213_075': 'CCRm_-75%_30kph',
             'EBA_TC_213_076': 'CCRm_-75%_35kph',
             'EBA_TC_213_077': 'CCRm_-75%_40kph',
             'EBA_TC_213_078': 'CCRm_-75%_45kph',
             'EBA_TC_213_079': 'CCRm_-75%_50kph',
             'EBA_TC_213_080': 'CCRm_-75%_55kph',
             'EBA_TC_213_081': 'CCRm_-75%_60kph',
             'EBA_TC_213_082': 'CCRm_-75%_65kph',
             'EBA_TC_213_083': 'CCRm_-75%_70kph',
             'EBA_TC_213_118': 'CCRm_-75%_75kph',
             'EBA_TC_213_119': 'CCRm_-75%_80kph',

             'EBA_TC_213_020': 'CCRm_50%_30kph',
             'EBA_TC_213_021': 'CCRm_50%_35kph',
             'EBA_TC_213_022': 'CCRm_50%_40kph',
             'EBA_TC_213_023': 'CCRm_50%_45kph',
             'EBA_TC_213_024': 'CCRm_50%_50kph',
             'EBA_TC_213_025': 'CCRm_50%_55kph',
             'EBA_TC_213_026': 'CCRm_50%_60kph',
             'EBA_TC_213_027': 'CCRm_50%_65kph',
             'EBA_TC_213_028': 'CCRm_50%_70kph',
             'EBA_TC_213_111': 'CCRm_50%_75kph',
             'EBA_TC_213_112': 'CCRm_50%_80kph',

             'EBA_TC_213_059': 'CCRm_-50%_30kph',
             'EBA_TC_213_060': 'CCRm_-50%_35kph',
             'EBA_TC_213_061': 'CCRm_-50%_40kph',
             'EBA_TC_213_062': 'CCRm_-50%_45kph',
             'EBA_TC_213_063': 'CCRm_-50%_50kph',
             'EBA_TC_213_064': 'CCRm_-50%_55kph',
             'EBA_TC_213_065': 'CCRm_-50%_60kph',
             'EBA_TC_213_066': 'CCRm_-50%_65kph',
             'EBA_TC_213_067': 'CCRm_-50%_70kph',
             'EBA_TC_213_116': 'CCRm_-50%_75kph',
             'EBA_TC_213_117': 'CCRm_-50%_80kph',

             'EBA_TC_211_016': 'CCRb_40m_-2m/s^2_50kph',
             'EBA_TC_211_018': 'CCRb_12m_-2m/s^2_50kph',
             'EBA_TC_211_026': 'CCRb_40m_-6m/s^2_50kph',
             'EBA_TC_211_028': 'CCRb_12m_-6m/s^2_50kph',

             'EBA_TC_300_014': 'CPNA_25%_Day_20kph',
             'EBA_TC_300_015': 'CPNA_25%_Day_25kph',
             'EBA_TC_300_016': 'CPNA_25%_Day_30kph',
             'EBA_TC_300_017': 'CPNA_25%_Day_35kph',
             'EBA_TC_300_018': 'CPNA_25%_Day_40kph',
             'EBA_TC_300_019': 'CPNA_25%_Day_45kph',
             'EBA_TC_300_020': 'CPNA_25%_Day_50kph',
             'EBA_TC_300_021': 'CPNA_25%_Day_55kph',
             'EBA_TC_300_022': 'CPNA_25%_Day_60kph',

             'EBA_TC_300_105': 'CPNA_25%_Night_20kph',
             'EBA_TC_300_106': 'CPNA_25%_Night_25kph',
             'EBA_TC_300_107': 'CPNA_25%_Night_30kph',
             'EBA_TC_300_108': 'CPNA_25%_Night_35kph',
             'EBA_TC_300_109': 'CPNA_25%_Night_40kph',
             'EBA_TC_300_110': 'CPNA_25%_Night_45kph',
             'EBA_TC_300_111': 'CPNA_25%_Night_50kph',
             'EBA_TC_300_112': 'CPNA_25%_Night_55kph',
             'EBA_TC_300_113': 'CPNA_25%_Night_60kph',

             'EBA_TC_803_352': 'CPNA_75%_Day_10kph',
             'EBA_TC_300_025': 'CPNA_75%_Day_20kph',
             'EBA_TC_300_026': 'CPNA_75%_Day_25kph',
             'EBA_TC_300_027': 'CPNA_75%_Day_30kph',
             'EBA_TC_300_028': 'CPNA_75%_Day_35kph',
             'EBA_TC_300_029': 'CPNA_75%_Day_40kph',
             'EBA_TC_300_030': 'CPNA_75%_Day_45kph',
             'EBA_TC_300_031': 'CPNA_75%_Day_50kph',
             'EBA_TC_300_032': 'CPNA_75%_Day_55kph',
             'EBA_TC_300_033': 'CPNA_75%_Day_60kph',

             'EBA_TC_300_034': 'CPNA_75%_Night_20kph',
             'EBA_TC_300_035': 'CPNA_75%_Night_25kph',
             'EBA_TC_300_036': 'CPNA_75%_Night_30kph',
             'EBA_TC_300_037': 'CPNA_75%_Night_35kph',
             'EBA_TC_300_038': 'CPNA_75%_Night_40kph',
             'EBA_TC_300_039': 'CPNA_75%_Night_45kph',
             'EBA_TC_300_040': 'CPNA_75%_Night_50kph',
             'EBA_TC_300_041': 'CPNA_75%_Night_55kph',
             'EBA_TC_300_042': 'CPNA_75%_Night_60kph',

             'EBA_TC_300_118': 'CPLA_50%_Day_20kph',
             'EBA_TC_300_119': 'CPLA_50%_Day_25kph',
             'EBA_TC_300_120': 'CPLA_50%_Day_30kph',
             'EBA_TC_300_121': 'CPLA_50%_Day_35kph',
             'EBA_TC_300_122': 'CPLA_50%_Day_40kph',
             'EBA_TC_300_123': 'CPLA_50%_Day_45kph',
             'EBA_TC_300_124': 'CPLA_50%_Day_50kph',
             'EBA_TC_300_125': 'CPLA_50%_Day_55kph',
             'EBA_TC_300_126': 'CPLA_50%_Day_60kph',

             'EBA_TC_300_043': 'CPLA_50%_Night_20kph',
             'EBA_TC_300_044': 'CPLA_50%_Night_25kph',
             'EBA_TC_300_045': 'CPLA_50%_Night_30kph',
             'EBA_TC_300_046': 'CPLA_50%_Night_35kph',
             'EBA_TC_300_047': 'CPLA_50%_Night_40kph',
             'EBA_TC_300_048': 'CPLA_50%_Night_45kph',
             'EBA_TC_300_049': 'CPLA_50%_Night_50kph',
             'EBA_TC_300_127': 'CPLA_50%_Night_55kph',
             'EBA_TC_300_128': 'CPLA_50%_Night_60kph',

             'EBA_TC_300_129': 'CPLA_25%_Day_50kph',
             'EBA_TC_300_130': 'CPLA_25%_Day_55kph',
             'EBA_TC_300_131': 'CPLA_25%_Day_60kph',
             'EBA_TC_300_132': 'CPLA_25%_Day_65kph',
             'EBA_TC_300_133': 'CPLA_25%_Day_70kph',
             'EBA_TC_300_134': 'CPLA_25%_Day_75kph',
             'EBA_TC_300_135': 'CPLA_25%_Day_80kph',

             'EBA_TC_300_051': 'CPLA_25%_Night_50kph',
             'EBA_TC_300_052': 'CPLA_25%_Night_55kph',
             'EBA_TC_300_053': 'CPLA_25%_Night_60kph',
             'EBA_TC_300_054': 'CPLA_25%_Night_65kph',
             'EBA_TC_300_055': 'CPLA_25%_Night_70kph',
             'EBA_TC_300_056': 'CPLA_25%_Night_75kph',
             'EBA_TC_300_057': 'CPLA_25%_Night_80kph',

             'EBA_TC_300_003': 'CPFA_50_20kph',
             'EBA_TC_300_004': 'CPFA_50_25kph',
             'EBA_TC_300_005': 'CPFA_50_30kph',
             'EBA_TC_300_006': 'CPFA_50_35kph',
             'EBA_TC_300_007': 'CPFA_50_40kph',
             'EBA_TC_300_008': 'CPFA_50_45kph',
             'EBA_TC_300_009': 'CPFA_50_50kph',
             'EBA_TC_300_010': 'CPFA_50_55kph',
             'EBA_TC_300_011': 'CPFA_50_60kph',

             'EBA_TC_300_060': 'CPNC_50%_20kph',
             'EBA_TC_300_061': 'CPNC_50%_25kph',
             'EBA_TC_300_062': 'CPNC_50%_30kph',
             'EBA_TC_300_063': 'CPNC_50%_35kph',
             'EBA_TC_300_064': 'CPNC_50%_40kph',
             'EBA_TC_300_065': 'CPNC_50%_45kph',
             'EBA_TC_300_066': 'CPNC_50%_50kph',
             'EBA_TC_300_067': 'CPNC_50%_55kph',
             'EBA_TC_300_068': 'CPNC_50%_60kph',

             'EBA_TC_803_332': 'CPNA_5_50_Day_10kph',
             'EBA_TC_803_333': 'CPNA_5_50_Day_20kph',
             'EBA_TC_803_334': 'CPNA_5_50_Day_30kph',
             'EBA_TC_803_335': 'CPNA_5_50_Day_40kph',
             'EBA_TC_803_336': 'CPNA_5_50_Day_50kph',
             'EBA_TC_803_337': 'CPNA_5_50_Day_60kph',

             'EBA_TC_803_470': 'CPNA_5_25_Day_40kph',

             'EBA_TC_803_353': 'CPNAO_5_50_Day_25kph',
             'EBA_TC_803_354': 'CPNAO_5_50_Day_35kph',
             'EBA_TC_803_490': 'CPNAO_5_50_Day_40kph',
             'EBA_TC_803_355': 'CPNAO_5_50_Day_45kph',

             # 'EBA_TC_803_450': 'CPFA_1LX_5_50_Night_30kph',  # <-- Not Used. Need to confirm??
             'EBA_TC_803_451': 'CPFA_50_45kph',  # 'CPFA_1LX_5_50_Night_45kph',  # Night Spec2 = 1LX
             # 'EBA_TC_803_470': 'CPFA_1LX_8_50_Night_40kph',
             'EBA_TC_803_471': 'CPFC_1LX_5_50_Night_50kph',  # <-- Check if speed is 50 or 40 or 45 kph
             'EBA_TC_803_603': 'CPFA_1LX_5_75_Night_45kph',
             'EBA_TC_803_604': 'CPFA_1LX_5_25_Night_45kph',

             'EBA_TC_803_480': 'CPFAO_15LX_5_50_Night_30kph',  # <-- Night Spec 1 = 15LX
             }


TC_SCENARIO_REGEX = '(CCRs|CCRm|CCRb|' \
                    'CPFA_50|CPNA_75|CPNA_25|CPNC_50|CPLA_50|CPLA_25|CPRTO|CPLTO|' \
                    'CBFA|CBNAO|CBNA|CBLA_50|CBLA_25|' \
                    'CPNA_5_50|CPNA_5_25|CPNA_5_75|CPNA_8_50|CPNC_5_50|' \
                    'CPNAO_5_50|CPNAO_5_25|CPNAO_5_75|CPNAO_8_50|CPNCO_5_50|' \
                    'CPFA_15LX_5_50|CPFA_15LX_5_25|CPFA_15LX_5_75|CPFA_15LX_8_50|' \
                    'CPFA_1LX_5_50|CPFA_1LX_5_25|CPFA_1LX_5_75|CPFA_1LX_8_50)([0-9]*)'
TC_FCW_REGEX = '(FCW)'
TC_DAY_NIGHT_REGEX = '(Day|day)|(Night|night)'
TC_SPEED_REGEX = '([0-9]{2})\s?(?:km/h|kph|Kph|KPH)'
# TC_OVERLAP_REGEX = '(?<=Overlap[:|_])\s?(pos|neg)([0-9]{2})'
TC_OVERLAP_REGEX = '([0-9,-]*)%'

# def calculate_impact_velocity(TTC_time, test_speed):
#     # Currently calculating for pure step function brake model
#     impact_vel = test_speed + (DECEL * (TTC_time - DEAD_TIME) * 18 / 5) # Convert m/s to km/hr
#     return impact_vel


def read_testcase_data(input_files):

    # tc_scenario_regex = '(' + '|'.join(ncap_scenarios_list) + ')'

    testcases = {}
    for input_file in input_files:
        with open(input_file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0

            for row in csv_reader:
                # Get the index of the 'Measured Activation TTC for PreBrake'
                if line_count == 0:
                    try:
                        ttc_prebrake_idx = row.index('Measured activation TTC for PreBrakeLevel>=2')
                    except ValueError:
                        print "Could not find the index for Prebrake TTC activation. " \
                              "Change the header text to match 'Measured activation TTC for PreBrake'"
                        break

                    try:
                        result_idx = row.index('Result')
                    except ValueError:
                        print "Could not find the index for Result. Change the header text to match 'Result'"
                        break

                    try:
                        tc_id_idx = row.index('Testcase ID')
                    except ValueError:
                        print "Could not find the index for Testcase ID. Change the header text to match 'Testcase ID'"
                        break

                    try:
                        testcase_name_idx = row.index('Testcase Name')
                    except ValueError:
                        print "Could not find the index for Testcase Name. " \
                              "Change the header text to match 'Testcase Name'"
                        break

                    try:
                        rec_idx = row.index('Recording')
                    except ValueError:
                        print "Could not find the index for Recording. Change the header text to match 'Recording'"
                        break

                    try:
                        dynAcWarn_idx = row.index('Measured activation TTC for DynAcuteWarning')
                    except ValueError:
                        print "Could not find the index for Result. Change the header text to match 'Measured activation " \
                              "TTC for DynAcuteWarning'"
                        # break
                        dynAcWarn_idx = None

                # Skip first line since it is the header row
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

                            # print tc_scenario_res.groups(), tc_speed_res.groups()

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

                            # Calculate impact velocity
                            try:
                                ttc_time = float(row[ttc_prebrake_idx])
                                v_impact = calculate_impact_velocity(ttc_time, float(test_speed))
                            except ValueError:
                                # For entries with blanks or "N/A", impact speed is set to test speed
                                # This means that the testcase is failed and will be awarded 0 points (red region).
                                v_impact = float(test_speed)

                            if tc_fcw_res is not None:
                                tc_scenario = tc_scenario + "_FCW"

                            if tc_day_night_res is not None:
                                if tc_day_night_res.group(1) is not None:
                                    tc_scenario = tc_scenario + "_Day"
                                elif tc_day_night_res.group(2) is not None:
                                    tc_scenario = tc_scenario + "_Night"

                            testcases.setdefault(tc_scenario, [])

                            warn_TTC = row[dynAcWarn_idx] if dynAcWarn_idx is not None else 0
                            tc_dict = {"TestSpeed": int(test_speed),
                                       "Overlap": tc_overlap,
                                       "ImpactSpeed": v_impact,
                                       "TestCaseID": row[tc_id_idx],
                                       "Recording": row[rec_idx],
                                       "MeasuredTTC": row[ttc_prebrake_idx],
                                       "MeasuredWarnTTC": warn_TTC}

                            testcases[tc_scenario].append(tc_dict)
                        else:
                            print "Testcase name does not match regex: " + row[testcase_name_idx]

                    # print row[1]
                line_count += 1
                # break

        print 'Processed  ', str(line_count), ' lines from', input_file
        # print 'Found ', str(ccr_scenario_count) , ' car-to-car scenarios'

    numTests = [len(testcases[k]) for k in testcases.keys()]
    print "\nScenario       : No. of Test Cases"
    for i, k in enumerate(testcases.keys()):
        print '{0: <21}: {1}'.format(k, numTests[i])
    print "\n"

    return testcases

