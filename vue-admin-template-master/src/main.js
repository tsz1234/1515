import Vue from 'vue'
import axios from 'axios'
import ViewUI from 'view-design'
import dataV from '@jiaminghi/data-view'
import * as echarts from 'echarts'
import $http from '@/api/index.js'
import App from './App'
import store from './store'
import router from './router'
import 'view-design/dist/styles/iview.css'
import './permission'

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
