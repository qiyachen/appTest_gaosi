import configparser    #导入configparser库，用于读取配置文件
import os

class ReadConfig():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')    #获取制定配置文件所在路径
        self.config.read(self.conf_path, encoding='utf-8-sig')     #读取配置文件，编码格式为utf-8-sig

        self.conf = {
            'phone': '',
            'password_test': '',
            'password_product': '',
            'test_url': '',
            'product_url':''
        }

    def get_conf(self):
        """
        配置文件读取，并赋值给全局参数
        :return:
        """
        self.conf['phone'] = self.config.get("app_user_info", 'phone')
        self.conf['password_test'] = self.config.get("app_user_info", "password_test")
        self.conf['password_product'] = self.config.get("app_user_info", "password_product")
        self.conf['test_url'] = self.config.get("url", "test_url")
        self.conf['product_url'] = self.config.get("url", "product_url")
        return self.conf

if __name__ == '__main__':
    ReadConfig()