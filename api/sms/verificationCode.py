import hashlib
import requests
from config import configAction
from common import  commonAction

def getVerificationCode(phone,type):
    '''
    获取验证码
    一分钟内同一手机只能获取一次验证码,连续获取6次验证码后，3小时内不能再次获取，不需要登录
    type:验证码用途，0-登录，1-修改密码，2-绑定手机号
    '''

    '''初始化数据'''
    conf = configAction.get_conf()
    url = conf["domain_test"] + conf["verification_code"]

    '''传参'''
    p = {"phone": phone, "type": type}
    sign = commonAction.getSign(params = p)
    h = {"sign": sign, "partner": "10016"}

    '''发送请求'''
    resp = requests.get(url = url, params = p, headers = h)
    r = resp.json()
    code = r["AppendData"]

    '''获取成功返回验证码'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("获得验证码失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print("验证码为:" + code)
        return code