# from lxml import etree
import xml.etree.ElementTree as etree
import xml.dom.minidom as dom

# def prettify(elem):
#     """Return a pretty-printed XML string for the Element.
#     """
#     rough_string = etree.ElementTree.tostring(elem, 'utf-8')
#     reparsed = minidom.parseString(rough_string)
#     return reparsed.toprettyxml(indent="  ")
#
#
# msrsw = etree.Element("MSRSW")
# sw_systems = etree.SubElement(msrsw, "SW-SYSTEMS")
# sw_system = etree.SubElement(sw_systems, "SW-SYSTEM")
# sw_instance_spec = etree.SubElement(sw_system, "SW-INSTANCE-SPEC")
# sw_instance_tree = etree.SubElement(sw_instance_spec, "SW-INSTANCE-TREE")
# sw_instance_tree_origin = etree.SubElement(sw_instance_tree, "SW-INSTANCE-TREE-ORIGIN")
# sw_instance = etree.SubElement(sw_instance_tree, "SW-INSTANCE")
# sw_phys_values = etree.SubElement(sw_instance, "SW-VALUES-PHYS")
# value_text = etree.SubElement(sw_phys_values, "VT")
#
# print(prettify(msrsw))


def add_element(parent, element_tag_name, attributes={}, tag_value=''):
    tempChild = doc.createElement(element_tag_name)
    if tag_value != '':
        nodeText = doc.createTextNode(tag_value)
        tempChild.appendChild(nodeText)
    for attr in attributes.keys():
        tempChild.setAttribute(attr, attributes[attr])

    parent.appendChild(tempChild)
    return tempChild


if __name__ == '__main__':
    doc = dom.Document()

    msrsw = add_element(doc, "MSRSW", {"CREATOR-VERSION": "V2.1.0",
                                       "CREATOR": 'HEAD Autocoder'})
    msrsw_category = add_element(msrsw, "CATEGORY", {}, 'CDF21')
    sw_systems = add_element(msrsw, "SW-SYSTEMS")
    sw_system = add_element(sw_systems, "SW-SYSTEM")
    sw_instance_spec = add_element(sw_system, "SW-INSTANCE-SPEC")
    sw_instance_tree = add_element(sw_instance_spec, "SW-INSTANCE-TREE")
    sw_instance_tree_category = add_element(sw_instance_spec, "CATEGORY", {}, 'NO_VCD')
    sw_instance_tree_origin = add_element(sw_instance_tree, "SW-INSTANCE-TREE-ORIGIN")
    sw_instance = add_element(sw_instance_tree, "SW-INSTANCE")
    sw_phys_values = add_element(sw_instance, "SW-VALUES-PHYS")
    value = add_element(sw_phys_values, "V", {'xml:space': "preserve"}, '0')

    doc.writexml(open('MySampleCDFX.cdfx', 'w'),
                 indent="  ",
                 addindent="  ",
                 newl='\n')

    doc.unlink()

