import clr
clr.AddReference("ASAP2")
from jnsoft.ASAP2 import A2LParser, A2LPROJECT, A2LCHARACTERISTIC, A2LCharDict, WriterSortMode

a2l_parser = A2LParser()
a2l_parser.parse("BasicTest.a2l")

char_dict = a2l_parser.Project.CharDict.Keys

for k in char_dict:
    print "Reading", k
    a2l_char = a2l_parser.Project.CharDict.get_Item(k)
    print "Characteristic", k, "is of type", a2l_char.CharType, "and address", hex(a2l_char.Address)
    print "Matrix Dim is", a2l_char.MatrixDim, "and Number is", a2l_char.Number
    print ""

print "\nDone"
