# -*- coding: utf-8 -*-
import unittest
import os
import xlrd
import time
import copy
from config import readConfig
from api.app import shoppingCart,login

class PlaceOrder(unittest.TestCase):
    def setUp(self):
        '''初始化数据'''
        print("-初始化-")
        '''获得utoken/student_code'''
        conf = readConfig.ReadConfig().get_conf()
        phone = conf["phone"]
        psw = conf["password_test"]
        resp = login.loginByPassword(phone,psw)
        self.uToken = resp["AppendData"][0]["LoginToken"]
        self.studentCode = resp["AppendData"][0]["Code"]

        '''获得class_codes'''
        file_path = os.path.join(os.path.abspath('..').split('src')[0] + "/testFile/placeOrder.xlsx")
        workbook = xlrd.open_workbook(file_path)
        table = workbook.sheet_by_index(0)
        rows = table.nrows
        i = 1
        self.classCodes = []
        for i in range(rows):
            self.classCodes.append(table.cell(i, 0).value)
        time.sleep(1)

    def test_placeOrder(self):
        ''''
        完成 添加选课单->查看选课单->计算订单
        '''
        print("-测试支付订单开始-")
        print('测试课程为：'+str(self.classCodes))
        time.sleep(1)

        '''查看选课单'''
        cart_resp = shoppingCart.shoppingCartList(self.uToken,self.studentCode)
        time.sleep(1)

        '''清空选课单内有效课程，防止课程重复添加'''
        rmList= []
        for classes in cart_resp["AppendData"]["Items"]:
            rmList.append(classes["Items"][0]["Code"])
        for classes in cart_resp["AppendData"]["InvalidItems"]:
            rmList.append(classes["Code"])
        shoppingCart.removeShoppingCart(self.uToken,self.studentCode,rmList)
        time.sleep(1)

        '''将课程添加至选课单'''
        shoppingCart.addShoppingCart(self.uToken, self.studentCode, self.classCodes, False)
        time.sleep(1)

        '''查看选课单'''
        cart_resp = shoppingCart.shoppingCartList(self.uToken, self.studentCode)
        time.sleep(1)


        '''计算价格'''
        calc_items = []
        for classes in cart_resp["AppendData"]["Items"]:
            for details in classes["Items"]:
                i = {}
                i["ClassCode"] = details["Code"]
                for parts in details["Items"]:
                    i["StartLessonNo"] = parts["StartLessonNo"]
                    i["LessonNum"] = parts["LessonNum"]
                    new_i = copy.deepcopy(i)
                    calc_items.append(new_i)
                    print(str(calc_items))
        shoppingCart.calcPrice(self.uToken,calc_items,self.studentCode) #不使用优惠券



if __name__ == '__main__':
    PlaceOrder()