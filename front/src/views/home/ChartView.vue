<template>
  <div class="charts-container">
    <!-- 判断：如果 data 中的每项都没有图表数据，则展示列表 -->
    <template v-if="isAllEmpty">
      <ul class="empty-list">
        <li v-for="(chart, index) in data" :key="index">
          {{ chart.title }}
        </li>
      </ul>
    </template>
    <!-- 否则展示图表 -->
    <template v-else>
      <div
        v-for="(chartData, index) in data"
        :key="index"
        class="chart-wrapper"
      >
        <div ref="chartRefs" class="chart-container"></div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, defineProps } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  // data 为数组，每项格式：{ title: string, labels: Array, values: Array }
  data: {
    type: Array,
    default: () => [],
  },
});

// 计算属性：若所有项的 labels 和 values 均为空，则返回 true
const isAllEmpty = computed(() => {
  return props.data.length > 0 && props.data.every(item => {
    return (!item.labels || item.labels.length === 0) && (!item.values || item.values.length === 0);
  });
});

// 收集多个图表的 DOM 容器
const chartRefs = ref([]);
// 保存每个图表的实例，方便后续销毁和更新
const chartInstances = [];

// 渲染图表
const renderCharts = () => {
  nextTick(() => {
    chartRefs.value.forEach((container, index) => {
      if (!container) return;
      
      // 如果已存在实例，则销毁
      if (chartInstances[index]) {
        chartInstances[index].dispose();
      }
      // 初始化当前容器的 ECharts 实例
      const instance = echarts.init(container);
      const currentData = props.data[index] || { title: '', labels: [], values: [] };

      const option = {
        title: { text: currentData.title || `查询结果 ${index + 1}` },
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: currentData.labels || [] },
        yAxis: { type: 'value' },
        series: [{
          data: currentData.values || [],
          type: 'line',
          smooth: true,
        }],
      };

      instance.setOption(option);
      chartInstances[index] = instance;
    });
  });
};

onMounted(() => {
  // 仅当数据不全为空时渲染图表
  if (!isAllEmpty.value) {
    renderCharts();
  }
});

// 当响应数据变化时，根据是否全部为空判断更新逻辑
watch(
  () => props.data,
  () => {
    if (isAllEmpty.value) {
      // 如果数据全部为空，则销毁所有图表实例，确保页面只展示列表
      chartInstances.forEach(instance => {
        if (instance) instance.dispose();
      });
      chartInstances.length = 0;
    } else {
      renderCharts();
    }
  },
  { deep: true }
);
</script>

<style scoped>
.charts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-wrapper {
  width: 100%;
  height: 400px;
}

.chart-container {
  width: 100%;
  height: 100%;
}

/* 列表展示样式 */
.empty-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.empty-list li {
  padding: 8px;
  border-bottom: 1px solid #ddd;
}
</style>
