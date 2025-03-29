import request from '@/utils/request'

import axios from 'axios'

const service=axios.create({
    baseURl: 'http://127.0.0.1:8000/',
    TIMEOUT: 40000,
})
export default service
