<template>
  <div class="page-container">
    <div class="card">
      <h1 class="title">新闻数据分析</h1>
      <select v-model="selectedQueryType" class="select">
        <option disabled value="">请选择查询类型</option>
        <option v-for="type in queryTypes" :key="type.value" :value="type.value">
          {{ type.label }}
        </option>
      </select>

      <!-- 根据查询类型动态显示表单 -->
      <div v-if="selectedQueryType" class="form-container">
        <query-form :key="selectedQueryType" :queryType="selectedQueryType" @query-submit="fetchData" />
      </div>

      <!-- 结果图表 -->
      <div v-if="chartData" class="chart-container">
        <chart-view :data="chartData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import QueryForm from './QueryForm.vue';
import ChartView from './ChartView.vue';

const selectedQueryType = ref('');
const chartData = ref();

const queryTypes = [
  { value: 'news_lifecycle', label: '单个新闻生命周期查询' },
  { value: 'news_category_stats', label: '新闻种类统计查询' },
  { value: 'user_interest_stats', label: '用户兴趣变化统计' },
  { value: 'custom_filters', label: '多种条件组合查询' },
  { value: 'viral_news_analysis', label: '爆款新闻分析' },
  { value: 'realtime_recommendation', label: '实时新闻推荐' },
  { value: 'daily_news_topic', label: '每日新闻主题变化' },
];

const fetchData = async (formData) => {
  // 查找当前查询类型在数组中的索引，注意 JavaScript 数组索引从 0 开始，因此加1
  const queryIndex = queryTypes.findIndex(q => q.value === selectedQueryType.value) + 1;
  
  // 合并 queryIndex 到提交数据中
  const payload = { queryIndex, ...formData };
  console.log(payload)

  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
    });
    chartData.value = await response.json();
    console.log(chartData)
  } catch (error) {
    console.error('查询失败:', error);
  }
};
</script>

<style scoped>
/* 整个页面居中显示 */
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f2f2f2;
  padding: 20px;
}

/* 卡片样式 */
.card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 600px;
  padding: 30px;
}

/* 标题样式 */
.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 28px;
  color: #333;
}

/* 下拉选择框样式 */
.select {
  display: block;
  width: 100%;
  padding: 8px 12px;
  font-size: 16px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 内容区域样式 */
.form-container,
.chart-container {
  margin-top: 20px;
}
</style>
