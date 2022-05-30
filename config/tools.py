import re


def find_all_data(data, lb='', rb=''):
    rule = lb + r'(.+?)' + rb
    data_list = re.findall(rule, data)
    return data_list
