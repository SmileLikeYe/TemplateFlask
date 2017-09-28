# 目的
经常需要找一个麻雀虽小，五脏齐全的网页应用进行比赛，或者demo。遂理此最精简的框架，拿去直接做开发，直到上线。

# 环境
参见：http://www.jianshu.com/p/f654f9895555

# 运行
cd 当前目录
> source venv/bin/active
> python main.py
> open http://0.0.0.0:5000

# 常见问题
1. port端口5000被占用

> lsof -i:5000
> kill -9（线程id）


@Smile_安之

