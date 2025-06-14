from flask import Blueprint, request, jsonify
from sqlalchemy.orm import defer
from app.init import db
from service import query_1, query_2, query_3, query_4, query_5, query_6, query_7

bp = Blueprint('main', __name__)


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

    # 根据 queryIndex 判断查询类型并处理相应业务逻辑（这里只是示例数据）
    if query_index == 1:
        # 单个新闻生命周期查询（使用 news_id，如果用户填写了的话）
        # 示例中不论用户是否填入，都返回示例数据
        news_id = data.get('newsId')
        return query_1(news_id)

    elif query_index == 2:
        # 新闻种类统计查询（使用 news_category）
        news_category = data.get('newsCategory')
        return query_2(news_category)

    elif query_index == 3:
        # 用户兴趣变化统计（使用 user_id）
        user_id = data.get('userId')
        return query_3(user_id)

    elif query_index == 4:
        # 多种条件组合查询（使用 time_range、news_topic、news_length）
        time_range = data.get('timeRange')
        news_topic = data.get('newsTopic')
        news_length = data.get('newsLength')
        return query_4(time_range, news_topic, news_length)

    elif query_index == 5:
        # 爆款新闻分析（无需额外输入）
        return query_5()

    elif query_index == 6:
        # 实时新闻推荐（无需额外输入）
        user_id = data.get('userId')
        return query_6(user_id)

    elif query_index == 7:
        # 每日新闻主题变化（无需额外输入）
        return query_7()
    else:
        return jsonify({"error": "Invalid queryIndex"}), 400

    # 返回的数据格式为数组，每个元素对应展示一个图表的数据
    return jsonify(result), 200
