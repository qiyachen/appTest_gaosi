import json
import requests
from common import commonAction,commonEnum
from config import configAction


conf = configAction.get_conf()
semester = commonEnum.semester

def calcPrice(uToken,items,studentCode,goidCoin = None,balance = None,choosedCoupon = False,selectedCouponIds = None):
    '''
    计算报名指定班级的价格和享受的优惠，可以使用优惠劵
    :param uToken:token
    :param items: 班级信息
    :param studentCode: 学生编码
    :param choosedCoupon: 选择优惠券 默认未选择
    :param selectedCouponIds:优惠券编码 选填项
    :return: 响应数据
    '''

    '''初始化数据'''
    url = conf["domain_test"]+ conf["calc_price"]

    '''传参'''
    d = {
        "StudentCode": studentCode,
        "Channel": 6,
        "ChoosedCoupon": False,
        "Items": items
         }
    if choosedCoupon == True and selectedCouponIds != None:
        d["ChoosedCoupon"]= True
        d["SelectedCouponIds"] = selectedCouponIds
    elif choosedCoupon == True and selectedCouponIds != None:
        print("计算价格参数有误！")

    sign = commonAction.getSign(uToken, data = d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken": uToken}

    '''发送请求'''
    resp = requests.post(url=url, data=json.dumps(d), headers=h)  # 计算优惠
    r = resp.json()

    '''计算后返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("计算价格失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print("计算价格成功:")
        print("课程信息：")
        print("-")
        for class_iterator in  r["AppendData"]["Items"]:
            sem = semester[class_iterator["Semester"]]

            print(class_iterator["ClassName"]+" "+class_iterator["ClassCode"])
            for part_iterator in class_iterator["Items"]:
                print("     "+sem+part_iterator["Section"]+": ￥"+str(round(part_iterator["Price"])))
            if class_iterator["ManageFee"] != 0.0:
                print("管理费：￥" + str(class_iterator["ManageFee"]))
            if class_iterator["Deposit"] != 0.0:
                print("押金：￥"+ str(class_iterator["Deposit"]))
            if class_iterator["Coupons"] !=[]:
                print("班级优惠明细：")
                for coupon_iterator in class_iterator["Coupons"]:
                    print("     "+coupon_iterator["CouponPolicyName"]+":￥"+str(round(coupon_iterator["Amount"])))
            print("-")
        print("结算明细：")
        print("课程总数："+ str(r["AppendData"]["ClassNum"])+"个")
        print("课程费用：￥"+ str(round(r["AppendData"]["TotalPrice"])))
        if r["AppendData"]["TotalDeposit"] != 0.0:
            print("总押金￥："+ str(r["AppendData"]["TotalDeposit"]))
        if r["AppendData"]["TotalManageFee"] != 0.0:
            print("总管理费：￥" + str(r["AppendData"]["TotalManageFee"]))
        if not r["AppendData"]["MemberCoupons"] is None:
            print(r["AppendData"]["MemberCoupons"]["CouponPolicy"]+":￥"+str(round(r["AppendData"]["MemberCoupons"]["Amount"])))
            for items_iterator in r["AppendData"]["MemberCoupons"]["Items"]:
                print("     "+items_iterator["CouponPolicyName"]+":￥"+str(round(items_iterator["Amount"])))
        if not r["AppendData"]["CDAndSysCoupons"] is None:
            print(r["AppendData"]["CDAndSysCoupons"]["CouponPolicy"]+":￥"+str(round(r["AppendData"]["CDAndSysCoupons"]["Amount"])))
            for items_iterator in r["AppendData"]["CDAndSysCoupons"]["Items"]:
                print("     " + items_iterator["CouponPolicyName"] + ":￥" + str(round(items_iterator["Amount"])))
        print("优惠券："+r["AppendData"]["CouponUsedStatus"]["Tips"]+":￥"+str(round(r["AppendData"]["CouponUsedStatus"]["Amount"])))
        g = min(r["AppendData"]["MaxGoldCoinAmount"],goidCoin)
        if goidCoin != 0.00:
            print("高思币：共"+str(int(goidCoin))+"个,本次使用"+str(int(g)))
        if balance != 0.00:
            print("余额：￥"+str(balance))
        print("合计：￥" + str(round(r["AppendData"]["AmountPayable"])))
        return r