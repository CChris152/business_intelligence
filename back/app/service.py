from datetime import datetime, timedelta, date

from sqlalchemy import case, func, desc

from app.init import db
from app.model.user import User
from app.model.user_event import UserEvent
from app.model.user_interest_evolution import UserInterestEvolution
from app.model.query_log import QueryLog
from app.model.news_article import NewsArticle
from app.model.processing_batch import ProcessingBatch
from app.model.real_time_recommendation import RealTimeRecommendation
from app.model.unified_analysis_result import UnifiedAnalysisResult
from app.model.viral_news_prediction import ViralNewsPrediction
from app.model.ai_analysis_result import AiAnalysisResult
from app.model.category_trend import CategoryTrend
from app.model.multidim_statistic import MultidimStatistic
from app.model.news_lifecycle import NewsLifecycle
from app.model.performance_metric import PerformanceMetric
from app.model.news_lifecycle2 import NewsLifecycle2


def query_1(news_id: str):
    # 先筛选出指定 news_id 的记录，并根据 total_reads 降序排列，取第一条，即为最大 total_reads 的记录
    record = (
        db.session.query(NewsLifecycle2)
        .filter(NewsLifecycle2.news_id == news_id)
        .order_by(NewsLifecycle2.total_reads.desc())
        .first()
    )
    if not record:
        return {}

    # 提取所需要的字段
    start_time = record.start_time
    end_time = record.end_time
    max_total_reads = record.total_reads if record.total_reads is not None else 0

    # 如果 start_time 和 end_time 都可用，则计算它们之间的中间时间
    if start_time and end_time:
        mid_time = start_time + (end_time - start_time) / 2
    else:
        mid_time = None

    # 构造长度为 3 的数据列表
    values = [0, max_total_reads, 0]
    labels = [start_time, mid_time, end_time]

    result = [{"title": "总阅读量", "labels": labels, "values": values}]
    print(result)
    return result


def query_2(category: str):
    # 计算过去 3 天的截止时间（基于 UTC 时间）
    cutoff = datetime.utcnow() - timedelta(days=3)

    # 统计每一天该 category 出现的记录次数（将一行视作一次）
    query = (
        db.session.query(
            func.date(CategoryTrend.date_hour).label("date_day"),
            func.count().label("occurrences")
        )
        .filter(CategoryTrend.category == category)
        .filter(CategoryTrend.date_hour >= cutoff)
        .group_by(func.date(CategoryTrend.date_hour))
        .order_by(func.date(CategoryTrend.date_hour))
    )

    rows = query.all()
    if not rows:
        return []

    # 构造连续日期序列：从 cutoff 的日期到今天（含）
    start_day = cutoff.date()
    end_day = datetime.utcnow().date()
    day_list = []
    current = start_day
    while current <= end_day:
        day_list.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # 初始化字典，以日期字符串为 key，对应值初始为 0
    daily_counts = {day: 0 for day in day_list}
    for row in rows:
        # row.date_day 可能为 date 类型，也可能为 datetime 类型
        day_str = row.date_day.strftime("%Y-%m-%d") if hasattr(row.date_day, "strftime") else str(row.date_day)
        daily_counts[day_str] = row.occurrences

    # 构造每天的记录数列表（作为 labels），并对每个值除以 1000
    counts = [daily_counts.get(day, 0) for day in day_list]

    # 按要求，将 labels 数组两边各加一个 0
    padded_counts = [0] + counts + [0]

    # 对应的 values 数组为日期序列，扩展两侧：在最前面加上第一天的前一天，在末尾加上最后一天的后一天
    first_date = datetime.strptime(day_list[0], "%Y-%m-%d").date() - timedelta(days=1)
    last_date = datetime.strptime(day_list[-1], "%Y-%m-%d").date() + timedelta(days=1)
    padded_dates = [first_date.strftime("%Y-%m-%d")] + day_list + [last_date.strftime("%Y-%m-%d")]

    result = [{
        "title": "趋势统计 (每天记录计数 / 1000)",
        "labels": padded_dates,
        "values": padded_counts
    }]

    return result


def query_3(uid: str):
    categories = ["news", "health", "sports", "lifesyle", "music", "autos", "foodanddrink", "finance", "weather"]

    # 查询指定用户所有的记录，不再限制时间
    rows = (
        db.session.query(UserInterestEvolution)
        .filter(UserInterestEvolution.user_id == uid)
        .all()
    )

    if not rows:
        return []

    # 初始化计数字典，所有兴趣的初始值均为 0
    counts = {cat: 0 for cat in categories}

    # 遍历记录，拆解 interest_categories（JSON 数组）并统计出现次数
    for record in rows:
        interests = record.interest_categories if record.interest_categories else []
        for cat in interests:
            if cat in counts:
                counts[cat] += 1

    # 计算所有类别数量之和
    total = sum(counts.values())

    # 计算每个兴趣的百分比，保留两位小数，当 total==0 时均为 0
    percentages = [
        round((counts[cat] / total * 100), 2) if total > 0 else 0 for cat in categories
    ]

    # 构造结果：labels 使用预先定义的兴趣标签，values 为各兴趣出现的百分比
    result = [{
        "title": "Interest Distribution",
        "labels": categories,
        "values": percentages
    }]

    return result


def query_4(start_date: datetime, end_date: datetime, category: str, length: str):
    # 构造基本查询条件：发布时间在给定范围内，类别匹配
    query = db.session.query(NewsArticle).filter(
        NewsArticle.created_at >= start_date,
        NewsArticle.created_at < end_date,
        NewsArticle.category == category
    )

    # 根据内容字符长度过滤记录
    if length == "短":
        query = query.filter(func.char_length(NewsArticle.news_body) <= 200)
    elif length == "中":
        query = query.filter(
            func.char_length(NewsArticle.news_body) > 200,
            func.char_length(NewsArticle.news_body) <= 500
        )
    elif length == "长":
        query = query.filter(func.char_length(NewsArticle.news_body) > 500)

    query = query.limit(100)

    articles = query.all()

    result = []
    for idx, article in enumerate(articles, start=1):
        content_len = len(article.news_body) if article.news_body else 0
        publish_str = article.created_at.strftime("%Y-%m-%d %H:%M:%S") if article.created_at else ""
        # 构造标题：序号. 新闻标题 - 新闻类别 - 字符数字 - 发布时间
        title_str = f"{idx}. {article.headline} - {article.category} - {content_len}字 - {publish_str}"
        result.append({
            "title": title_str,
            "labels": [],
            "values": []
        })

    return result


def query_5():
    # 计算截止时间：当前时间减去 3 天
    cutoff = datetime.now() - timedelta(days=3)

    # 第一步：只查询 ViralNewsPrediction 表中 created_at 在 3 天内的记录，
    # 按 viral_score 降序排序，取前 10 条（只需要 id、news_id、viral_score）
    predictions = (
        db.session.query(ViralNewsPrediction)
        .filter(ViralNewsPrediction.created_at >= cutoff)
        .order_by(desc(ViralNewsPrediction.viral_score))
        .limit(5)
        .all()
    )

    if not predictions:
        return []

    output = []
    rank = 1
    for pred in predictions:
        # 第二步：通过 news_id 在 NewsArticle 中查询相应记录
        article = (
            db.session.query(NewsArticle)
            .filter(NewsArticle.news_id.collate("utf8mb4_unicode_ci") == pred.news_id)
            .first()
        )
        if article:
            # 如果找到了文章，则构造："排名. 新闻标题 - 新闻类别"
            title = "{}. {} - {}".format(rank, article.headline, article.category)
        else:
            # 如果文章未找到，则构造："排名. id"
            title = "{}. {}".format(rank, pred.id)

        output.append({
            "title": title,
            "labels": [],
            "values": []
        })
        rank += 1

    return output


def query_6(uid: str):
    # 查询用户最新的一次推荐记录（最新推荐）
    rec = (
        db.session.query(RealTimeRecommendation)
        .filter(RealTimeRecommendation.user_id == uid)
        .order_by(RealTimeRecommendation.generated_at.desc())
        .first()
    )

    if not rec or not rec.recommended_news:
        return []

    # 假设 recommended_news 字段为 JSON，对应 Python 对象中的 list
    recommended_ids = rec.recommended_news  # 例如: ["news1", "news2", ..., "news10"]
    if not recommended_ids:
        return []

    # 批量查询 news_articles，获取核心信息 headline 和 category
    # 为保证按照推荐顺序输出，这里先生成一个新闻ID到新闻详情的字典
    articles = (
        db.session.query(NewsArticle)
        .filter(NewsArticle.news_id.in_(recommended_ids))
        .all()
    )
    article_map = {article.news_id: article for article in articles}

    result = []
    for idx, news_id in enumerate(recommended_ids):
        # 按照推荐顺序，如果新闻ID对应的新闻详情存在，则构造结果
        article = article_map.get(news_id)
        if article:
            # 构造 title 格式： "序号. 新闻标题 - 新闻类型"
            title_str = "{}. {} - {}".format(idx + 1, article.headline, article.category)
            result.append({
                "title": title_str,
                "labels": [],
                "values": []
            })
    return result


def query_7():
    categories = ["news", "health", "sports", "lifesyle", "music", "autos", "foodanddrink", "finance", "weather"]
    # 计算过去 3 天的截止时间（基于 UTC 时间）
    cutoff = datetime.utcnow() - timedelta(days=3)

    results = []

    for category in categories:
        # 统计每一天该 category 出现的记录次数（将一行视作一次）
        query = (
            db.session.query(
                func.date(CategoryTrend.date_hour).label("date_day"),
                func.count().label("occurrences")
            )
            .filter(CategoryTrend.category == category)
            .filter(CategoryTrend.date_hour >= cutoff)
            .group_by(func.date(CategoryTrend.date_hour))
            .order_by(func.date(CategoryTrend.date_hour))
        )

        rows = query.all()

        # 构造连续日期序列：从 cutoff 的日期到今天（含）
        start_day = cutoff.date()
        end_day = datetime.utcnow().date()
        day_list = []
        current = start_day
        while current <= end_day:
            day_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)

        # 初始化字典，以日期字符串为 key，对应值初始为 0
        daily_counts = {day: 0 for day in day_list}
        for row in rows:
            # row.date_day 可能为 date 类型，也可能为 datetime 类型
            day_str = row.date_day.strftime("%Y-%m-%d") if hasattr(row.date_day, "strftime") else str(row.date_day)
            daily_counts[day_str] = row.occurrences

        # 构造每天的记录数列表（作为 labels）
        counts = [daily_counts.get(day, 0) for day in day_list]

        # 按要求，将 labels 数组两边各加一个 0
        padded_counts = [0] + counts + [0]

        # 对应的 values 数组为日期序列，扩展两侧：在最前面加上第一天的前一天，在末尾加上最后一天的后一天
        first_date = datetime.strptime(day_list[0], "%Y-%m-%d").date() - timedelta(days=1)
        last_date = datetime.strptime(day_list[-1], "%Y-%m-%d").date() + timedelta(days=1)
        padded_dates = [first_date.strftime("%Y-%m-%d")] + day_list + [last_date.strftime("%Y-%m-%d")]

        results.append({
            "title": f"{category} 趋势统计 (每天记录计数)",
            "labels": padded_dates,
            "values": padded_counts
        })

    return results


def query_8(start_date: datetime, end_date: datetime):
    # 根据 query_timestamp 限定查询范围，并查询所有满足条件的记录
    logs = QueryLog.query.filter(
        QueryLog.query_timestamp >= start_date,
        QueryLog.query_timestamp <= end_date
    ).all()

    # 对每一条记录分别构造一个字典并加入结果数组
    result = []
    for log in logs:
        qtype = log.query_type if log.query_type is not None else ""
        sql_query = log.sql_query if log.sql_query is not None else ""
        exec_time = str(log.execution_time_ms) if log.execution_time_ms is not None else "0"
        title_str = f"{qtype} | {sql_query} | {exec_time}ms"

        result.append({
            "title": title_str,
            "labels": [],
            "values": []
        })

    return result
