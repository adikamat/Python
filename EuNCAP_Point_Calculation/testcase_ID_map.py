import csv
input_file = 'Testcase_ID_mapping.csv'

mydict = {}
with open(input_file, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[3] in mydict.keys():
            print 'Multiple values for ' + row[3]
        else:
            mydict[row[3]] = row[0]

print mydict