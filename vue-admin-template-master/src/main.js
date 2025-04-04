import Vue from 'vue'
import axios from 'axios'
import dataV from '@jiaminghi/data-view'
import * as echarts from 'echarts'
import $http from '@/api/index.js'
import store from './store'
import router from './router'
import App from './App.vue';
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
import './permission';

// 使用 ViewUI
Vue.prototype.$echarts=echarts
Vue.prototype.$http=$http
Vue.use(dataV)
Vue.config.productionTip = false
Vue.use(ViewUI)
Vue.prototype.$echarts = echarts

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
})
