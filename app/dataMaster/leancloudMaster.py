# coding:utf-8
# @Date    : 2017-09-28 18:07:21
# @Author  : Smile Hu (www.smilehu.com)
# @Link    : http://www.smilehu.com

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import leancloud
import random
import requests
import ast
import json
from bs4 import BeautifulSoup

# 或者使用 masterKey获得CRUD权限
# leancloud.init("", master_key="")
leancloud.use_master_key()
# 开启log
import logging
logging.basicConfig(level=logging.DEBUG)

# 可以用继承的方式定义 leancloud.Object 的子类
class Requirements(leancloud.Object):
    pass

'''
增：单个
插入单个对象
modelName: 表名
arrayData: 对象数据
'''
def insert_object(modelName, data):
    try:
        print "====================开始存储===================="
        print "表名： ", modelName
        print "数据： "
        bo = leancloud.Object.extend(modelName)()
        for k, v in data.items():
            # if isinstance(v,leancloud.Object):
            #     relation = bo.relation(k)
            #     relation.add(v)
            if isinstance(v, leancloud.Object):
                bo.set(k, v)
            elif (type(v)==type({})) or (type(v)==type([])):
                bo.set(k, v)
            else:
                bo.set(k, str(v))
        bo.save()
        print "===================结束存储===================="
        return bo.id
    except Exception as e:
        print "===================存储发生意外：", str(e)
        return False

'''
增：多个
插入多个对象
modelName: 表名
arrayData: 对象数据数组
'''
def insert_object_array(modalName,arrayData):
    print("")
    for data in arrayData:
        insert_object(modalName, data)

'''
使用用户名和密码进行注册
username
password
'''
def sign_up(username, password):
    user = leancloud.User()
    user.set_username(username)
    user.set_password(password)
    try:
        user.sign_up()
        return {"resultCode": "0", "message":"注册成功"}
    except leancloud.errors.LeanCloudError as e:
        print "LError: 注册问题", e, e.code
        if e.code == 202:
            message = "用户名已经被占用"
        else:
            message = e.error
        return {"resultCode": "1", "message":message}

'''
删
传入objectID删除对象
'''
def delete_object_by_ID(modelName, objectId):
    bo = leancloud.Object.extend(modelName)
    print bo 
    query = bo.query
    result = query.get(objectId)
    result.destroy()

'''
改
传入objectID和需要更新的字典更新对象
'''
def update_object_by_ID(modelName, objectId, dataDic):
    bo = leancloud.Object.extend(modelName)
    print bo 
    query = bo.query
    result = query.get(objectId)

    for k, v in dataDic.items():
        result.set(k,v);
    result.save()

'''
查
leancloud文档：https://leancloud.cn/docs/leanstorage_guide-python.html#比较查询
传入条件组filters，返回dic对象数组
'''
def query_object_by_filter(modelName, filters):
    bo = leancloud.Object.extend(modelName)
    query = bo.query
    for k, v in filters.items():
        query.equal_to(k, v)
    itemsList = query.find()

    resultList = [item.attributes for item in itemsList]
    return resultList
