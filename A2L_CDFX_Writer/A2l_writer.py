import sys
try:
    import clr
    clr.AddReference("ASAP2")
except Exception as e:
    print('Error while importing ASAP2 library')
    raise e

from jnsoft.ASAP2 import *

class A2L_writer:

    def __init__(self):
        self.a2l_parser = A2LParser()
        self.a2l_parser.parse("head_1_template.a2l")
        self.module_node = self.a2l_parser.Project.getNode[A2LMODULE](False)

    def write(self):
        self.a2l_parser.write("HEAD_Param_List.a2l", WriterSortMode.None, False, False)

    def add_compu_method_for_rat_func(self, name, long_desc, conv_type, format, coeffs, unit=''):
        """

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param conv_type: (Enum) Refer to ASAM2 standard for valid values
        :param format: (string) display format in %[<length>].<layout>
        :param coeffs: (list) list of integers of length 6 indicating co-efficients for rational polynomial
        :param unit: (string) physical unit
        :return: None
        """
        if len(coeffs) < 6:
            raise ValueError("Co-efficients parameter must have 6 entries")

        # Create a new compu method
        a2l_compu_method = self.a2l_parser.create(self.module_node, "COMPU_METHOD")
        a2l_compu_method.Name = name
        a2l_compu_method.Description = long_desc
        a2l_compu_method.ConversionType = conv_type
        a2l_compu_method.Format = format
        a2l_compu_method.Coeffs.a = coeffs[0]
        a2l_compu_method.Coeffs.b = coeffs[1]
        a2l_compu_method.Coeffs.c = coeffs[2]
        a2l_compu_method.Coeffs.d = coeffs[3]
        a2l_compu_method.Coeffs.e = coeffs[4]
        a2l_compu_method.Coeffs.f = coeffs[5]
        a2l_compu_method.Unit = unit

        # Add compu method to project
        self.a2l_parser.Project.CompDict.Add(name, a2l_compu_method)

    def add_compu_method_for_tab(self, name, long_desc, conv_type, format, compu_tab_ref, unit=''):
        """

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param conv_type: (Enum) Refer to ASAM2 standard for valid values
        :param format: (string) display format in %[<length>].<layout>
        :param compu_tab_ref: (string) COMPU_VTAB Identifier string
        :param unit: (string) physical unit
        :return: None
        """
        # Create a new compu method
        a2l_compu_method = self.a2l_parser.create(self.module_node, "COMPU_METHOD")
        a2l_compu_method.Name = name
        a2l_compu_method.Description = long_desc
        a2l_compu_method.ConversionType = conv_type
        a2l_compu_method.Format = format
        a2l_compu_method.CompuTabRef = compu_tab_ref
        a2l_compu_method.Unit = unit
        # Add compu method to project
        self.a2l_parser.Project.CompDict.Add(name, a2l_compu_method)

    def add_compu_tab(self, name, long_desc, conv_type, verb_dict):
        """
        Can be used to add all 3 types of table based computation methods:
        1) TAB_INTP
        2) TAB_NOINTP
        3) TAB_VERB

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param conv_type: (Enum) Enum values defined in ASAP2 Library. Should be one of the 3 supported types
        :param verb_dict: (Dictionary) Dictionary for entries in compu_vtab block
                                       Key: (float) Value of CHARACTERISTIC, etc. blocks
                                       Value: (string / double) Display string for verbal tables or double value for
                                                                tables with and without interpolation
        :return: None
        """
        # Create a new compu vtab
        if conv_type in  [CONVERSION_TYPE.TAB_INTP, CONVERSION_TYPE.TAB_NOINTP]:
            a2l_compu_vtab = self.a2l_parser.create(self.module_node, "COMPU_TAB")
        elif conv_type == CONVERSION_TYPE.TAB_VERB:
            a2l_compu_vtab = self.a2l_parser.create(self.module_node, "COMPU_VTAB")
        else:
            raise AttributeError('conv_type must be one of [TAB_INTP|TAB_NOINTP|TAB_VERB]')

        a2l_compu_vtab.Name = name
        a2l_compu_vtab.Description = long_desc
        a2l_compu_vtab.ConversionType = conv_type
        for key in verb_dict.keys():
            a2l_compu_vtab.Verbs.Add(key, verb_dict[key])

        # Add compu vtab to project
        if conv_type in  [CONVERSION_TYPE.TAB_INTP, CONVERSION_TYPE.TAB_NOINTP]:
            self.a2l_parser.Project.CompTabDict.Add(name, a2l_compu_vtab)
        elif conv_type == CONVERSION_TYPE.TAB_VERB:
            self.a2l_parser.Project.CompVTabDict.Add(name, a2l_compu_vtab)
        else:
            raise AttributeError('conv_type must be one of [TAB_INTP|TAB_NOINTP|TAB_VERB]')


    def add_record_layout(self, name):
        """
        Currently, the record layouts are maintained manually.
        This function must not be used to add new record layouts

        :param name: (string)
        :return: None
        """
        # Create a new record layout
        a2l_record_layout = self.a2l_parser.create(self.module_node, "RECORD_LAYOUT")
        a2l_record_layout.Name = name
        # Add record layout to project
        self.a2l_parser.Project.RecLayDict.Add(name, a2l_record_layout)

    def add_typedef_char(self, name, long_desc, char_type, rec_lay, max_diff, conv_method,
                         min_val, max_val, bit_mask=pow(2, 64)-1):
        """

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param char_type: (enum) Enum Value, refer ASAM 2 library for enum values
        :param rec_lay: (string) Record Layout Identifier to be used
        :param max_diff: (float) Maximum float with respect to the adjustment of a table value
        :param conv_method: (string) Conversion Method Identifier to be used
        :param min_val: (double) Minimum value fo characteristic
        :param max_val: (double) Maximum value for characteristic
        :param bit_mask: (64-bit integer) Bit-mask value to apply to characteristic
        :return: None
        """
        # Create a new typedef_characteristic
        a2l_char = self.a2l_parser.create(self.module_node, "TYPEDEF_CHARACTERISTIC")
        a2l_char.Name = name
        a2l_char.Description = long_desc
        a2l_char.CharType = char_type
        a2l_char.RecordLayout = rec_lay
        a2l_char.MaxDiff = max_diff
        a2l_char.Conversion = conv_method
        a2l_char.LowerLimit = min_val
        a2l_char.UpperLimit = max_val
        a2l_char.LowerLimitEx = min_val
        a2l_char.UpperLimitEx = max_val
        a2l_char.Bitmask = bit_mask

        # Add characteristic to project
        self.a2l_parser.Project.TypeDefDict.Add(name, a2l_char)

    def add_typedef_struct(self, name, long_desc, size, struct_comp_dict):
        """

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param size: (32-bit integer) Total size of the structure in bytes
        :param struct_comp_dict: (Dictionary) Entries describe structure component.
                                              Key: Structure Component Name
                                              Value: 2-element list [TypedefName (string),
                                                                     AddressOffset (32-bit integer)]
        :return: None
        """
        # Create a new typedef_structure
        a2l_ts = self.a2l_parser.create(self.module_node, "TYPEDEF_STRUCTURE")
        a2l_ts.Name = name
        a2l_ts.Description = long_desc
        a2l_ts.Size = size

        for k, v in struct_comp_dict:
            a2l_sc = self.a2l_parser.create(a2l_ts, "STRUCTURE_COMPONENT")
            a2l_sc.Name = k
            a2l_sc.TypedefName = v[0]
            a2l_sc.AddressOffset = v[1]

        # Add characteristic to project
        self.a2l_parser.Project.TypeDefDict.Add(name, a2l_ts)

    def add_instance(self, name, long_desc, typedef_name, address):
        """

        :param name: (string) Type identifier for current block
        :param long_desc: (string) Comment, description for the type
        :param typedef_name: (string) Typedef Identifier to be used
        :param address: (string) Address for the instance
        :return: None
        """
        # Create a new instance
        a2l_instance = self.a2l_parser.create(self.module_node, "INSTANCE")
        a2l_instance.Name = name
        a2l_instance.Description = long_desc
        a2l_instance.TypedefName = typedef_name
        a2l_instance.Address = address

        # Add instance to project
        self.a2l_parser.Project.InstanceDict.Add(name, a2l_instance)


