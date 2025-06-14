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


def query_1(news_id: str):
    order_case = case(
        (NewsLifecycle.time_period == '1h', 1),
        (NewsLifecycle.time_period == '6h', 2),
        (NewsLifecycle.time_period == '12h', 3),
        (NewsLifecycle.time_period == '1d', 4),
        (NewsLifecycle.time_period == '3d', 5),
        (NewsLifecycle.time_period == '7d', 6),
        else_=7
    )

    query_results = (
        db.session.query(NewsLifecycle, NewsArticle)
        .join(NewsArticle, NewsLifecycle.news_id == NewsArticle.news_id)
        .filter(NewsLifecycle.news_id == news_id)
        .order_by(order_case)
        .all()
    )

    if not query_results:
        return []

    labels = []  # 时间段
    total_reads_vals = []
    total_likes_vals = []
    total_shares_vals = []
    total_comments_vals = []
    unique_readers_vals = []
    popularity_scores = []
    growth_rates = []

    for lifecycle, article in query_results:
        labels.append(lifecycle.time_period)
        total_reads_vals.append(lifecycle.total_reads)
        total_likes_vals.append(lifecycle.total_likes)
        total_shares_vals.append(lifecycle.total_shares)
        total_comments_vals.append(lifecycle.total_comments)
        unique_readers_vals.append(lifecycle.unique_readers)
        # 对于数值型数据，注意可能为 None 的处理
        popularity_scores.append(
            float(lifecycle.popularity_score) if lifecycle.popularity_score is not None else 0.0
        )
        growth_rates.append(
            float(lifecycle.growth_rate) if lifecycle.growth_rate is not None else 0.0
        )

    result = [
        {
            "title": "总阅读量",
            "labels": labels,
            "values": total_reads_vals
        },
        {
            "title": "总点赞数",
            "labels": labels,
            "values": total_likes_vals
        },
        {
            "title": "转发量",
            "labels": labels,
            "values": total_shares_vals
        },
        {
            "title": "评论数",
            "labels": labels,
            "values": total_comments_vals
        },
        {
            "title": "唯一阅读者数",
            "labels": labels,
            "values": unique_readers_vals
        },
        {
            "title": "人气分数",
            "labels": labels,
            "values": popularity_scores
        },
        {
            "title": "增长率",
            "labels": labels,
            "values": growth_rates
        }
    ]
    return result


def query_2(category: str):
    # 计算 24 小时前的截止时间
    cutoff = datetime.utcnow() - timedelta(hours=24)

    # 按 date_hour 分组，统计各项指标
    query = (
        db.session.query(
            CategoryTrend.date_hour,
            func.sum(CategoryTrend.total_articles).label("articles"),
            func.sum(CategoryTrend.total_reads).label("reads"),
            func.sum(CategoryTrend.total_interactions).label("interactions"),
            func.avg(CategoryTrend.avg_engagement).label("avg_eng")
        )
        .filter(CategoryTrend.category == category)
        .filter(CategoryTrend.date_hour >= cutoff)
        .group_by(CategoryTrend.date_hour)
        .order_by(CategoryTrend.date_hour)
    )

    rows = query.all()
    if not rows:
        return []

    # 初始化各指标对应的数组
    labels = []
    total_articles_vals = []
    total_reads_vals = []
    total_interactions_vals = []
    avg_eng_vals = []

    for row in rows:
        # 格式化日期时间提高前端展示友好性
        labels.append(row.date_hour.strftime("%Y-%m-%d %H:%M:%S"))
        total_articles_vals.append(row.articles)
        total_reads_vals.append(row.reads)
        total_interactions_vals.append(row.interactions)
        avg_eng_vals.append(float(row.avg_eng) if row.avg_eng is not None else 0.0)

    # 分别构造各指标的查询结果，并自定义 title 名称区分
    result = [
        {
            "title": "文章总数趋势",
            "labels": labels,
            "values": total_articles_vals
        },
        {
            "title": "总阅读量趋势",
            "labels": labels,
            "values": total_reads_vals
        },
        {
            "title": "总互动量趋势",
            "labels": labels,
            "values": total_interactions_vals
        },
        {
            "title": "平均互动趋势",
            "labels": labels,
            "values": avg_eng_vals
        }
    ]

    return result


def query_3(uid:str):
    # 指定需要统计的四种兴趣标签
    categories = ["健康", "体育", "科技", "娱乐"]

    # 计算起始日期：最近 7 天（含今天）
    cutoff = date.today() - timedelta(days=7)

    # 查询指定用户最近 7 天的记录，按 date_period 升序排序
    rows = (
        db.session.query(UserInterestEvolution)
        .filter(
            UserInterestEvolution.user_id == uid,
            UserInterestEvolution.date_period >= cutoff
        )
        .order_by(UserInterestEvolution.date_period)
        .all()
    )

    # 如果没有记录，直接返回空列表
    if not rows:
        return []

    # 构造连续的日期序列：从 cutoff 开始到今天
    date_list = []
    current = cutoff
    while current <= date.today():
        date_list.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    # 构造字典存储每天每个类别的计数，初始化全部为 0
    daily_counts = {d: {cat: 0 for cat in categories} for d in date_list}

    # 遍历查询结果，统计每天 interest_categories 中包含指定类别的次数
    for record in rows:
        # 将记录的 date_period 格式化为字符串（例如 "2025-06-07"）
        record_date = record.date_period.strftime("%Y-%m-%d")
        # 仅处理日期在 date_list 中的记录
        if record_date in daily_counts:
            # 假设 interest_categories 为 JSON 格式（通常映射为 Python 的 list）
            interests = record.interest_categories if record.interest_categories else []
            for cat in categories:
                if cat in interests:
                    daily_counts[record_date][cat] += 1

    # 根据日期序列构造每个类别的趋势数据
    result = []
    for cat in categories:
        values = []
        for d in date_list:
            values.append(daily_counts[d].get(cat, 0))
        result.append({
            "title": cat,
            "labels": date_list,
            "values": values
        })

    return result


def query_4(time_str: str, category: str, length: str):
    try:
        given_date = datetime.strptime(time_str, "%Y-%m-%d")
    except Exception:
        return []

        # 当天起始时间和次日起始时间
    end_date = given_date + timedelta(days=1)

    # 构造基本查询条件：发布时间在当天内，类别匹配
    query = db.session.query(NewsArticle).filter(
        NewsArticle.publish_time >= given_date,
        NewsArticle.publish_time < end_date,
        NewsArticle.category == category
    )

    # 根据 content 字符长度过滤，使用 func.length
    if length == "短":
        query = query.filter(func.char_length(NewsArticle.content) <= 200)
    elif length == "中":
        query = query.filter(func.char_length(NewsArticle.content) > 200, func.char_length(NewsArticle.content) <= 500)
    elif length == "长":
        query = query.filter(func.char_length(NewsArticle.content) > 500)

    articles = query.all()

    result = []
    for idx, article in enumerate(articles, start=1):
        content_len = len(article.content) if article.content else 0
        # 格式化发布时间，若存在
        publish_str = article.publish_time.strftime("%Y-%m-%d %H:%M:%S") if article.publish_time else ""
        # 构造标题：序号. 新闻标题 - 新闻类别 - 字符数字 - 发布时间
        title_str = f"{idx}. {article.headline} - {article.category} - {content_len}字 - {publish_str}"
        result.append({
            "title": title_str,
            "labels": [],
            "values": []
        })

    return result


def query_5():
    query = (
        db.session.query(ViralNewsPrediction, NewsArticle)
        .join(NewsArticle, ViralNewsPrediction.news_id == NewsArticle.news_id)
        .filter(ViralNewsPrediction.predicted_peak_time >= func.now())
        .order_by(desc(ViralNewsPrediction.viral_score))
        .limit(10)
    )
    results = query.all()
    if not results:
        return []

    output = []
    rank = 1
    for viral, article in results:
        # 构造 title 内容：排名. 新闻标题 - 新闻类别
        title = "{}. {} - {}".format(rank, article.headline, article.category)
        output.append({
            "title": title,
            "labels": [],
            "values": []
        })
        rank += 1
    return output


def query_6(uid:str):
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
            title_str = "{}. {} - {}".format(idx+1, article.headline, article.category)
            result.append({
                "title": title_str,
                "labels": [],
                "values": []
            })
    return result


def query_7():
    # 固定分类列表
    categories = ["健康", "体育", "科技", "娱乐"]
    # 计算过去7天的截止时间
    cutoff = datetime.utcnow() - timedelta(days=7)

    result = []
    for cat in categories:
        # 使用 func.date() 将 datetime 转换为日期，以便按天分组
        query = (
            db.session.query(
                func.date(CategoryTrend.date_hour).label("day"),
                func.sum(CategoryTrend.total_articles).label("articles"),
                func.sum(CategoryTrend.total_reads).label("reads")
            )
            .filter(CategoryTrend.category == cat)
            .filter(CategoryTrend.date_hour >= cutoff)
            .group_by(func.date(CategoryTrend.date_hour))
            .order_by(func.date(CategoryTrend.date_hour))
        )
        rows = query.all()

        labels = []
        articles_vals = []
        reads_vals = []

        for row in rows:
            # row.day 为日期类型，格式化为字符串显示（例如 "2025-06-07"）
            labels.append(row.day.strftime("%Y-%m-%d"))
            articles_vals.append(row.articles)
            reads_vals.append(row.reads)

        result.append({
            "title": f"{cat}-文章总数趋势",
            "labels": labels,
            "values": articles_vals
        })
        result.append({
            "title": f"{cat}-总阅读量趋势",
            "labels": labels,
            "values": reads_vals
        })

    return result
