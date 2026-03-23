# 导入sqlite3模块，用于操作SQLite数据库
import sqlite3
# 导入os模块，用于处理文件路径
import os
from typing import Optional, Dict, Any

# 定义数据库文件的绝对路径
# __file__表示当前文件的路径，os.path.dirname获取所在目录
# os.path.join用于拼接路径，确保跨平台兼容
DB_PATH: str = os.path.join(os.path.dirname(__file__), 'tasks.db')

def get_db() -> sqlite3.Connection:
    """
    获取数据库连接
    
    Returns:
        sqlite3.Connection: 数据库连接对象，配置了行工厂
    """
    # 连接到SQLite数据库，如果文件不存在会自动创建
    conn: sqlite3.Connection = sqlite3.connect(DB_PATH)
    # 设置row_factory，使查询结果可以通过列名访问（如task['title']）
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """
    初始化数据库，创建tasks表
    
    如果表已存在则不会重复创建
    """
    # 获取数据库连接
    conn: sqlite3.Connection = get_db()
    # 创建游标对象，用于执行SQL语句
    c: sqlite3.Cursor = conn.cursor()
    # 执行建表SQL语句
    c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增主键
        title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 100),  -- 标题，必填，长度1-100
        description TEXT,  -- 描述，可选
        due_date TEXT,  -- 截止日期，可选
        is_done BOOLEAN DEFAULT FALSE,  -- 是否完成，默认为False
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间，默认为当前时间
    )
    ''')
    # 提交事务，使更改生效
    conn.commit()
    # 关闭数据库连接
    conn.close()

# 模块加载时自动初始化数据库
init_db()