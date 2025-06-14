import { createRouter, createWebHistory } from "vue-router";

// 路由配置
const routes = [
  {
    path: "/", // 路由路径
    name: "home", // 路由名称
    component: () => import("@/views/home/home.vue"),
  },
];
// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes, // 路由配置简写形式，同 routes: routes
});
// 导出 router
export default router;