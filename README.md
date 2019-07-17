# QuestionBank

*一个基于flask和mysql的题库*

![图片](http://ww1.sinaimg.cn/large/005L13Yhgy1g53nhvdbbuj31cf0cr0uv.jpg)

## Function

1. 支持搜索(题目, 来源, 考点)
2. 分类显示(常识判断, 数量关系等)

## Run

执行下面的命令安装需要的环境:

`pip install -r requirements.txt`

然后修改`config.py`文件内的数据库相关信息.

执行:

`python app.py`

*PS:如果报错, 且与Flask-SQLAlchemy有关, 通过pip卸载重装即可.*

## Others

本程序需要配合mysql运行, 附带一个可以用于测试的数据库文件`questionbank.sql`.

mysql安装以及配合使用的细节暂且不表.
