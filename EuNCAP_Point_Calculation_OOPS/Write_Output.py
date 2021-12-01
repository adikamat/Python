import os
import csv
from pyHTMLReport.htmlReport import cHTMLReport, cHTMLReportTable, cHTMLReportTableRow, cHTMLReportTableCell, \
    cHTMLReportGraph, cHTMLReportGraphYData, cHTMLReportImage, cHTMLReportLink, cHTMLReportVideo, \
    cHTMLReportVerticalLine, cHTMLReportCode

class WriteOutput(object):
    _instance = None
    sim_run_output_prefix = 'TestCase_sim_'  # File name will be 'TestCase_sim_scenarioname.csv',e.g. TestCase_sim_CCRs.csv
    output_folder = './'
    report = None
    warning_list = []

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            # print('Creating new instance')
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance

    def set_output_folder(self, output_folder):
        self.output_folder = output_folder

    def set_report_title(self, title):
        self.report = cHTMLReport(title=title, theme="contimodern", toc=True)

    def write_to_csv(self, csv_rows, scenario_name):
        # Write CSV file
        with open(os.path.join(self.output_folder, self.sim_run_output_prefix + scenario_name + '.csv'),
                  'wb') as my_csv_file:
            my_csv_writer = csv.writer(my_csv_file, delimiter=';')
            my_csv_writer.writerows(csv_rows)

    def add_to_warn_list(self, warning):
        if isinstance(warning, list):
            self.warning_list.extend(warning)
        else:
            self.warning_list.append(warning)

    def add_table_to_report(self, section_name, table_name, rows):

        self.report.SectionBegin(section_name)
        # self.report.AddText("Input Filename: " + ',\n'.join(input_files))
        # numTests = [len(testcase_dataset[k]) for k in testcase_dataset.keys()]
        entryTable = cHTMLReportTable(table_name, sortable=False)
        entryTable.setHeaderRow(cHTMLReportTableRow(cells=rows[0]))
        for i in range(1, len(rows)):
            entryTable.addRow(cHTMLReportTableRow(cells=rows[i]))
        self.report.AddTable(entryTable)
        self.report.SectionEnd()

    def save_report(self):
        # Add warnings to report
        self.report.SectionBegin("Warnings and Errors")
        self.report.AddText("List of Errors and Problems when running the script")

        warnListTable = cHTMLReportTable("Warnings and Errors", sortable=False)
        warnListTable.setHeaderRow(cHTMLReportTableRow(cells=["Sr. No.", "Warnings"]))
        for i, w in enumerate(self.warning_list):
            warnListTable.addRow(cHTMLReportTableRow(cells=[str(i), w]))
        self.report.AddTable(warnListTable)
        self.report.SectionEnd()

        self.report.Save(os.path.join(self.output_folder, 'HTMLReport', "test_report.html"))
