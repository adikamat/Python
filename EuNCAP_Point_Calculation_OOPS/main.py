import ncap_standards as ncap_std
from Write_Output import *
from Export_To_Document import Export2Document

################################################
#    INPUT SECTION
################################################
input_files = ['19W46/2018/ValidReport_20200220_AL_ARS510TA19_03.02.00_INT-20_EU18.csv']

output_folder = './output'
output_file = 'Data.csv'
sim_run_scores = 'Simulation_score_scenario_wise.csv'


# Select the no. of runs to simulate for monte-carlo simulations
SIM_RUN_LENGTH = 1000  # 0

# Select if each run of monte carlo is exported to csv file
EXPORT_TO_CSV = True

# Select the NCAP Standard to run
# Options:
#         1. 'EU_2018' - EuNCAP 2018
#         2. 'EU_2020' - EuNCAP 2020
#         3. 'JN_2018' - JNCAP 2018

ncap_standard_to_run = 'EU_2018'

################################################
#    END OF INPUT SECTION
################################################

if __name__ == "__main__":

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    if not os.path.isdir(os.path.join(output_folder, 'HTMLReport')):
        os.makedirs(os.path.join(output_folder, 'HTMLReport'))

    if ncap_standard_to_run == 'EU_2020':
        ncap = ncap_std.EuNCAP_2020()
    elif ncap_standard_to_run == 'EU_2018':
        ncap = ncap_std.EuNCAP_2018()
    elif ncap_standard_to_run == 'JN_2018':
        ncap = ncap_std.JNCAP_2018()
    else:
        raise RuntimeError('Invalid NCAP Standard Selected: ' + ncap_standard_to_run)

    # Instantiate output writer object
    out_writer = WriteOutput.instance()
    out_writer.set_output_folder(output_folder)
    out_writer.set_report_title(ncap.name + " Point Calculation Report")

    ncap.read_csv_report(input_files)
    ncap.calc_stats()
    # ncap.print_stats()

    out_writer.save_report()

    pptx_exporter = Export2Document(ncap)
    pptx_exporter.export_data()

    print "Done"


