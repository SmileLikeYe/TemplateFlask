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
leancloud.init("cNO7BhP6IY0UIU3fq4m1WYCj-gzGzoHsz", master_key="DEV18zlBrfNAKJFEn4aBKNEL")
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
    for data in arrayData:
        insert_object(modalName, data)

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

# for i in range(200):
#     insert_object("Pe", {"testk":"testv"+str(i)})
# update_object_by_ID("Pe","59d33a491b69e6004085ef11", {"testk":"v2"})
# delete_object_by_ID("Pe","59d33a491b69e6004085ef11")
# query_object_by_filter("Pe", {"testk": "testv3"})


def insert_Or_Update_UserInfo(userInfoDic):
    try:
        query = UserInfo.query
        query.equal_to("OpenID", userInfoDic['OpenID'])
        userInfos = query.find()
        print "-----------"
        print "len(userInfos): ", len(userInfos)
        if len(userInfos) == 0:
            insert_object("UserInfo", userInfoDic)
        else:
            userInfo = userInfos[len(userInfos) - 1]
            print "-----------", userInfo.attributes
            userInfo.set('AccessToken', userInfoDic['AccessToken'])
            userInfo.set('RefreshToken', userInfoDic['RefreshToken'])
            userInfo.set('ExpiresIn', str(userInfoDic['ExpiresIn']))
            PhoneNumber = userInfo.get('PhoneNumber')
            print "-----------"
            print "PhoneNumber: ", PhoneNumber
            if len(PhoneNumber)==11 and ('.' not in PhoneNumber):
                print "是手机用户,暂时不改PhoneNumber"
            else:
                userInfo.set('PhoneNumber', str(userInfoDic['OpenID']))
                PhoneNumber = str(userInfoDic['OpenID'])
            userInfo.save()

        return PhoneNumber
    except Exception as e:
        print "--------error:", e
        return -1

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
    












    
def get_Requirements_By_Joint_People(joint_people):
    print "joint_people: ", joint_people
    query = Requirements.query
    query.equal_to("joint_people", joint_people)
    try:
        userInfo = query.find()
        # print userInfo
        return userInfo
    except Exception as e:
        print "get_Requirements_By_Joint_People: ",e
        return "-1"  




def get_AccessToken_By_PhoneNumber(phoneNumber):
    userInfo = get_UserInfo_by_PhoneNumber(phoneNumber)
    if userInfo == "-2":
        return "-2"
    else:
        AccessToken = userInfo.get('AccessToken')
        print "getAccessToken: ", AccessToken
        return AccessToken

def get_UserInfo_By_AccessToken(accessToken):
    print "get_UserInfo_By_AccessToken: ", accessToken
    query = UserInfo.query
    query.equal_to("AccessToken", accessToken)
    try:
        userInfo = query.find()[0]
        return userInfo
    except:
        return {}

def get_OpenID_By_PhoneNumber(phoneNumber):
    userInfo = get_UserInfo_by_PhoneNumber(phoneNumber)
    if userInfo == "-2":
        return {"resultCode": "-2", "result": "用户未授权"}
    else:
        OpenID = userInfo.get('OpenID')
        print "OpenID: ", OpenID
        return OpenID

def login_with_phoneNumber(phoneNumber, password):
    user = leancloud.User()
    try:
        user.login_with_mobile_phone(phoneNumber, password)
        return {"resultCode": "0", "message": "登录成功！", "phoneNumber":phoneNumber}
    except Exception as e:
        print 'Exception: ', e
        message = str(e).split(']')[1]
        return {"resultCode": "1", "message": message}

def login_with_username(username, password):
    user = leancloud.User()
    try:
        user.login(username, password)
        access = get_AccessToken_By_PhoneNumber(username)
        if access == "-2":
            return {"resultCode": "0", "message": "登录成功！", "phoneNumber": username, "authStatus": "false"}
        else:
            return {"resultCode": "0", "message": "登录成功！", "phoneNumber": username, "authStatus": "true"}
    except leancloud.errors.LeanCloudError as e:
        print 'Exception: ', e
        print "Signup Error:", e, e.code
        if e.code == 211:
            message = "用户不存在"
        elif e.code == 202:
            message = "密码不能为空"
        elif e.code == 210:
            message = "密码和用户名不匹配"
        else:
            message = e.error
        return {"resultCode": "1", "message": message}

def get_UserInfo_by_PhoneNumber(PhoneNumber):
    print "get_UserInfo_by_PhoneNumber: ",PhoneNumber
    query = UserInfo.query
    query.equal_to("PhoneNumber", PhoneNumber)
    try:
        userInfo = query.find()[0]
        print userInfo
        return userInfo
    except Exception as e:
        print e
        return "-2"

def save_filter(filter_data):
    userInfo = get_UserInfo_by_PhoneNumber(filter_data['PhoneNumber'])
    if userInfo == "-2":
        return {"resultCode": "-2", "message": "用户未授权"}
    else:
        filter_data["UserInfo"] = userInfo
        try:
            insert_object("Filter", filter_data)
            return {"resultCode": "0", "message": "插入成功！"}
        except Exception as e:
            print 'Exception: ', e
            return {"resultCode": "1", "message": str(e)}

def get_Filters_By_PhoneNumber(PhoneNumber):
    try:
        query = Filter.query
        query.equal_to("PhoneNumber", PhoneNumber)
        queryResultList = query.find()
        resultList = []
        for filter_bo in queryResultList:
            temp_bo = {}
            temp_bo['PerIntentedFund']  = filter_bo.get("PerIntentedFund")
            temp_bo['Duration'] = filter_bo.get("Duration")
            temp_bo['Risk'] = filter_bo.get("Risk")
            temp_bo['TotalInIendedFund'] = filter_bo.get("TotalInIendedFund")
            temp_bo['FilterName'] = filter_bo.get("FilterName")
            temp_bo['FilterId'] = filter_bo.get("objectId")
            print temp_bo
            resultList.append(temp_bo)

        return {"resultCode": "0", "result": resultList}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "result": str(e)}

def update_user_info(userInfo):
    dataDict =  userInfo.attributes
    print dataDict
    print userInfo.get('objectId')
    new_userInfo = UserInfo.create_without_data(userInfo.get('objectId'))
    # 这里修改 location 的值
    for k,v in dataDict.items():
        print k
        if k != "updatedAt" and k != "createdAt": 
            new_userInfo.set(k, v)
    return new_userInfo.save()

def get_Hot_Filters():
    try:
        query = Filter.query
        query.greater_than_or_equal_to("UseCount", 0)
        queryResultList = query.find()
        if (len(queryResultList) >10):
            queryResultList = random.sample(queryResultList, 10)

        resultList = []
        for filter_bo in queryResultList:
            print filter_bo.attributes

            temp_bo = {}
            temp_bo['PerIntentedFund'] = filter_bo.get("PerIntentedFund")
            temp_bo['Duration'] = filter_bo.get("Duration")
            temp_bo['Risk'] = filter_bo.get("Risk")
            temp_bo['TotalInIendedFund'] = filter_bo.get("TotalInIendedFund")
            temp_bo['FilterName'] = filter_bo.get("FilterName")
            temp_bo['FilterId'] = filter_bo.get("objectId")
            temp_bo['UseCount'] = filter_bo.get("UseCount")
            resultList.append(temp_bo)

        return {"resultCode": "0", "result": resultList}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "result": str(e)}

def get_Customer_Strategy_By_PhoneNumber(PhoneNumber):
    try:
        query = CustomerStrategy.query
        query.equal_to("PhoneNumber", PhoneNumber)
        queryResultList = query.find()

        print "-------拿回用户自定义的策略：", len(queryResultList)
        resultList = []
        for filter_bo in queryResultList:
            dataDict = filter_bo.attributes;
            dataDict['updatedAt'] = str(dataDict['updatedAt'])
            dataDict['createdAt'] = str(dataDict['createdAt'])
            resultList.append(dataDict)

        return {"resultCode": "0", "result": resultList}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "result": str(e)}

def switch_Customer_Strategy(objectId, switch, phone):
    try:
        query = CustomerStrategy.query
        cs = query.get(objectId)
        cs.set("isAuto", switch)
        cs.set("Phone", phone)
        cs.save()
        return {"resultCode": "0", "message": "操作成功"}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "message": "操作失败" + str(e)}


def getSysStraField(PhoneNumber, sysStraId):
    try:
        userInfo = get_UserInfo_by_PhoneNumber(PhoneNumber)
        sysStraName = "sysStra" + str(sysStraId)
        print "1111: " ,userInfo.get(sysStraName)
        return userInfo.get(sysStraName)
    except Exception as e:
        pass
    finally:
        pass

def getStrategyMarket(PhoneNumber):
    try:
        query = Strategy.query
        queryResultList = query.find()
        if (len(queryResultList) >30):
            queryResultList = random.sample(queryResultList, 30)

        resultList = []
        for filter_bo in queryResultList:
            dataDict = filter_bo.attributes;
            dataDict['updatedAt'] = str(dataDict['updatedAt'])
            dataDict['createdAt'] = str(dataDict['createdAt'])
            sysStraField = getSysStraField(PhoneNumber, dataDict['sysStraId'])
            print "sysStraField: ",sysStraField
            if sysStraField == None:
                dataDict['isAuto'] = 0
                dataDict['autoParams'] = {"perInvestAmount": "0",
                                        "totalInvestAmount": "0",
                                        "alreadyInvestAmount": "0"
                                        }
            else:
                dataDict['isAuto'] = 1
                dataDict['autoParams'] = sysStraField

            resultList.append(dataDict)

        return {"resultCode": "0", "result": resultList}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "result": str(e)}

def get_First_Filter_By_PhoneNumber(PhoneNumber):
    try:
        query = Filter.query
        query.equal_to("PhoneNumber", PhoneNumber)
        queryResultList = query.find()
        if (len(queryResultList) ==0):
            return {"resultCode": "1", "result": "您目前还未新建过策略"}
        else:
            filter_bo = queryResultList[0]
            temp_bo = {}
            temp_bo['PerIntentedFund'] = filter_bo.get("PerIntentedFund")
            temp_bo['Duration'] = filter_bo.get("Duration")
            temp_bo['Risk'] = filter_bo.get("Risk")
            temp_bo['TotalInIendedFund'] = filter_bo.get("TotalInIendedFund")
            temp_bo['FilterName'] = filter_bo.get("FilterName")
            temp_bo['FilterId'] = filter_bo.get("objectId")
            temp_bo['UseCount'] = filter_bo.get("UseCount")
            return {"resultCode": "0", "result": temp_bo}
    except Exception as e:
        print 'Exception: ', e
        return {"resultCode": "1", "result": str(e)}

def get_Filters_By_ID(FilterId):
    try:
        query = Filter.query
        print "get_Filters_By_ID: ",FilterId
        filter_bo = query.get(FilterId)

        temp_bo = {}
        temp_bo['PerIntentedFund'] = filter_bo.get("PerIntentedFund")
        temp_bo['Duration'] = filter_bo.get("Duration")
        temp_bo['Risk'] = filter_bo.get("Risk")
        temp_bo['TotalInIendedFund'] = filter_bo.get("TotalInIendedFund")
        temp_bo['FilterName'] = filter_bo.get("FilterName")
        temp_bo['FilterId'] = filter_bo.get("objectId")
        temp_bo['UseCount'] = filter_bo.get("UseCount")
        print temp_bo

        return temp_bo
    except Exception as e:
        print 'Exception: ', e
        return {}

def getOtherWebData():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'}
    url = "http://m.wdzj.com/shuju/interfaceWapIndustry"
    result = requests.get(url, headers=headers)
    resultList = []
    if result.status_code == 200:
        clean_result = ast.literal_eval(result.text)
        print json.dumps(clean_result).decode("unicode-escape")
        dateList =  clean_result['data']['date']
        volumeList = clean_result['data']['volume']
        interestRateList = clean_result['data']['interestRate']
        for i in xrange(0, len(dateList)):
            obj = {}
            obj['date'] = dateList[i]
            obj['volume'] = volumeList[i]
            obj['interestRate'] = interestRateList[i]
            resultList.append(obj)
        print "resultList: ", resultList
    return json.dumps(resultList).decode("unicode-escape")


def getResultFromUrl(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Connection': 'keep-alive'}
	result = requests.get(url, headers=headers)
	if result.status_code == 200:
		clean_result = ast.literal_eval(result.text)
		print "clean_result:", json.dumps(clean_result).decode("unicode-escape")
		return clean_result
	else:
		return {}

def getPostResult(url, postData):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/44.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Connection': 'keep-alive'}
	result = requests.post(url, postData, headers=headers)
	print "result.text:", ast.literal_eval(result.text)
	return ast.literal_eval(result.text)

def sophia9to14CommonFunction(postData):
	resultList = []
	url = "http://shuju.wdzj.com/plat-info-target.html"
	result = getPostResult(url, postData)
	if type(result['data1']) == type({}):
		result = result['data1']
	keys = result.keys()

	length = len(result[keys[0]])
	if length >10:
		length = 10
	for i in xrange(0, length):
		obj = {}
		for j in xrange(0, len(keys)):
			key = keys[j]
			obj[key] = result[key][i]
		resultList.append(obj)
	return json.dumps(resultList).decode("unicode-escape")

def genarateDataVSerialData(dataList):
    resultList = []
    print dataList
    for data in dataList:
        print "data: ", data
        keys = data.keys()
        s = 1
        for key in keys:
            if key != 'x':
                obj = {}
                obj['x'] = data['x']
                obj['y'] = data[key]
                obj['s'] = s
                resultList.append(obj)
                s = s + 1

    return json.dumps(resultList).decode("unicode-escape")

def test():
    getStrategyMarket()
    return ;

