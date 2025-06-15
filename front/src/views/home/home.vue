<template>
  <el-container class="page-container">
    <el-aside width="250px" class="aside">
      <div class="logo">
        <h2>新闻数据分析</h2>
      </div>
      <el-menu
        :default-active="selectedQueryType"
        class="menu"
        @select="handleSelect"
      >
        <el-menu-item 
          v-for="type in queryTypes" 
          :key="type.value"
          :index="type.value"
        >
          <el-icon><DataLine /></el-icon>
          <span>{{ type.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header height="60px">
        <div class="header-content">
          <h1>{{ currentQueryLabel }}</h1>
        </div>
      </el-header>
      
      <el-main>
        <el-row :gutter="20" justify="center">
          <el-col :xs="24" :sm="22" :md="20" :lg="18" :xl="16">
            <el-card class="main-card" shadow="hover">
              <!-- 根据查询类型动态显示表单 -->
              <div v-if="selectedQueryType" class="form-container">
                <div class="section-title">
                  <el-icon><Search /></el-icon>
                  <span>查询条件</span>
                </div>
                <query-form 
                  :key="selectedQueryType" 
                  :queryType="selectedQueryType" 
                  @query-submit="fetchData" 
                />
              </div>

              <!-- 结果图表 -->
              <div v-if="chartData" class="chart-container">
                <div class="section-title">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>分析结果</span>
                </div>
                <el-card shadow="hover" class="result-card">
                  <chart-view :data="chartData" />
                </el-card>
              </div>

              <!-- 空状态 -->
              <el-empty 
                v-if="selectedQueryType && !chartData" 
                description="暂无数据"
                :image-size="200"
              >
                <template #description>
                  <p>请填写查询条件并点击查询按钮</p>
                </template>
              </el-empty>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { DataLine, Search, DataAnalysis } from '@element-plus/icons-vue';
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

const currentQueryLabel = computed(() => {
  const type = queryTypes.find(t => t.value === selectedQueryType.value);
  return type ? type.label : '请选择查询类型';
});

const handleSelect = (index) => {
  selectedQueryType.value = index;
  chartData.value = null; // 切换查询类型时清空结果
};

const fetchData = async (formData) => {
  const queryIndex = queryTypes.findIndex(q => q.value === selectedQueryType.value) + 1;
  const payload = { queryIndex, ...formData };
  
  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
    });
    chartData.value = await response.json();
  } catch (error) {
    console.error('查询失败:', error);
  }
};
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.aside {
  background-color: #304156;
  color: #fff;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow-y: auto;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b3649;
  padding: 0 20px;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  color: #fff;
}

.menu {
  border-right: none;
  background-color: transparent;
}

:deep(.el-menu) {
  background-color: transparent;
}

:deep(.el-menu-item) {
  color: #bfcbd9;
}

:deep(.el-menu-item.is-active) {
  color: #409EFF;
  background-color: #263445;
}

:deep(.el-menu-item:hover) {
  background-color: #263445;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 8px;
}

.el-container {
  margin-left: 250px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-content h1 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.main-card {
  margin-bottom: 20px;
  border-radius: 8px;
  border: none;
}

.section-title {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.section-title .el-icon {
  margin-right: 8px;
  font-size: 20px;
  color: #409EFF;
}

.section-title span {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.form-container {
  margin-top: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}

.chart-container {
  margin-top: 30px;
}

.result-card {
  margin-top: 20px;
  border: none;
  background-color: #fff;
}

:deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid #ebeef5;
  background-color: #f5f7fa;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input__wrapper),
:deep(.el-select) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover),
:deep(.el-select:hover) {
  box-shadow: 0 0 0 1px #409EFF inset;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-select.is-focus) {
  box-shadow: 0 0 0 1px #409EFF inset;
}

:deep(.el-button--primary) {
  background-color: #409EFF;
  border-color: #409EFF;
  padding: 12px 20px;
  font-size: 14px;
  border-radius: 4px;
  transition: all 0.3s;
}

:deep(.el-button--primary:hover) {
  background-color: #66b1ff;
  border-color: #66b1ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 12px 0 rgba(64, 158, 255, 0.1);
}

:deep(.el-empty__description) {
  margin-top: 20px;
  color: #909399;
}

:deep(.el-card__body) {
  padding: 20px;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .aside {
    width: 64px !important;
  }
  
  .el-container {
    margin-left: 64px;
  }
  
  .logo h2 {
    display: none;
  }
  
  :deep(.el-menu-item span) {
    display: none;
  }

  .el-main {
    padding: 10px;
  }

  .form-container {
    padding: 15px;
  }

  .section-title {
    margin-bottom: 15px;
  }
}
</style>
