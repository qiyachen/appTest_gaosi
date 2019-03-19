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
    reportFile =  now + "Report.txt"

    #暂时没想好报告导出什么数据，怎么展示#