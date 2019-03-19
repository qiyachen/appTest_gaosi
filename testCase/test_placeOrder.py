# -*- coding: utf-8 -*-
import unittest
import os
import xlrd
import time
from config import configFunction
from api.student import login,accountBalance
from api.webOrder import shoppingCart,price,order

class PlaceOrder(unittest.TestCase):
    def setUp(self):
        '''初始化数据'''
        print("-初始化-")

        '''获得token和学生编号'''
        conf = configFunction.get_conf()
        phone = conf["phone"]
        psw = conf["password_test"]
        resp = login.loginByPassword(phone, psw)
        self.uToken = resp["AppendData"][0]["LoginToken"]
        self.studentCode = resp["AppendData"][0]["Code"]

        '''获得班级编号'''
        file_path = os.path.join(os.path.abspath('..').split('src')[0] + "/testFile/placeOrder.xlsx")
        workbook = xlrd.open_workbook(file_path)
        table = workbook.sheet_by_index(0)
        rows = table.nrows
        i = 1
        self.classCodes = []
        for i in range(rows):
            self.classCodes.append(table.cell(i, 0).value)
        time.sleep(1)

        '''获得高思币和余额'''
        balance_resp = accountBalance.accountBalance(self.uToken, self.studentCode)
        self.goldCoin = balance_resp["AppendData"]["GoldCoin"]
        self.balance = balance_resp["AppendData"]["Balance"]

    def test_placeOrder(self):
        ''''
        完成 添加选课单->查看选课单->计算订单
        '''
        print("-测试支付订单开始-")
        print('测试课程为：'+str(self.classCodes))
        time.sleep(1)

        '''查看选课单'''
        cart_resp = shoppingCart.shoppingCartList(self.uToken, self.studentCode)
        time.sleep(1)

        '''清空选课单内有效课程，防止课程重复添加'''
        rmList= []
        for classes in cart_resp["AppendData"]["Items"]:
            rmList.append(classes["Items"][0]["Code"])
        for classes in cart_resp["AppendData"]["InvalidItems"]:
            rmList.append(classes["Code"])
        shoppingCart.removeShoppingCart(self.uToken, self.studentCode, rmList)
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

                for parts in details["Items"]:
                    i = {}
                    i["ClassCode"] = details["Code"]
                    i["StartLessonNo"] = parts["StartLessonNo"]
                    i["LessonNum"] = parts["LessonNum"]
                    calc_items.append(i)

        price_resp = price.calcPrice(self.uToken, calc_items, self.studentCode,self.goldCoin,self.balance) #自动选择优惠券

        '''下单'''
        order_items = []
        for class_iterator in price_resp["AppendData"]["Items"]:
            classes = {}
            classes["ClassCode"] = class_iterator["ClassCode"]
            classes["StartLessonNo"] = class_iterator["StartLessonNo"]
            classes["RegLessonNum"] = class_iterator["RegLessonNum"]
            classes["Price"] = class_iterator["Price"]
            classes["Deposit"] = class_iterator["Deposit"]
            classes["ManageFee"] = class_iterator["ManageFee"]
            classes["MaxGoldCoinPayAmount"] = class_iterator["MaxGoldCoinPayAmount"]
            classes["Coupons"] = class_iterator["Coupons"]
            order_items.append(classes)

        order_resp = order.placeOrder(self.uToken,self.studentCode,self.goldCoin,self.balance,order_items)

        '''取消订单'''
        if order_resp["ResultType"]==0:
            orderCode = order_resp["AppendData"]["OrderCode"]
            order.cancelOrder(self.uToken,self.studentCode,orderCode)







