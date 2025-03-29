import axios from 'axios'
export default function() {
  return axios.get('https://geo.datav.aliyun.com/areas_v3/bound/430100_full.json')
}
