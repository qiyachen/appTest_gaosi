import os
import unittest
from testCase.test_placeOrder  import PlaceOrder
from BeautifulReport import BeautifulReport #导入哦
import time


if __name__ == '__main__':
    s1= unittest.TestLoader().loadTestsFromTestCase(PlaceOrder)

    #设置执行顺序
    list =[s1]
    suite = unittest.TestSuite(list)

    # 设置报告文件保存路径
    report_dir = os.path.abspath('.').split('src')[0] + "/testResult/"

    # 获取系统当前时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    # 设置报告名称格式
    HtmlFile =  now + "Report.html"
    result = BeautifulReport(suite)
    result.report(filename=HtmlFile, description='App接口测试报告', log_path=report_dir)