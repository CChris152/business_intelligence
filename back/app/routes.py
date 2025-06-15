import random
from datetime import datetime

from flask import Blueprint, request, jsonify
from sqlalchemy.orm import defer
from app.init import db
from app.model.query_log import QueryLog
from service import query_1, query_2, query_3, query_4, query_5, query_6, query_7, query_8

bp = Blueprint('main', __name__)

QUERY_TYPE_MAP = {
    1: "lifecycle",
    2: "category_trend",
    3: "user_interest",
    4: "multidim_stat",
    5: "viral_prediction",
    6: "recommendation",
    7: "other",
    8: "other"
}

@bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()

    # 检查是否包含 queryIndex 字段
    if not data or 'queryIndex' not in data:
        return jsonify({"error": "Missing queryIndex"}), 400

    try:
        query_index = int(data.get('queryIndex'))
    except ValueError:
        return jsonify({"error": "queryIndex must be an integer"}), 400

    query_type = QUERY_TYPE_MAP.get(query_index, "other")
    start_time = datetime.now()


    result = []
    # 根据 queryIndex 判断查询类型并处理相应业务逻辑（这里只是示例数据）
    if query_index == 1:
        # 单个新闻生命周期查询（使用 news_id，如果用户填写了的话）
        # 示例中不论用户是否填入，都返回示例数据
        news_id = data.get('newsId')
        result = query_1(news_id)

    elif query_index == 2:
        # 新闻种类统计查询（使用 news_category）
        news_category = data.get('newsCategory')
        result = query_2(news_category)

    elif query_index == 3:
        # 用户兴趣变化统计（使用 user_id）
        user_id = data.get('userId')
        result = query_3(user_id)

    elif query_index == 4:
        # 多种条件组合查询（使用 time_range、news_topic、news_length）
        news_topic = data.get('newsTopic')
        news_length = data.get('newsLength')

        time_range = data.get('timeRange', None)

        start_date_str = time_range[0]
        end_date_str = time_range[1]

        # 假设日期字符串格式为 "YYYY-MM-DD"，可以根据需要调整格式
        date_format = '%Y-%m-%d'

        start_date_str = start_date_str.replace("Z", "+00:00")
        end_date_str = end_date_str.replace("Z", "+00:00")
        try:
            # 将字符串转换为 datetime 对象
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
            result = query_4(start_date, end_date, news_topic, news_length)
        except ValueError as ve:
            return jsonify({"error": "日期格式错误，请确保使用 'YYYY-MM-DD' 格式"}), 400

    elif query_index == 5:
        # 爆款新闻分析（无需额外输入）
        result = query_5()

    elif query_index == 6:
        # 实时新闻推荐（无需额外输入）
        user_id = data.get('userId')
        result = query_6(user_id)

    elif query_index == 7:
        # 每日新闻主题变化（无需额外输入）
        result = query_7()

    elif query_index == 8:
        # 查询记录
        time_range = data.get('timeRange', None)  # 获取前端传来的时间数组

        # 验证数据是否为有效的列表，且包含两个日期
        if time_range and isinstance(time_range, list) and len(time_range) == 2:
            start_date_str = time_range[0]
            end_date_str = time_range[1]

            # 假设日期字符串格式为 "YYYY-MM-DD"，可以根据需要调整格式
            date_format = '%Y-%m-%d'

            start_date_str = start_date_str.replace("Z", "+00:00")
            end_date_str = end_date_str.replace("Z", "+00:00")
            try:
                # 将字符串转换为 datetime 对象
                start_date = datetime.fromisoformat(start_date_str)
                end_date = datetime.fromisoformat(end_date_str)
                result = query_8(start_date, end_date)
            except ValueError as ve:
                return jsonify({"error": "日期格式错误，请确保使用 'YYYY-MM-DD' 格式"}), 400

    else:
        return jsonify({"error": "Invalid queryIndex"}), 400

    end_time = datetime.now()
    execution_time_ms = int((end_time - start_time).total_seconds() * 1000)
    query_id = f"{query_type}_{int(datetime.utcnow().timestamp())}"

    sql_query = "SELECT * FROM some_table WHERE condition = TRUE;"
    query_parameters = {"param1": random.randint(1, 100), "param2": "test_value"}
    result_count = random.randint(0, 500)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    ip_address = f"192.168.1.{random.randint(1, 255)}"
    error_message = None if random.random() > 0.2 else "Some error occurred"
    query_timestamp = datetime.utcnow()
    try:
        new_log = QueryLog(
            query_id=query_id,
            query_type=query_type,
            sql_query=sql_query,
            query_parameters=query_parameters,
            execution_time_ms=execution_time_ms,
            result_count=result_count,
            user_agent=user_agent,
            ip_address=ip_address,
            error_message=error_message,
            query_timestamp=query_timestamp
        )
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    return result
