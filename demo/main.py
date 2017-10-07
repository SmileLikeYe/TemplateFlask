#!/usr/bin/env python
# coding:utf-8
# @Date    : 2017-09-28 16:58:54
# @Author  : Smile Hu (www.smilehu.com)
# @Link    : http://www.smilehu.com

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import json
from flask import Flask, render_template
app = Flask(__name__)

'''
WebsiteURL: 作为网站的接口-首页
'''
@app.route('/')
def index():
    return render_template("index.html", data={"k":"v"})


'''
------------------------------------------------------------------
|下面是写网站常用的功能区，作为参考，你可以删除
'''

'''
1. 提交表单的处理
'''
@app.route('/handle_form', methods = ['GET', 'POST'])
def handle_form():
    print "收到提交表单: ", request.form
    # 通过表单里面的 name 标签获取用户输入的参数
    organization_name = request.form['organization_name']
    # 这里返回了首页
    return url_for("/")

'''
2.1 echarts数据展示页面
'''
@app.route('/echartsdemo')
def echartsdemo():
    return render_template("echartsdemo.html")

'''
2.2 echarts数据数据请求接口
'''
@app.route('/backend/api/echartsdata', methods = ['GET', 'POST'])
def api_test1():
	data = [
                {"value": 30, "name": '访问'},
                {"value": 10, "name": '咨询'},
                {"value": 5, "name": '订单'},
                {"value": 50, "name": '点击'},
                {"value": 80, "name": '展现'}
            ]
	return json.dumps(data).decode('unicode-escape')

'''
|常用功能区结束
------------------------------------------------------------------
'''



'''
------------------------------------------------------------------
Main Entry: 主入口
'''
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0', 这会让操作系统监听所有公网 IP,服务器和局域网才能通过你本机ip访问
    app.run(host='0.0.0.0', port=port, debug=True)