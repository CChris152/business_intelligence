<template>
  <el-form @submit.prevent="submitForm" class="query-form" label-position="top">
    <!-- 单个新闻生命周期查询 -->
    <el-form-item v-if="queryType === 'news_lifecycle'" label="新闻ID">
      <el-input 
        v-model="formData.newsId" 
        placeholder="请输入新闻ID"
        clearable
        required
      >
        <template #prefix>
          <el-icon><Document /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <!-- 新闻种类统计查询 -->
    <el-form-item v-if="queryType === 'news_category_stats'" label="新闻类别">
      <el-input 
        v-model="formData.newsCategory" 
        placeholder="请输入新闻类别"
        class="w-100"
        clearable
      >
        <template #prefix>
          <el-icon><Collection /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <!-- 用户兴趣变化统计查询 -->
    <el-form-item v-if="queryType === 'user_interest_stats'" label="用户ID">
      <el-input 
        v-model="formData.userId" 
        placeholder="请输入用户ID"
        clearable
        required
      >
        <template #prefix>
          <el-icon><User /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <!-- 多种条件组合查询 -->
    <template v-if="queryType === 'custom_filters'">
      <el-form-item label="时间范围">
        <el-date-picker
          v-model="formData.timeRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="w-100"
        >
          <template #prefix>
            <el-icon><Calendar /></el-icon>
          </template>
        </el-date-picker>
      </el-form-item>
      
      <el-form-item label="新闻类型">
        <el-input 
          v-model="formData.newsTopic" 
          placeholder="请输入新闻类型"
          clearable
        >
          <template #prefix>
            <el-icon><Collection /></el-icon>
          </template>
        </el-input>
      </el-form-item>
      
      <el-form-item label="新闻长度">
        <el-select 
          v-model="formData.newsLength" 
          placeholder="请选择新闻长度"
          class="w-100"
          clearable
        >
          <template #prefix>
            <el-icon><ScaleToOriginal /></el-icon>
          </template>
          <el-option label="短" value="短" />
          <el-option label="中" value="中" />
          <el-option label="长" value="长" />
        </el-select>
      </el-form-item>
    </template>

    <!-- 实时新闻推荐 -->
    <el-form-item v-if="queryType === 'realtime_recommendation'" label="用户ID">
      <el-input 
        v-model="formData.userId" 
        placeholder="请输入用户ID"
        clearable
        required
      >
        <template #prefix>
          <el-icon><User /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <!-- 查询记录 -->
     <template v-if="queryType === 'query_logs'">
      <el-form-item label="时间范围">
        <el-date-picker
          v-model="formData.timeRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          class="w-100"
        >
          <template #prefix>
            <el-icon><Calendar /></el-icon>
          </template>
        </el-date-picker>
      </el-form-item>
    </template>

    <!-- 查询按钮 -->
    <el-form-item>
      <el-button 
        type="primary" 
        native-type="submit"
        class="submit-button"
        :loading="loading"
      >
        <el-icon v-if="!loading"><Search /></el-icon>
        <span>{{ loading ? '查询中...' : '开始查询' }}</span>
      </el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import { 
  Document, 
  Collection, 
  User, 
  Calendar, 
  ScaleToOriginal,
  Search
} from '@element-plus/icons-vue';

const props = defineProps({ queryType: String });
const emit = defineEmits(['query-submit']);

const formData = ref({});
const loading = ref(false);

const submitForm = async () => {
  loading.value = true;
  try {
    emit('query-submit', formData.value);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.query-form {
  max-width: 100%;
}

.w-100 {
  width: 100%;
}

.submit-button {
  width: 100%;
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
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

:deep(.el-input__prefix) {
  color: #909399;
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

:deep(.el-button--primary:active) {
  transform: translateY(0);
}

:deep(.el-date-editor) {
  width: 100%;
}
</style>
