from urllib.parse import urlencode
import json
import hashlib

'''基本操作'''

def getSign(uToken = None,params = None,data = None):
    '''
    获取验证签名的sign值
    :param uToken: token  类型string
    :param data: url中键值对 类型dict
    :param body: 正文信息 类型dict
    :return: sign的MD5 类型string
    '''
    '''根据签名规则文档 获取sign值 文档见 http://47.94.40.214:8098/RegTest/help.html'''
    '''1.取得Url中键值对(data)和Head中的键值对(h：包含partner和uToken)，并把key转换成小写'''
    h = {"partner":10016}
    p = {}
    if uToken != None:  #添加 uToken到header中
        h["uToken"] = uToken
    if params != None:    #合并url和head中键值对
        p.update(h)
        p.update(params)
    else:
        p.update(h)
    for key in p:       #大小写转换
        p[str.lower(key)] = p.pop(key)

    '''把所有的键值对按 a-z 顺序排列'''
    p_sort = {}
    while p != {}:      #遍历key值，将最小值前置
        k = min(p.keys())
        p_sort[k] = p.pop(k)

    '''key重复时，排序value，并合并成一个新value'''
    for k in p_sort.keys():
        while isinstance(p_sort[k],list):
            l = p_sort[k]
            t = ''
            while l != []:
                t = t + min(l)
                l.remove(min(l))
            p_sort[k] = t


    '''2.把排序后的键值对组装成(key1 = value1 & key2 = value2)格式的字符串'''
    s = urlencode(p_sort)

    '''3.如果请求正文包含信息body，则把body 转换成字符串并拼接到步骤2中的字符串后面。得到新字符串 s'''
    if data != None:
        s = s +"&"+ json.dumps(data)
    s = s + "gaosiedu"


    '''4.把 s 进行 MD5 算法，得到签名sign'''
    sign = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()

  #  print("签名字符串为："+s)
  #  print(sign)
    return sign

