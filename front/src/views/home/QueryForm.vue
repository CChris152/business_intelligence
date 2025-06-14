<template>
  <form @submit.prevent="submitForm" class="query-form">
    <!-- 单个新闻生命周期查询 -->
    <div v-if="queryType === 'news_lifecycle'" class="form-group">
      <label class="form-label">新闻ID：</label>
      <input class="form-input" v-model="formData.newsId" type="text" required />
    </div>

    <!-- 新闻种类统计查询 -->
    <div v-if="queryType === 'news_category_stats'" class="form-group">
      <label class="form-label">新闻类别：</label>
      <select class="form-input" v-model="formData.newsCategory">
        <option value="健康">健康</option>
        <option value="体育">体育</option>
        <option value="科技">科技</option>
        <option value="娱乐">娱乐</option>
      </select>
    </div>

    <!-- 用户兴趣变化统计查询 -->
    <div v-if="queryType === 'user_interest_stats'" class="form-group">
      <label class="form-label">用户ID：</label>
      <input class="form-input" v-model="formData.userId" type="text" required />
    </div>

    <!-- 多种条件组合查询 -->
    <div v-if="queryType === 'custom_filters'" class="form-group">
      <div class="sub-group">
        <label class="form-label">时间范围：</label>
        <input class="form-input" v-model="formData.timeRange" type="date" />
      </div>
      <div class="sub-group">
        <label class="form-label">新闻类型：</label>
        <input class="form-input" v-model="formData.newsTopic" type="text" />
      </div>
      <div class="sub-group">
        <label class="form-label">新闻长度：</label>
        <select class="form-input" v-model="formData.newsLength">
          <option disabled value="">请选择</option>
          <option value="短">短</option>
          <option value="中">中</option>
          <option value="长">长</option>
        </select>
      </div>
    </div>

    <div v-if="queryType === 'realtime_recommendation'" class="form-group">
      <label class="form-label">用户ID：</label>
      <input class="form-input" v-model="formData.userId" type="text" required />
    </div>

    <!-- 查询按钮 -->
    <div class="form-group">
      <button type="submit" class="submit-button">查询</button>
    </div>
  </form>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({ queryType: String });
const emit = defineEmits(['query-submit']);

const formData = ref({});

const submitForm = () => {
  emit('query-submit', formData.value);
};
</script>

<style scoped>
/* 整体表单容器样式 */
.query-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* 每个表单组 */
.form-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

/* 子项组 */
.sub-group {
  margin-bottom: 10px;
}

/* 标签 */
.form-label {
  font-size: 16px;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

/* 表单输入框 */
.form-input {
  padding: 8px 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

/* 查询按钮 */
.submit-button {
  background-color: #409eff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  width: 100%;
}

.submit-button:hover {
  background-color: #66b1ff;
}
</style>
