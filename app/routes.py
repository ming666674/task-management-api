#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务管理 API 路由文件

包含所有任务相关的 API 端点，实现了完整的 CRUD 操作
"""

# 导入必要的模块
try:
    from flask import Blueprint, request, jsonify, Response
except ImportError:
    import sys
    print("错误: Flask 模块未安装，请先执行 pip install flask", file=sys.stderr)
    raise

# 导入数据库连接函数
from .db import get_db
from typing import Dict, Any, Optional, List, Union, Tuple

# 创建蓝图
bp: Blueprint = Blueprint('tasks', __name__)

def convert_task_to_dict(task) -> Dict[str, Any]:
    """
    将数据库查询结果转换为字典，处理布尔值
    
    Args:
        task: 数据库查询结果（sqlite3.Row对象）
    
    Returns:
        Dict[str, Any]: 转换后的任务字典
    """
    task_dict = dict(task)
    # 将is_done从整数转换为布尔值
    if 'is_done' in task_dict:
        task_dict['is_done'] = bool(task_dict['is_done'])
    return task_dict


@bp.route('/tasks', methods=['GET'])
def get_tasks() -> Union[Response, Tuple[Response, int]]:
    """
    获取任务列表
    
    Returns:
        JSON: 任务列表，按创建时间倒序排列
    """
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 执行查询，按创建时间倒序
    c.execute('SELECT * FROM tasks ORDER BY created_at DESC')
    tasks = c.fetchall()
    
    # 关闭连接
    conn.close()
    
    # 返回 JSON 格式的任务列表
    return jsonify([convert_task_to_dict(task) for task in tasks])


@bp.route('/tasks', methods=['POST'])
def create_task() -> Union[Response, Tuple[Response, int]]:
    """
    创建新任务
    
    Request Body:
        {
            "title": "任务标题",  # 必填，长度 1-100
            "description": "任务描述",  # 可选
            "due_date": "2026-03-31"  # 可选
        }
    
    Returns:
        JSON: 新创建的任务详情
        400: 验证错误
    """
    # 获取请求数据，处理JSON解析异常
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': {'code': 'INVALID_JSON', 'message': '无效的JSON格式'}}), 400
    
    # 验证标题是否存在
    if not data or 'title' not in data:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': '需要标题'}}), 400
    
    # 验证标题长度
    if len(data['title']) < 1 or len(data['title']) > 100:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': '标题长度必须在1-100之间'}}), 400
    
    # 验证is_done字段类型
    if 'is_done' in data:
        if not isinstance(data['is_done'], bool):
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'is_done必须是布尔值'}}), 400
    
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 插入新任务
    c.execute(
        'INSERT INTO tasks (title, description, due_date, is_done) VALUES (?, ?, ?, ?)',
        (data['title'], data.get('description'), data.get('due_date'), data.get('is_done', False))
    )
    
    # 获取新任务的 ID
    task_id = c.lastrowid
    
    # 查询新创建的任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    
    # 返回新任务详情
    return jsonify(convert_task_to_dict(task)), 201


@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    获取单个任务详情
    
    Args:
        task_id: 任务 ID
    
    Returns:
        JSON: 任务详情
        404: 任务不存在
    """
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 查询任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    
    # 关闭连接
    conn.close()
    
    # 检查任务是否存在
    if not task:
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': '任务不存在'}}), 404
    
    # 返回任务详情
    return jsonify(convert_task_to_dict(task))


@bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    更新任务
    
    Args:
        task_id: 任务 ID
    
    Request Body:
        {
            "title": "新标题",  # 可选
            "description": "新描述",  # 可选
            "due_date": "2026-03-31",  # 可选
            "is_done": true  # 可选
        }
    
    Returns:
        JSON: 更新后的任务详情
        400: 验证错误
        404: 任务不存在
    """
    # 获取请求数据，处理JSON解析异常
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': {'code': 'INVALID_JSON', 'message': '无效的JSON格式'}}), 400
    
    # 验证是否有更新数据
    if not data:
        return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': '需要更新数据'}}), 400
    
    # 定义允许的字段列表
    allowed_fields = {'title', 'description', 'due_date', 'is_done'}
    
    # 检查是否有未知字段
    for field in data:
        if field not in allowed_fields:
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': f'未知字段: {field}'}}), 400
    
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 查询任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    
    # 检查任务是否存在
    if not task:
        conn.close()
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': '任务不存在'}}), 404
    
    # 验证标题长度
    if 'title' in data:
        if len(data['title']) < 1 or len(data['title']) > 100:
            conn.close()
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': '标题长度必须在1-100之间'}}), 400
    
    # 验证is_done字段类型
    if 'is_done' in data:
        if not isinstance(data['is_done'], bool):
            conn.close()
            return jsonify({'error': {'code': 'VALIDATION_ERROR', 'message': 'is_done必须是布尔值'}}), 400
    
    # 构建更新语句
    update_fields = []
    update_values = []
    
    if 'title' in data:
        update_fields.append('title = ?')
        update_values.append(data['title'])
    if 'description' in data:
        update_fields.append('description = ?')
        update_values.append(data['description'])
    if 'due_date' in data:
        update_fields.append('due_date = ?')
        update_values.append(data['due_date'])
    if 'is_done' in data:
        update_fields.append('is_done = ?')
        update_values.append(data['is_done'])
    
    # 执行更新
    if update_fields:
        update_values.append(task_id)
        c.execute(
            f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?",
            update_values
        )
    
    # 查询更新后的任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated_task = c.fetchone()
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    
    # 返回更新后的任务
    return jsonify(convert_task_to_dict(updated_task))


@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Union[Response, Tuple[str, int], Tuple[Response, int]]:
    """
    删除任务
    
    Args:
        task_id: 任务 ID
    
    Returns:
        204: 删除成功
        404: 任务不存在
    """
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 查询任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    
    # 检查任务是否存在
    if not task:
        conn.close()
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': '任务不存在'}}), 404
    
    # 删除任务
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    
    # 返回 204 No Content
    return '', 204


@bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    切换任务完成状态
    
    Args:
        task_id: 任务 ID
    
    Returns:
        JSON: 更新后的任务详情
        404: 任务不存在
    """
    # 获取数据库连接
    conn = get_db()
    c = conn.cursor()
    
    # 查询任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    
    # 检查任务是否存在
    if not task:
        conn.close()
        return jsonify({'error': {'code': 'NOT_FOUND', 'message': '任务不存在'}}), 404
    
    # 切换完成状态
    new_is_done = not task['is_done']
    c.execute('UPDATE tasks SET is_done = ? WHERE id = ?', (new_is_done, task_id))
    
    # 查询更新后的任务
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated_task = c.fetchone()
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    
    # 返回更新后的任务
    return jsonify(convert_task_to_dict(updated_task))