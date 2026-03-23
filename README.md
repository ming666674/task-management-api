# Task API 项目

## 项目结构

```
task/
  app/
    __init__.py      # Flask 应用初始化
    routes.py        # API 路由定义
    db.py            # 数据库连接和初始化
  scripts/
    start.sh         # 启动服务脚本
    stop.sh          # 停止服务脚本
    restart.sh       # 重启服务脚本
  nginx/
    tinytask.conf    # Nginx 配置文件
  requirements.txt   # 项目依赖
  run.py             # 应用入口
  README.md          # 项目说明
```

## 技术栈

- Python 3.x
- Flask
- SQLite3
- Nginx

## 功能特性

- RESTful API 设计
- 完整的 CRUD 操作
- 统一的错误处理
- 支持 HTTPS
- 后台运行

## 本地开发

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 启动服务

```bash
python run.py
```

服务将在 `http://127.0.0.1:8000` 上运行。

## 服务器部署

### 1. 上传代码

将项目代码上传到服务器。

```bash
# 在本地执行，将代码上传到服务器
scp -r task ubuntu@95.40.92.231:~
```

### 2. 安装依赖

```bash
# 在服务器上执行
cd ~/task
pip install -r requirements.txt
```

### 3. 启动服务

使用提供的脚本启动服务：

```bash
# 在服务器上执行
chmod +x scripts/*.sh
./scripts/start.sh
```

服务将在后台运行，断开 SSH 后仍会继续运行。

### 4. Nginx 配置

1. 复制 Nginx 配置文件到 Nginx 配置目录：

```bash
# 在服务器上执行
sudo cp nginx/tinytask.conf /etc/nginx/sites-available/
```

2. 创建符号链接：

```bash
# 在服务器上执行
sudo ln -s /etc/nginx/sites-available/tinytask.conf /etc/nginx/sites-enabled/
```

3. 修改配置文件中的域名和证书路径：

```bash
# 编辑配置文件
sudo nano /etc/nginx/sites-available/tinytask.conf

# 修改以下内容：
server_name examination.dianchuang.club;
ssl_certificate /etc/ssl/certs/bundle.crt;
ssl_certificate_key /etc/ssl/private/cert.key;
```

4. 测试 Nginx 配置：

```bash
# 在服务器上执行
sudo nginx -t
```

5. 重启 Nginx：

```bash
# 在服务器上执行
sudo systemctl restart nginx
```

### 5. HTTPS 配置

- 证书文件应放置在安全的目录中，建议使用 `/etc/ssl/certs/` 和 `/etc/ssl/private/`
- 私钥文件权限应设置为 600，仅 root 可读：
  ```bash
  # 在服务器上执行
  sudo chmod 600 /path/to/your/private.key
  ```
- 确保证书链完整，避免浏览器证书错误

### 6. 验证服务

服务启动后，可以通过以下方式验证：

- **域名访问**：`https://examination.dianchuang.club/api/v1/tasks`
- **IP 地址访问**：`https://95.40.92.231/api/v1/tasks`
- 使用 Apifox 进行 API 测试
- 检查服务运行状态：
  ```bash
  # 在服务器上执行（Linux）
  ps aux | grep python
  
  # 在本地执行（PowerShell）
  Get-Process | Where-Object {$_.ProcessName -like "*python*"}
  ```

## 线上入口

- **域名入口**：`https://examination.dianchuang.club/api/v1/tasks`
- **IP 地址入口**：`https://95.40.92.231/api/v1/tasks`

## API 文档

### 文档概览

本文档详细描述了 Task API 的所有接口，包括请求参数、响应结构、状态码和错误处理。

### 基础信息

- **API 基础路径**: `/api/v1`
- **请求格式**: JSON
- **响应格式**: JSON
- **认证方式**: 无（当前版本）

### 错误处理

所有错误响应符合统一结构，并使用正确的 HTTP 状态码：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "需要标题"
  }
}
```

### API 接口详情

#### 1. 获取任务列表

- **方法**: `GET`
- **路径**: `/api/v1/tasks`
- **描述**: 获取所有任务列表，按创建时间倒序排列
- **请求参数**: 无
- **响应体**: 
  ```json
  [
    {
      "id": 1,
      "title": "完成项目文档",
      "description": "编写项目的详细文档",
      "due_date": "2026-03-31",
      "is_done": false,
      "created_at": "2026-03-18 10:00:00"
    }
  ]
  ```
- **状态码**: 
  - `200 OK`: 成功

#### 2. 创建任务

- **方法**: `POST`
- **路径**: `/api/v1/tasks`
- **描述**: 创建新任务
- **请求体**: 
  ```json
  {
    "title": "任务标题",  // 必填，长度 1-100
    "description": "任务描述",  // 可选
    "due_date": "2026-03-31"  // 可选
  }
  ```
- **响应体**: 
  ```json
  {
    "id": 1,
    "title": "任务标题",
    "description": "任务描述",
    "due_date": "2026-03-31",
    "is_done": false,
    "created_at": "2026-03-18 10:00:00"
  }
  ```
- **状态码**: 
  - `201 Created`: 创建成功
  - `400 Bad Request`: 验证错误

#### 3. 获取单个任务

- **方法**: `GET`
- **路径**: `/api/v1/tasks/{task_id}`
- **描述**: 获取指定任务的详细信息
- **路径参数**: 
  - `task_id`: 任务 ID（整数）
- **响应体**: 
  ```json
  {
    "id": 1,
    "title": "任务标题",
    "description": "任务描述",
    "due_date": "2026-03-31",
    "is_done": false,
    "created_at": "2026-03-18 10:00:00"
  }
  ```
- **状态码**: 
  - `200 OK`: 成功
  - `404 Not Found`: 任务不存在

#### 4. 更新任务

- **方法**: `PATCH`
- **路径**: `/api/v1/tasks/{task_id}`
- **描述**: 更新任务信息（支持局部更新）
- **路径参数**: 
  - `task_id`: 任务 ID（整数）
- **请求体**: 
  ```json
  {
    "title": "新标题",  // 可选
    "description": "新描述",  // 可选
    "due_date": "2026-04-01",  // 可选
    "is_done": true  // 可选
  }
  ```
- **响应体**: 
  ```json
  {
    "id": 1,
    "title": "新标题",
    "description": "新描述",
    "due_date": "2026-04-01",
    "is_done": true,
    "created_at": "2026-03-18 10:00:00"
  }
  ```
- **状态码**: 
  - `200 OK`: 更新成功
  - `400 Bad Request`: 验证错误
  - `404 Not Found`: 任务不存在

#### 5. 删除任务

- **方法**: `DELETE`
- **路径**: `/api/v1/tasks/{task_id}`
- **描述**: 删除指定任务
- **路径参数**: 
  - `task_id`: 任务 ID（整数）
- **响应体**: 无
- **状态码**: 
  - `204 No Content`: 删除成功
  - `404 Not Found`: 任务不存在

#### 6. 切换任务状态

- **方法**: `POST`
- **路径**: `/api/v1/tasks/{task_id}/toggle`
- **描述**: 切换任务的完成状态
- **路径参数**: 
  - `task_id`: 任务 ID（整数）
- **响应体**: 
  ```json
  {
    "id": 1,
    "title": "任务标题",
    "description": "任务描述",
    "due_date": "2026-03-31",
    "is_done": true,  // 状态已切换
    "created_at": "2026-03-18 10:00:00"
  }
  ```
- **状态码**: 
  - `200 OK`: 切换成功
  - `404 Not Found`: 任务不存在

### 数据模型

#### 任务 (Task)

| 字段名 | 类型 | 说明 | 约束 |
|-------|------|------|------|
| id | INTEGER | 任务 ID | 自增主键 |
| title | TEXT | 任务标题 | 必填，长度 1-100 |
| description | TEXT | 任务描述 | 可选 |
| due_date | TEXT | 截止日期 | 可选，格式：YYYY-MM-DD |
| is_done | BOOLEAN | 是否完成 | 默认为 false |
| created_at | TIMESTAMP | 创建时间 | 默认为当前时间 |

### Apifox 文档

API 文档已在 Apifox 平台维护，包含所有接口的详细说明和测试用例。

#### 文档内容
- 所有 API 接口的详细说明
- 请求参数和响应字段定义
- 成功和错误示例
- 测试场景和测试套件

#### 可用性测试
- 在 Apifox 中创建测试场景，覆盖所有 API 接口
- 在「线上 HTTPS 域名环境」执行测试
- 验证完整的 CRUD 操作链路
- 测试边界情况和错误处理

## 数据库

- 使用 SQLite3 作为数据库
- 数据持久化存储在 `app/tasks.db` 文件中
- 首次启动时自动创建表结构
- 服务重启后数据不丢失

## 注意事项

- 线上环境已关闭 debug 模式
- 服务默认在 `127.0.0.1:8000` 上运行，通过 Nginx 反向代理对外提供服务
- 数据库使用 SQLite3，数据会持久化存储
- 断开 SSH 后服务会继续运行（后台运行）
- 私钥文件权限已设置为 600，确保安全性

## 常用命令

### 服务管理

```bash
# 启动服务（Linux）
./scripts/start.sh

# 停止服务（Linux）
./scripts/stop.sh

# 重启服务（Linux）
./scripts/restart.sh

# 查看服务日志（Linux）
tail -f app.log

# 查看服务状态（Linux）
ps aux | grep python

# 查看服务状态（PowerShell）
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
```

### Nginx 管理

```bash
# 测试 Nginx 配置（Linux）
sudo nginx -t

# 重启 Nginx（Linux）
sudo systemctl restart nginx

# 查看 Nginx 状态（Linux）
sudo systemctl status nginx
```

## 部署检查清单

- [ ] 代码已上传到服务器
- [ ] 依赖已安装
- [ ] 服务已启动（后台运行）
- [ ] Nginx 配置已完成
- [ ] HTTPS 证书已配置
- [ ] 服务可通过域名访问
- [ ] 服务可通过 IP 地址访问
- [ ] API 测试已通过
- [ ] Apifox 文档已创建
- [ ] 可用性测试已完成