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
    root = tree.getroot()
    prettyXml(root, '\t', '\n')            #执行美化方法
    tree.write(out_path,encoding="utf-8")

# elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
def prettyXml(element, indent, newline, level = 0): 
    if element: #判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作
