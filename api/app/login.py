from config import readConfig
from api.app import verificationCode
import json
import hashlib
import requests
from common import commonFuns

def loginByPassword(phone,password):
    '''密码登录'''

    '''初始化数据'''
    c = readConfig.ReadConfig().get_conf()
    url = c["test_url"]+"/V4/Student/LoginByPassword"

    '''传参'''
    d = {"Phone": phone, "Password": password}
    sign = commonFuns.getSign(data = d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8"}

    '''发送请求'''
    resp = requests.post(url = url, data = json.dumps(d), headers = h)
    r = resp.json()


    '''登录成功返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("登录失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        for stu in r["AppendData"]:
            print("学员 ["+ stu["Name"] +"] 登录成功")
        return r


def loginByVerificationCode(phone):
    '''验证码登录'''

    '''初始化数据'''
    c = readConfig.ReadConfig().get_conf()
    url = c["test_url"] + "/V4/Student/LoginByVerificationCode"

    '''传参'''
    d = {"Phone": phone, "VerificationCode": verificationCode.getVerificationCode(phone, '0')} #0为登录
    sign = commonFuns.getSign(data = d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8"}

    '''发送请求'''
    resp = requests.post(url = url, data = json.dumps(d), headers = h)  # 登录
    r = resp.json()

    '''登录成功返回响应'''
    try:
         assert r["ResultType"] == 0
    except AssertionError:
        print("登录失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print("登录成功")
        return r