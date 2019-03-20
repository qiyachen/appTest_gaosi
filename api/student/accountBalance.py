from config import configFunction
from common import commonFunction
import json
import requests

conf = configFunction.get_conf()

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
    p = {"StudentCode":studentCode}
    sign = commonFunction.getSign(uToken, params=p)
    h = {"sign": sign,"uToken":uToken, "partner": "10016"}

    '''发送请求'''
    resp = requests.get(url=url, params= p, headers=h)
    r = resp.json()

    '''查询成功返回响应'''

    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("查询金库信息失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        return r

if __name__ == '__main__':
    a = {"StudentCode":"BJ213965"}
    commonFunction.getSign('d2abc64e24e74a158f283282197bf926', params=a)
    commonFunction.getSign('d2abc64e24e74a158f283282197bf926', data = a)
    print("49aaff8b7b3727e41c1bd90507616dc1")