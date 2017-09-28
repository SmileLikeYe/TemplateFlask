#!/usr/bin/env python
# coding:utf-8
# @Date    : 2017-09-28 16:58:54
# @Author  : Smile Hu (www.smilehu.com)
# @Link    : http://www.smilehu.com

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0', 这会让操作系统监听所有公网 IP,服务器和局域网才能通过你本机ip访问
    app.run(host='0.0.0.0', port=port, debug=True)