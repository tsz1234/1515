import axios from 'axios'
import { Message } from 'view-design'
import router from '@/router'
import { showLoading, closeLoading } from '@/utils/loading'
import { resetTokenAndClearUser } from '@/utils'

const service = axios.create({
    baseURL: window.location.origin,
    timeout: 60000,
})

service.interceptors.request.use(config => {
    showLoading()
    if (localStorage.getItem('token')) {
        config.headers.Authorization = localStorage.getItem('token')
    }

    return config
}, (error) => Promise.reject(error))

service.interceptors.response.use(response => {
    closeLoading()
    const res = response.data

    if (res.code != 0 && res.msg) {
        Message.error({
            content: res.msg,
        })

        if (res.code == 2) {
            resetTokenAndClearUser()
            router.push('login')
        }

        return Promise.reject()
    }

    // 如果接口正常，直接返回数据
    return res
}, (error) => {
    closeLoading()
    if (error.name == 'Error') {
        Message.error({
            content: error.msg,
        })
    } else {
        Message.error({
            content: error.response.data.data || error.message,
        })
    }

    return Promise.reject(error)
})

export default service
