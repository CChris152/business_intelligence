<template>
  <div class="charts-container">
    <!-- 如果 data 中的每项（labels 和 values）均为空，则展示标题列表 -->
    <template v-if="isAllEmpty">
      <div class="titles-list">
        <div v-for="(chartData, index) in data" :key="index" class="title-row">
          {{ chartData.title }}
        </div>
      </div>
    </template>

    <!-- 否则展示图表 -->
    <template v-else>
      <el-row :gutter="20">
        <el-col 
          v-for="(chartData, index) in data" 
          :key="index"
          :xs="24" 
          :sm="24" 
          :md="12" 
          :lg="12" 
          :xl="12"
        >
          <div class="chart-wrapper">
            <div ref="chartRefs" class="chart-container"></div>
          </div>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
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
    // 延时 100ms，确保 DOM 容器的尺寸被正确计算
    setTimeout(() => {
      chartRefs.value.forEach((container, index) => {
        if (!container) return;
        
        // 如果已存在图表实例，则先销毁
        if (chartInstances[index]) {
          chartInstances[index].dispose();
        }

        // 初始化当前容器的 ECharts 实例
        const instance = echarts.init(container);
        const currentData = props.data[index] || { title: '', labels: [], values: [] };

        const option = {
          title: { 
            text: currentData.title || `查询结果 ${index + 1}`,
            left: 'center',
            top: 10,
            textStyle: {
              fontSize: 16,
              fontWeight: 'normal'
            }
          },
          tooltip: { 
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: { 
            left: '3%', 
            right: '4%', 
            bottom: '3%', 
            containLabel: true,
            top: 60
          },
          xAxis: { 
            type: 'category', 
            data: currentData.labels || [],
            axisLabel: {
              interval: 0,
              rotate: 30
            }
          },
          yAxis: { 
            type: 'value',
            name: currentData.yAxisName || '',
            nameTextStyle: {
              padding: [0, 0, 0, 40]
            }
          },
          series: [{
            data: currentData.values || [],
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#409EFF'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(64,158,255,0.3)'
                },
                {
                  offset: 1,
                  color: 'rgba(64,158,255,0.1)'
                }
              ])
            }
          }]
        };

        instance.setOption(option);
        chartInstances[index] = instance;

        // 响应式调整：窗口大小变化时重新调整图表尺寸
        window.addEventListener('resize', () => {
          instance.resize();
        });
      });
    }, 100);
  });
};

onMounted(() => {
  // 仅当数据项中有图表数据时渲染图表
  if (!isAllEmpty.value) {
    renderCharts();
  }
});

// 当数据变化时按条件重新处理
watch(
  () => props.data,
  () => {
    if (isAllEmpty.value) {
      // 数据全部为空时，销毁所有图表实例，确保页面只展示标题列表
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
.chart-container {
  width: 100%;
  height: 350px; /* 为避免容器高度为 0，明确设置图表容器的高度 */
}

.titles-list {
  padding: 20px;
  border: 1px dashed #dcdfe6;
}

.title-row {
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.title-row:last-child {
  border-bottom: none;
}
</style>
