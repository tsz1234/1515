import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        isShowLoading: false, // 全局 loading
        // 左侧菜单栏数据
        menuItems: [
            {
                name: 'home', // 要跳转的路由名称 不是路径
                size: 18, // icon大小
                type: 'ios-home', // icon类型
                text: '主页', // 文本内容
            },
            {
                name: 'summary', // 要跳转的路由名称 不是路径
                size: 18, // icon大小
                type: 'md-home', // icon类型
                text: '总览', // 文本内容
            },
            {
                size: 18, // icon大小
                type: 'md-arrow-forward', // icon类型
                text: '链家网',
                url: 'https://www.lianjia.com',
                isExternal: true, // 外链 跳到一个外部的 URL 页面
            },
            {
                type: 'ios-grid',
                name: 't1',
                text: '预测单价',
                // hidden 属性 隐藏此菜单 可以通过在地址栏上输入对应的 URL 来显示页面
                // hidden: true,
            },
            {
                text: '词云图',
                type: 'ios-paper',
                children: [
                    {
                        size: 18, // icon大小
                        type: 'md-home', // icon类型
                        text: '区域词云图',
                        name: 'c1', // 外链 跳到一个外部的 URL 页面
                    },
                    {
                        size: 18, // icon大小
                        type: 'md-home', // icon类型
                        text: '小区词云图',
                        name: 'c2', // 外链 跳到一个外部的 URL 页面
                    },
                ],
            },
        ],
    },
    mutations: {
        setMenus(state, items) {
            state.menuItems = [...items]
        },
        setLoading(state, isShowLoading) {
            state.isShowLoading = isShowLoading
        },
    },
})

export default store
