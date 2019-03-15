from config import configAction
from common import commonAction
import json
import requests

conf = configAction.get_conf()

def accountBalance(uToken,studentCode):
    '''
    查询指定学员的高思币和余额，用于支付页面调用
    :param uToken:
    :param studentCode:
    :return:
    '''
    '''初始化数据'''
    url = conf["domain_test"] + conf["account_balance"]

    '''传参'''
    p = {"StudentCode": studentCode}
    sign = commonAction.getSign(uToken, params = p)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8"}

    '''发送请求'''
    resp = requests.post(url=url, params=json.dumps(p), headers=h)
    r = resp.json()

    '''查询成功返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("查询金库信息失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        return r