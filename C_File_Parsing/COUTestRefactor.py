import os
import sys


class COU2GTEST:

    def __init__(self):
        self.files_for_refactoring = []
        self.cou_test_define_names = []
        self.src_dir = ''
        self.dst_dir = ''

    def add_cou_test_alias(self, line, line_no):
        # Split across spaces for #define
        if "COU_TEST" in line:
            entries = line.strip().split(" ")
            entries = ' '.join(entries).split()
            if len(entries) < 3:
                print("Invalid #define at line number " + str(line_no))
                new_line = line + "\n"
            else:
                self.cou_test_define_names.append(entries[1])
                new_line = ""
        else:
            new_line = line + "\n"
        return new_line

    @staticmethod
    def convert_cou_test(line, line_no):
        # Remove leading and trailing spaces
        # Remove string "COU_TEST"
        stripped_line = line.strip()[8:]
        new_line = "TEST" + stripped_line + "\n"
        return new_line

    @staticmethod
    def convert_alias_cou_test(line, line_no):
        # Remove the function name and keep the rest
        entries = line.strip().split("(")
        if len(entries) < 2:
            print("Invalid COU_TEST at line number " + str(line_no))
            new_line = line
        else:
            new_line = "TEST(" + entries[1].replace('"', '') + "\n"
        return new_line

    @staticmethod
    def convert_cou_assert(line, line_no):
        # Remove leading and trailing spaces
        # Remove string "COU_ASSERT_EQ", ";", and "()"
        stripped_line = line.strip()[17:-2]
        entries = stripped_line.split(",")
        if len(entries) < 3:
            print("Invalid COU_ASSERT_EQ at line number " + str(line_no))
            new_line = stripped_line
        else:
            new_line = "    //" + entries[2] + "\n"
            new_line += "    EXPECT_EQ(" + entries[0] + " , " + entries[1] + ");\n"
        return new_line

    @staticmethod
    def convert_cou_call(line, line_no):
        # Remove leading and trailing spaces
        # Remove string "COU_CALL", ";", and "()"
        stripped_line = line.strip()[9:-2]
        entries = stripped_line.split('"')
        if len(entries) < 2:
            print("Invalid COU_CALL at line number " + str(line_no))
            new_line = stripped_line
        else:
            # func_call = ",".join(entries[0:-1])
            # new_line = "    //" + entries[-1] + "\n"
            # new_line += "    " + func_call + ";\n"
            new_line = "    //" + entries[1] + "\n"
            new_line += "    " + entries[0].strip()[:-1] + ";\n"
        return new_line

    @staticmethod
    def convert_cou_set(line, line_no):
        # Remove leading and trailing spaces
        # Remove string "COU_SET", ";", and "()"
        stripped_line = line.strip()[8:-2]
        entries = stripped_line.split(",")
        if len(entries) < 3:
            print("Invalid COU_SET at line number " + str(line_no))
            new_line = stripped_line
        else:
            new_line = "    //" + entries[2] + "\n"
            new_line += "    " + entries[0] + " = " + entries[1].strip() + ";\n"
        return new_line

    def detect_cou_test_define(self, line, line_no):
        entries = line.strip().split("(")
        if entries[0] in self.cou_test_define_names:
            return True
        else:
            return False

    def convert_line(self, line, line_no):
        if "#define" in line:
            new_line = self.add_cou_test_alias(line, line_no)
        elif "COU_SET" in line:
            new_line = self.convert_cou_set(line, line_no)
        elif "COU_CALL" in line:
            new_line = self.convert_cou_call(line, line_no)
        elif "COU_ASSERT" in line:
            new_line = self.convert_cou_assert(line, line_no)
        # elif "COU_TEST" in line:
        #     new_line = self.convert_cou_test(line, line_no)
        elif any(word in line for word in
                 ["cou_test_t", "COU_ADD_TEST", "COU_ADD_TEST_END", "COU_INIT", "cou_suite_t", "COU_ADD_SUITE",
                  "COU_ADD_SUITE_END", "mockup.h"]):
            new_line = "\n"
        elif "courage.h" in line:
            new_line = '#include "test_scripts/medic_test_setup.h"'
        elif self.detect_cou_test_define(line, line_no):
            new_line = self.convert_alias_cou_test(line, line_no)
        else:
            new_line = line + "\n"

        return new_line

    def convertFile(self, file):
        fh = open(file, "r")
        contents = fh.read()
        fh.close()

        lines = contents.split("\n")

        new_filename = file.replace(self.src_dir, self.dst_dir)
        # Converting .c files to .cpp
        if new_filename.endswith('.c'):
            new_filename += 'pp'
        head, tail = os.path.split(new_filename)
        if not os.path.isdir(head):
            os.makedirs(head)
        # new_filename = os.path.join(self.dst_dir, tail)
        with open(new_filename, "w") as f:
            new_code = []
            line_no = 0
            multi_line_comment_started = False
            code_line = ''
            for line in lines:
                line_no = line_no + 1
                stripped_line = line.strip()
                code_line = code_line + ' ' + stripped_line
                if len(code_line) == 0:
                    # Blank Line, Keep as it is
                    new_line = "\n"
                    code_line = ''
                elif stripped_line.endswith('*/'):
                    # Multi-Line Comment End, Keep as it is
                    new_line = line + "\n"
                    code_line = ''
                    multi_line_comment_started = False
                elif stripped_line.startswith("//") | multi_line_comment_started:
                    # Single-Line Comment, Keep as it is
                    #  OR
                    # Multi-Line comment was started in previous line
                    # Continue adding comments
                    # Add \n in the end of each line that we removed
                    new_line = line + "\n"
                    code_line = ''
                elif stripped_line.startswith("/*"):
                    # Multi-Line Comment Start
                    # Continue adding lines till */ token is found
                    # Add \n in the end of each line that we removed
                    new_line = line + "\n"
                    multi_line_comment_started = True
                elif stripped_line.startswith("cou_test_t"):
                    # The code below this line is not used in GTest
                    # Stop parsing
                    new_line = "\n"
                    break
                elif stripped_line.endswith(')') | stripped_line.endswith(';') | \
                        stripped_line.endswith('{') | stripped_line.endswith('}') | \
                        stripped_line.startswith('#'):
                    # Complete code line available, convert it
                    new_line = self.convert_line(code_line, line_no)
                    code_line = ''
                else:
                    # Complete code line not available.
                    # code_line already contains current line
                    # Proceed to search in next line
                    continue
                new_code.append(new_line)

            f.write("".join(new_code))

    def convert(self, src, dst):
        files_for_refactoring = self.recurse_dir(src)
        self.src_dir = src
        self.dst_dir = dst
        i = 1
        for filename in files_for_refactoring:
            print "Processing File " + filename + " (" + str(i) + " out of " + str(len(files_for_refactoring)) + ")"
            self.convertFile(filename)
            del self.cou_test_define_names[:]
            i = i + 1

    def recurse_dir(self, directory):

        files_for_refactoring = []

        list_of_files = os.listdir(directory)
        # print list_of_files

        for curr_file in list_of_files:
            # print file
            if curr_file.endswith("cpp") | curr_file.endswith('.c') | curr_file.endswith('.h'):
                name = os.path.join(directory, curr_file)
                files_for_refactoring.append(name)

            elif os.path.isdir(os.path.join(directory, curr_file)):
                files_for_refactoring.extend(self.recurse_dir(os.path.join(directory, curr_file)))

        return files_for_refactoring


if __name__ == "__main__":

    if len(sys.argv) == 1:
        src_directory = 'D:/Aditya/Sandboxes/LCA_LaneChangeAssist/05_Testing/05_Test_Environment/Dynamic_Tests/LCA/Courage'
        dst_directory = 'D:/Aditya/Sandboxes/LCA_LaneChangeAssist/05_Testing/05_Test_Environment/Dynamic_Tests/LCA/converter'
    elif len(sys.argv) < 3:
        print "Exactly 2 arguments reqd. Call the script with foloowing format: COUTestRefactor src_dir dest_dir"
    else:
        src_directory = sys.argv[1]
        dst_directory = sys.argv[1]


    Converter = COU2GTEST()
    Converter.convert(src_directory, dst_directory)

    print "Done."
