# 导入Flask应用实例
from app import app
from flask import Flask

# 当直接运行此文件时，启动Flask开发服务器
if __name__ == '__main__':
    # debug=False表示关闭调试模式，生产环境应该关闭
    # host='127.0.0.1'表示只监听本地地址，不允许外部访问
    # port=8000表示使用8000端口
    app.run(debug=False, host='127.0.0.1', port=8000)