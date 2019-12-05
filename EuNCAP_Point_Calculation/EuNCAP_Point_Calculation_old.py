# 
TEST_SPD = range(10,85,5)
COLOR_SCORE = {0: ["Green",1.0], 1:["Yellow",0.75], 2:["Orange",0.5], 3:["Brown",0.25], 4:["Red",0.0]}
# Dictionary with speed as key and list as values
# List contains thresholds (impact speed) for [Green, Yellow, Orange, Brown, Red] range
CCRs_impact_vel_th = {10:[1,1,1,1,10],
                        15:[1,1,1,1,15],
                        20:[1,1,1,1,20],
                        25:[5,5,15,15,25],
                        30:[5,15,25,25,30],
                        35:[5,15,25,25,35],
                        40:[5,15,25,35,40],
                        45:[5,15,25,35,45],
                        50:[5,15,30,40,50],
                        55:[5,15,30,45,55],
                        60:[5,20,35,50,60],
                        65:[5,20,40,55,65],
                        70:[5,20,40,60,70],
                        75:[5,25,45,65,75],
                        80:[5,25,50,70,80]}
                        
CCRm_impact_vel_th = {30:[5,5,5,5,10],
                        35:[5,5,5,5,15],
                        40:[5,5,15,15,20],
                        45:[5,5,15,15,25],
                        50:[5,15,25,25,30],
                        55:[5,15,25,25,35],
                        60:[5,15,25,35,40],
                        65:[5,15,25,35,45],
                        70:[5,15,30,40,50],
                        75:[5,15,30,45,55],
                        80:[5,20,35,50,60]}
                        

# Points Table
CCRs_points_AEB = {10:1, 15:2, 20:2, 25:2, 30:2,35:2, 40:1, 45:1, 50:1}
CCRs_points_FCW = {30:2,35:2, 40:2, 45:2, 50:3, 55:2, 60:1, 65:1, 70:1, 75:1, 80:1} 
CCRm_points_AEB = {30:1,35:1, 40:1, 45:1, 50:1, 55:1, 60:1, 65:2, 70:2, 75:2, 80:2} 
                        
# Function to get the bin for given impact and test speed
def get_bin_score(impact_speed, test_speed, test_scenario):
    
    if impact_speed > test_speed:
        return (COLOR_SCORE[4])
    
    if test_scenario == "CCRs":
        threshold_dict = CCRs_impact_vel_th
    elif test_scenario == "CCRm":
        threshold_dict = CCRm_impact_vel_th
           
    if test_speed in threshold_dict.keys():
        impact_sp_threshold = threshold_dict[test_speed]
    else:
        print "Invalid test speed"
    
    try:
        index = next(x[0] for x in enumerate(impact_sp_threshold) if x[1] > impact_speed)
        #print index
        
    except StopIteration:
        # When no item found, return score 0, color red
        index = 4

    return (COLOR_SCORE[index])

if __name__ == "__main__":
    #testcases : List of dictionary containing 
    testcases = [ {"TestSpeed":10, "Overlap":-50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":15, "Overlap":-50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":20, "Overlap":-50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":25, "Overlap":-50, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":30, "Overlap":-50, "ImpactSpeed": 28, "TestScenario":"CCRs"},
                    {"TestSpeed":35, "Overlap":-50, "ImpactSpeed": 33, "TestScenario":"CCRs"},
                    {"TestSpeed":40, "Overlap":-50, "ImpactSpeed": 38, "TestScenario":"CCRs"},
                    {"TestSpeed":45, "Overlap":-50, "ImpactSpeed": 43, "TestScenario":"CCRs"},
                    {"TestSpeed":50, "Overlap":-50, "ImpactSpeed": 48, "TestScenario":"CCRs"},
                    {"TestSpeed":10, "Overlap":-75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":15, "Overlap":-75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":20, "Overlap":-75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":25, "Overlap":-75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":30, "Overlap":-75, "ImpactSpeed": 10, "TestScenario":"CCRs"},
                    {"TestSpeed":35, "Overlap":-75, "ImpactSpeed": 10, "TestScenario":"CCRs"},
                    {"TestSpeed":40, "Overlap":-75, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":45, "Overlap":-75, "ImpactSpeed": 34, "TestScenario":"CCRs"},
                    {"TestSpeed":50, "Overlap":-75, "ImpactSpeed": 48, "TestScenario":"CCRs"},
                    {"TestSpeed":10, "Overlap":100, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":15, "Overlap":100, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":20, "Overlap":100, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":25, "Overlap":100, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":30, "Overlap":100, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":35, "Overlap":100, "ImpactSpeed": 10, "TestScenario":"CCRs"},
                    {"TestSpeed":40, "Overlap":100, "ImpactSpeed": 12, "TestScenario":"CCRs"},
                    {"TestSpeed":45, "Overlap":100, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":50, "Overlap":100, "ImpactSpeed": 38, "TestScenario":"CCRs"},
                    {"TestSpeed":10, "Overlap":75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":15, "Overlap":75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":20, "Overlap":75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":25, "Overlap":75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":30, "Overlap":75, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":35, "Overlap":75, "ImpactSpeed": 10, "TestScenario":"CCRs"},
                    {"TestSpeed":40, "Overlap":75, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":45, "Overlap":75, "ImpactSpeed": 33, "TestScenario":"CCRs"},
                    {"TestSpeed":50, "Overlap":75, "ImpactSpeed": 38, "TestScenario":"CCRs"},
                    {"TestSpeed":10, "Overlap":50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":15, "Overlap":50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":20, "Overlap":50, "ImpactSpeed": 0, "TestScenario":"CCRs"},
                    {"TestSpeed":25, "Overlap":50, "ImpactSpeed": 12, "TestScenario":"CCRs"},
                    {"TestSpeed":30, "Overlap":50, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":35, "Overlap":50, "ImpactSpeed": 22, "TestScenario":"CCRs"},
                    {"TestSpeed":40, "Overlap":50, "ImpactSpeed": 33, "TestScenario":"CCRs"},
                    {"TestSpeed":45, "Overlap":50, "ImpactSpeed": 33, "TestScenario":"CCRs"},
                    {"TestSpeed":50, "Overlap":50, "ImpactSpeed": 48, "TestScenario":"CCRs"}]
    
    
    
    CCRs_test_scores = {}
    CCRm_test_scores = {}
    # Loop over testcase 
    for testcase in testcases:
        CCRs_test_scores.setdefault(testcase["TestSpeed"], 0.0)
        CCRm_test_scores.setdefault(testcase["TestSpeed"], 0.0)
        
        # Need to Count 100% overlap case twice
        scale = 2 if testcase["Overlap"] == 100 else 1
        
        score_color, score_value = get_bin_score(testcase["ImpactSpeed"], testcase["TestSpeed"], testcase["TestScenario"])
        
        if testcase["TestScenario"] == "CCRs":
            CCRs_test_scores[testcase["TestSpeed"]] += (score_value * scale) / 6
        elif testcase["TestScenario"] == "CCRm":
            CCRm_test_scores[testcase["TestSpeed"]] += (score_value * scale) / 6
        
    # Loop over each test speed and multiply the weight factor
    AEB_CCRs_score = 0.0    
    for test_speed in CCRs_points_AEB.keys():
        if test_speed in CCRs_test_scores.keys():
            AEB_CCRs_score += (CCRs_test_scores[test_speed] * CCRs_points_AEB[test_speed])
       
    AEB_CCRm_score = 0.0
    for test_speed in CCRm_points_AEB.keys():
        if test_speed in CCRm_test_scores.keys():
            AEB_CCRm_score += (CCRm_test_scores[test_speed] * CCRm_points_AEB[test_speed])
        
    # Scale by 4 / 14
    AEB_CCRs_score = AEB_CCRs_score * 4 / 14
    AEB_CCRm_score = AEB_CCRm_score * 4 / 14
    
    print AEB_CCRs_score, AEB_CCRm_score
        
    
        
        
        
    
    
    