# 目的
常需一个麻雀虽小，五脏齐全的网页逐赛，抑或demo。遂理此最精简框架，拿去直接做开发，至上线。

# 环境
>python2.7
>virtualenv
详细的参见：http://www.jianshu.com/p/f654f9895555

# 运行
cd TemplateFlask/app
> source venv/bin/active  
> python main.py  
> open http://0.0.0.0:5000

# 常见问题
1. port端口5000被占用

> lsof -i:5000    
> kill -9（线程id）

# ChangeLog:
* 2017.10.03 增加leancloud的后台支持
* 2017.09.28 项目基础框架搭建完成

@Smile_安之

  