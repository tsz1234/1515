import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const commonRoutes = [
    {
        path: '/login',
        name: 'login',
        meta: { title: '登录' },
        component: () => import('../components/Login.vue'),
    },
    {
        path: '/other', // 点击侧边栏跳到一个单独的路由页面，需要定义，层级和其他顶级路由一样
        name: 'other',
        meta: { title: '单独的路由' },
        component: () => import('../views/Other.vue'),
    },
    {
        path: '/404',
        name: '404',
        meta: { title: '404' },
        component: () => import('../components/404.vue'),
    },
    { path: '/', redirect: '/home' },
]

// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
    home: {
        path: 'home',
        name: 'home',
        meta: { title: '主页' },
        component: () => import('../views/Home.vue'),
    },
    summary:{
        path: 'summary',
        name: 'summary',
        meta: { title: '总览' },
        component: () => import('../views/summary.vue'),
    },
    t1: {
        path: 't1',
        name: 't1',
        meta: { title: '查询' },
        component: () => import('../views/T1.vue'),
    },
    msg: {
        path: 'msg',
        name: 'msg',
        meta: { title: '词云图2' },
        component: () => import('../views/Msg.vue'),
    },
    c1:{
        path: 'c1',
        name: 'c1',
        meta: { title: '区域词云图' },
        component: () => import('../views/c1.vue'),
    },
    c2:{
        path: 'c2',
        name: 'c2',
        meta: { title: '小区词云图' },
        component: () => import('../views/c2.vue'),
    },
}

const createRouter = () => new Router({
    routes: commonRoutes,
})

const router = createRouter()

export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher
}

export default router
