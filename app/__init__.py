# 导入Flask框架，用于创建Web应用
from flask import Flask
# 导入CORS，用于处理跨域请求
from flask_cors import CORS
# 导入路由蓝图，包含所有API端点
from .routes import bp
from typing import Optional

# 创建Flask应用实例
app: Flask = Flask(__name__)
# 启用CORS支持，允许跨域访问
CORS(app)
# 注册蓝图，所有API端点都以/api/v1开头
app.register_blueprint(bp, url_prefix='/api/v1')

# 当直接运行此文件时，启动开发服务器
if __name__ == '__main__':
    # debug=False表示关闭调试模式，生产环境应该关闭
    # host='127.0.0.1'表示只监听本地地址
    # port=8000表示使用8000端口
    app.run(debug=False, host='127.0.0.1', port=8000)