import configparser    #导入configparser库，用于读取配置文件
import os

'''实例化配置文件'''
config = configparser.ConfigParser()
conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
config.read(conf_path, encoding='utf-8-sig')

'''配置文件信息'''
conf = {}


def get_conf():
    """
    配置文件读取，并赋值给全局参数
    :return:
    """
    for section_iterator in config.sections():
        items = config.items(section_iterator)
        for items_iterator in items:
            key = items_iterator[0]
            value = items_iterator[1]
            conf[key] = value

    return conf

def set_conf(conf):
    """
    配置文件读取,为其赋值
    :return:
    """

