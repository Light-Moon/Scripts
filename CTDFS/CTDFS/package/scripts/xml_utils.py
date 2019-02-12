# -*- coding:utf-8 -*-
from xml.etree.ElementTree import ElementTree,Element
def write_xml(dict, out_path):
    '''''
    :param dict:key-value集合
    :param out_path:xml文件输出路径
    :return:新建一个xml文件
    '''
    configuration = Element('configuration')
    for key in dict:
        property = Element('property')
        configuration.append(property)
        name = Element('name')
        name.text = key
        property.append(name)
        value = Element('value')
        value.text = dict.get(key, '')
        property.append(value)
    tree = ElementTree(configuration)
    tree.write(out_path,encoding="utf-8")
