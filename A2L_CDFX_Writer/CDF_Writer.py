import xml.dom.minidom as dom

class CDF_Writer:

    def add_element(self, parent, element_tag_name, attributes=None, tag_value=''):
        if attributes is None:
            attributes = {}
        tempChild = self.doc.createElement(element_tag_name)

        nodeText = self.doc.createTextNode(tag_value)
        tempChild.appendChild(nodeText)

        for attr in attributes.keys():
            tempChild.setAttribute(attr, attributes[attr])

        parent.appendChild(tempChild)
        return tempChild

    def __init__(self):
        self.doc = dom.Document()

        msrsw = self.add_element(self.doc, "MSRSW", {"CREATOR-VERSION": "V2.1.0",
                                                     "CREATOR": 'HEAD Autocoder'})

        msrsw_category = self.add_element(msrsw, "CATEGORY", {}, 'CDF21')
        sw_systems = self.add_element(msrsw, "SW-SYSTEMS")
        sw_system = self.add_element(sw_systems, "SW-SYSTEM")
        sw_instance_spec = self.add_element(sw_system, "SW-INSTANCE-SPEC")
        self.sw_instance_tree = self.add_element(sw_instance_spec, "SW-INSTANCE-TREE")
        sw_instance_tree_category = self.add_element(self.sw_instance_tree, "CATEGORY", {}, 'NO_VCD')
        sw_instance_tree_origin = self.add_element(self.sw_instance_tree, "SW-INSTANCE-TREE-ORIGIN")
        sym_file = self.add_element(sw_instance_tree_origin, "SYMBOLIC-FILE", {}, "HEAD_Param_list.a2l")

    def write(self):
        self.doc.writexml(open('MySampleCDFX.cdfx', 'w'),
                     indent="  ",
                     addindent="  ",
                     newl='\n')

        self.doc.unlink()

    def add_value_instance(self, parent, short_name, unit, value):

        sw_instance_param_type = self.add_element(parent, "SW-INSTANCE")
        short_name = self.add_element(sw_instance_param_type, 'SHORT-NAME', {}, short_name)
        category = self.add_element(sw_instance_param_type, 'CATEGORY', {}, 'VALUE')
        sw_value_cont = self.add_element(sw_instance_param_type, "SW-VALUE-CONT")
        unit = self.add_element(sw_value_cont, "UNIT-DISPLAY-NAME", {'xml:space': "preserve"}, unit)
        sw_phys_values = self.add_element(sw_value_cont, "SW-VALUES-PHYS")
        if isinstance(value, basestring):
            value = self.add_element(sw_phys_values, "VT", {'xml:space': "preserve"}, value)
        else:
            value = self.add_element(sw_phys_values, "V", {}, str(value))

    def add_scalar_structure_instance(self, name, HEADParam_Scalar):

        try:
            unit = HEADParam_Scalar['Unit']
        except KeyError:
            unit = ''

        # Create sw instance for Scalar HEAD Parameter structure
        sw_instance_struct_root = self.add_element(self.sw_instance_tree, "SW-INSTANCE")
        short_name = self.add_element(sw_instance_struct_root, 'SHORT-NAME', {}, name)
        category = self.add_element(sw_instance_struct_root, 'CATEGORY', {}, 'STRUCTURE')

        # Create sw instance for for first entry of structure: ParameterType
        sw_instance_param_type = self.add_element(sw_instance_struct_root, "SW-INSTANCE")
        short_name = self.add_element(sw_instance_param_type, 'SHORT-NAME', {}, 'ParameterType')
        category = self.add_element(sw_instance_param_type, 'CATEGORY', {}, 'STRUCTURE')

        # Add entries for ParameterTypes field
        for entry in ['ParameterMainType', 'ParameterMainValueType', 'ParameterOperator',
                      'ParameterOutType', 'ParameterMode', 'ParameterHypObjectClass',
                      'ParameterDynamicProperty', 'ParameterHypSubType', 'ParameterSensorSubType',
                      'ParameterObjectMovementDirection']:
            self.add_value_instance(sw_instance_param_type, entry, unit, HEADParam_Scalar[entry])

        # Add entries for next address field
        self.add_value_instance(sw_instance_struct_root, 'NextParamPointer', unit, 0)

        # Add entries for next relevant address field
        self.add_value_instance(sw_instance_struct_root, 'NextRelevantParamPointer', unit, 0)

        # Add entries for next relevant address field
        self.add_value_instance(sw_instance_struct_root, 'SpecialParInfo', unit, HEADParam_Scalar['BitPack'])

        # Add entries for next relevant address field
        self.add_value_instance(sw_instance_struct_root, 'f16RawValue', unit, HEADParam_Scalar['ParameterScalarValue'])
