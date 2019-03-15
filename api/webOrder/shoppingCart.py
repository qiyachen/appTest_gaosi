from config import configAction
import json
import requests
from common import commonAction,commonEnum

conf =  configAction.get_conf()
semester = commonEnum.semester

def addShoppingCart(uToken,studentCode,classCodes,isPromoted):
    '''
    添加班级到指定学员的购物车中，不允许重复添加
    :param uToken:
    :param studentCode:
    :param classCodes:
    :param isPromoted:
    :return:
    '''

    '''初始化数据'''
    url = conf["domain_test"] + conf["add_shopping_cart"]

    '''传参'''
    d = {"StudentCode": studentCode,
        "ClassCodes": classCodes,
        "IsPromoted": isPromoted
        }
    sign = commonAction.getSign(uToken, data = d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken":uToken }

    '''发送请求'''
    resp = requests.post(url = url, data = json.dumps(d), headers = h)  #添加购物车
    r = resp.json()

    '''添加成功返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("添加购物车失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print(str(classCodes) + "已成功添加购物车")
        return r

def removeShoppingCart(uToken,studentCode,classCodes):
    '''
    移除购物车,把班级从学员的购物车中移除
    :param uToken:
    :param studentCode:
    :param classCodes:
    :return:
    '''

    '''初始化数据'''
    url = conf["domain_test"] + conf["remove_shopping_cart"]

    '''传参'''
    d = {"StudentCode": studentCode,
        "ClassCodes": classCodes,
        }
    sign = commonAction.getSign(uToken, data = d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken":uToken }

    '''发送请求'''
    resp = requests.post(url = url, data = json.dumps(d), headers = h)  #移除购物车
    r = resp.json()

    '''移除成功返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("移除购物车失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print(str(classCodes) + "已成功移除购物车")
        return r


def shoppingCartList(uToken,studentCode):
    '''
    获取指定学员的购物车内班级列表
    :param uToken:
    :param studentCode:
    :return:
    '''

    '''初始化数据'''
    url = conf["domain_test"] + conf["shopping_cart_list"]

    '''传参'''
    p = {"StudentCode": studentCode}
    sign = commonAction.getSign(uToken, params = p)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken": uToken}

    '''发送请求'''
    resp = requests.get(url=url, params=p, headers=h)  # 计算优惠
    r = resp.json()

    '''选课单获取成功返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("选课单获取失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print("选课单获取成功：")
        for classes in r["AppendData"]["Items"]:
            sem = semester[classes["Items"][0]["Semester"]]
            print("有效课程" +": "+str(classes["Items"][0]["Name"])+" "+str(classes["Items"][0]["Code"]))
            for parts in classes["Items"][0]["Items"]:
                if parts["Purchased"] == True :
                     price = '已购买'
                else:
                    price = str(round(parts["Price"]))
                if parts["StartLessonNo"] == parts["EndLessonNo"]:
                    print("     "+sem +"-"+ parts["Section"]+":"+"第"+str(parts["StartLessonNo"])+"次课")
                else:
                    print("     "+sem +"-"+ parts["Section"]+":"+
                          "第" +str(parts["StartLessonNo"]) + "-"+ str(parts["EndLessonNo"]) +"次课:￥"+price )
        for classes in r["AppendData"]["InvalidItems"]:
            print("失效课程" + ": " + str(classes["Name"]) + " " + str(classes["Code"]))

        return r

