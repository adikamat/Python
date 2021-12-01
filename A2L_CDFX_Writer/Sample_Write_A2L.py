import clr
clr.AddReference("ASAP2")
from jnsoft.ASAP2 import A2LParser, A2LPROJECT, A2LCHARACTERISTIC, A2LCharDict, A2LMODULE, A2LNODE, CHAR_TYPE,\
    CONVERSION_TYPE, WriterSortMode

# a2l_char = A2LCHARACTERISTIC()
a2l_parser = A2LParser()
a2l_parser.parse("Empty.a2l")
a2l_parser.Project.CharDict = A2LCharDict()
module_node = a2l_parser.Project.getNode[A2LMODULE](False)

# Create a new compu method
a2l_compu_method = a2l_parser.create(module_node, "COMPU_METHOD")
a2l_compu_method.Name = "NewCompuMethod"
a2l_compu_method.Description = "Some Long Description. Blah Blah"
a2l_compu_method.ConversionType = CONVERSION_TYPE.IDENTICAL
a2l_compu_method.Format  = "%4.2"
a2l_compu_method.Unit = "m/s^2"
# Add compu method to project
a2l_parser.Project.CompDict.Add("NewCompuMethod", a2l_compu_method)

# Create a new compu vtab
a2l_compu_vtab = a2l_parser.create(module_node, "COMPU_VTAB")
a2l_compu_vtab.Name = "NewCompuVTab"
a2l_compu_vtab.Description = "Some Long Description. Blah Blah"
a2l_compu_vtab.ConversionType = CONVERSION_TYPE.TAB_VERB
a2l_compu_vtab.Verbs.Add(1.0, "Meh!")
# a2l_compu_vtab.NumberValuePairs  = "%4.2"
# a2l_compu_vtab.Unit = "m/s^2"
# Add compu vtab to project
a2l_parser.Project.CompVTabDict.Add("NewCompuVTab", a2l_compu_vtab)

# Create a new record layout
a2l_record_layout = a2l_parser.create(module_node, "RECORD_LAYOUT")
a2l_record_layout.Name = "MyNewRecLay"
# Add record layout to project
a2l_parser.Project.RecLayDict.Add("MyNewRecLay", a2l_record_layout)

# Create a new characteristic
a2l_char = a2l_parser.create(module_node, "CHARACTERISTIC")
a2l_char.CharType = CHAR_TYPE.VALUE
a2l_char.Address = int('0x119AE30', 16)
a2l_char.Description = "Some long description"
a2l_char.RecordLayout = "MyNewRecLay"
a2l_char.MaxDiff = 0.0
a2l_char.Conversion = 'NO_COMPU_METHOD'
a2l_char.LowerLimit = 0
a2l_char.UpperLimit = 65535
a2l_char.Name = "Adi"
# Add characteristic to project
a2l_parser.Project.CharDict.Add("Adi", a2l_char)

print a2l_parser.write("./Sample.a2l", WriterSortMode.None, False, False)
