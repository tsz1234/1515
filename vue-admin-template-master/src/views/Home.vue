<template>
    <div class="layout">
        <div class="header">
            <dv-decoration-8 style="width:300px;height:50px;" />
            <div>
                <span class="title-text">链家二手房可视化平台</span>
                <dv-decoration-5 style="width:300px;height:40px;" />"
            </div>
            <dv-decoration-8 :reverse="true" style="width:300px;height:50px;" />
    </div>
    <div class="content">
        <div class="left">
            <dv-border-box-13> <div ref="firstMain" style="width:350px;height:420px"></div></dv-border-box-13>
            <dv-border-box-8><div ref="secondMain" style="width:350px;height:420px" v-bind:key="realData.pieList[0][1]"></div></dv-border-box-8>
        </div>
        <div class="center">
        <div ref="thirdMain"style="width:1500px;height:1500px;"></div>
        </div>
        <div class="right">
            <dv-border-box-12><dv-decoration-3 style="width:300px;height:40px" /><div ref="fourthMain" style="width:320px;height:480px"></div></dv-border-box-12>
            <dv-border-box-1><h1 style="font-size:18px;text-align:center;color:C0C0C0;margin-top:10px">各户型二手房销售量占比</h1><div><dv-active-ring-chart :config="config" style="width:200px;height:400px;margin:50px auto" v-bind:key="config.data[0][0]" /></div></dv-border-box-1>
        </div>
    </div>
    </div>
</template>

<script>


import { color } from 'echarts'
import res from 'core-js/internals/is-forced'
import getMap from '@/api/getMap.js'
import changshaGeoJSON from '@/assets/changsha.json'

export default {
    data() {
        return {
            realData: {
                arealist: [1],
                followlist: [1],
                pieList: [{ name: 'data1', value: 10 }],
                mapData: [{ name: 'data2', value: 1000 }],
                LineRowData: [],
                LineColData: [1],
            },
            config: {
                data: [],
                lineWidth: 20,
                radius: '90%',
                activeRadius: '95%',
                acriveTimeGap: 2000,
                fontSize: 90,
            },
        }
    },
    methods: {
        drawLeftTop() {
            const myChart = this.$echarts.init(this.$refs.firstMain)
            const option = {
                xAxis: {
                    type: 'category',
                    data: this.realData.arealist,
                    axisLabel: {
                        textStyle: {
                            color: '#C0C0C0',
                        },
                    },
                },
                title: {
                    text: '各类装修二手房关注量',
                    textStyle: {
                        color: '#C0C0C0',
                    },
                },
                toolbox: {
                    show: true,
                    feature: {
                        // dataView: { show: true, readonly: true },
                        magicType: { show: true, type: ['line', 'bar'] },
                        restore: { show: true },
                        saveAsImage: { show: true },
                    },
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    data: ['关注量'],
                    textStyle: {
                        color: 'grey',
                    },
                    top: '8%',
                    left: '70%',
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '',

                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        textStyle: {
                            color: '#C0C0C0',
                        },
                    },
                },
                series: [
                    {
                        name: '关注量',
                        data: this.realData.followlist,
                        type: 'bar',
                        label: {
                            show: true,
                            textStyle: {
                                color: '#C0C0C0',
                            },
                        },
                    },
                ],
            }
            // eslint-disable-next-line no-unused-expressions
            option && myChart.setOption(option)
        },
        drawLeftBottom() {
            const myChart = this.$echarts.init(this.$refs.secondMain)
            const option = {
                title: {
                    text: '房屋结构',
                    left: 'center',
                    color: '#C0C0C0',
                },
                tooltip: {
                    trigger: 'item',
                },
                legend: {
                    orient: 'vertical',
                    left: 'left',
                    textStyle: {
                        color: '#C0C0C0',
                    },
                },
                series: [
                    {
                        name: '结构',
                        type: 'pie',
                        radius: '50%',
                        data: this.realData.pieList,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
                            },
                        },
                    },
                ],
            }
            option && myChart.setOption(option)
        },
        async drawCenterMap() {
            let myChart = this.$echarts.init(this.$refs.thirdMain)
            try {
                const res = await getMap()
                // 添加加载状态处理
                this.loading = false
            } catch (error) {
                if (error.response?.status === 500) {
                    this.$notify.error('服务器内部错误，请稍后重试')
                }
                // 使用可选链操作符和默认值
                console.error('API 请求失败:', error?.config?.url || '未知URL') // ✅
                console.error('错误详情:', error.message) // ✅
            }
            this.$echarts.registerMap('changsha', changshaGeoJSON)
            let data = this.realData.mapData
            let geoCoordMap = {
                芙蓉区: [112.988094, 28.193106],
                天心区: [112.97307, 28.192375],
                岳麓区: [112.911591, 28.213044],
                开福区: [112.985525, 28.201336],
                雨花区: [113.016337, 28.109937],
                望城区: [112.819549, 28.347458],
                长沙县: [113.080098, 28.237888],
            }
            let convertData = function (data) {
                let res = []
                for (let i = 0; i < data.length; i++) {
                    let geoCoord = geoCoordMap[data[i].name]
                    if (geoCoord) {
                        res.push({
                            name: data[i].name,
                            value: geoCoord.concat(data[i].value),
                        })
                    }
                }
                console.log(res)
                return res
            }
            let option = {
                scale: 0.1,
                backgroundColor: 'transparent',
                title: {
                    text: '长沙市各区小区销售数据',
                    subtext: '数据来自链家',
                    left: 'center',
                    color: '#fff',
                    fontSize: '80px',

                },
                geo: {
                    show: true,
                    map: 'changsha',
                    zoom: 1.25,
                    label: {
                        normal: {
                            show: true,
                            color: 'white',
                            fontSize: '8', // 修正拼写
                        },
                        emphasis: {
                            show: true,
                            color: 'white',
                            fontSize: '10px',
                        },
                    },
                    roam: true,
                    itemStyle: {
                        normal: {
                            areaColor: 'skyblue',
                            borderColor: '#fff', // 修正为borderColor
                        },
                        emphasis: {
                            areaColor: '#2B91B7',
                        },
                    },
                },
                series: [{
                    name: '二手房数据',
                    type: 'effectScatter',
                    coordinateSystem: 'geo',
                    data: convertData(data),
                    symbolSize(val) {
                        return val[2] / 10
                    },
                    showEffectOn: 'render',
                    rippleEffect: {
                        brushType: 'stroke',
                    },
                    hoverAnimation: true,
                    label: {
                        formatter: '{b}',
                        position: 'right', // 修正拼写
                        show: true,
                    },
                    itemStyle: {
                        color: '#ddb926',
                    },
                    emphasis: {
                        label: {
                            show: true,
                        },
                    },
                }],
            }
            myChart.setOption(option) // 添加此行以应用配置
        },
        drawRightTop() {
            let myChart = this.$echarts.init(this.$refs.fourthMain)
            let option = {
                xAxis: {
                    type: 'category',
                    data: this.realData.LineRowData || [],
                    name: '万元',
                    nameLocation: 'center',
                    nameGap: 30,
                    nameTextStyle: {
                        color: '#C0C0C0',
                        fontSize: 14,
                    },
                    axisLabel: {
                        interval: 0,
                        textStyle: {
                            color: '#C0C0C0',
                            fontSize: 12,
                        },
                        rotate: 45,
                    },
                },
                grid: {
                    bottom: 100,
                },
                yAxis: {
                    type: 'value',
                    name: '个',
                    axisLabel: {
                        textStyle: {
                            color: '#C0C0C0',
                        },
                    },
                },
                title: {
                    text: '二手房价格占比',
                    left: 'center',
                    textStyle: {
                        color: '#C0C0C0',
                    },
                },
                tooltip: {
                    trigger: 'axis',
                },
                legend: {
                    data: ['占比情况'],
                    textStyle: {
                        color: '#C0C0C0',
                    },
                    top: '8%',
                    right: '10%',
                },
                series: [{
                    name: '占比情况',
                    data: this.realData.LineColData,
                    type: 'line',
                    smooth: true,
                }],
            }
            option && myChart.setOption(option)
            window.addEventListener('resize', () => myChart.resize())
        },
    },
    async mounted() { // 移至methods外部
        const res = await this.$http.get('http://localhost:8000/myApp/screenData/')
        this.$set(this.realData, 'arealist', res.data.arealist)
        this.$set(this.realData, 'followlist', res.data.followlist)
        this.$set(this.realData, 'pieList', res.data.pieList)
        this.$set(this.realData, 'mapData', res.data.mapData)
        this.$set(this.realData, 'LineRowData', res.data.LineRowData)
        this.$set(this.realData, 'LineColData', res.data.LineColData)
        this.$set(this.config, 'data', res.data.circlieList)
        this.drawCenterMap()
        this.drawLeftBottom()
        this.drawRightTop()
    },
    async updated() { // 移至methods外部
        this.drawLeftTop()
        this.drawCenterMap()
        this.drawLeftBottom()
        this.drawLeftTop()
        this.drawRightTop()
    },
}
</script>

<style scoped>
.layout{
    height:100vh;
    width:100%;
    background:url('../assets/imgs/adc.jpg')
}
.header{
    display:flex;
    allign-content:center;
    justify-content: center;
}
.header div {
    width: 50%;
    text-align: center;
    align-items: center;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.header div span{
    color:orange;
    font-weight: bold;
    font-size:23px;
    padding:10px;
}
.content {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 0 20px;
    box-sizing: border-box;
}
.content .left {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height:80%;
    width:350px;
}
.content .left div{
    flex-grow:1;
    height:300px;
    width:380px;
    padding:5px;
margin-left:30px;
}
.content .right{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height:80%;
    width:350px;
}
.content .right div{
    flex-grow:1;
    height:300px;
    width:350px;
    padding:5px;

}
.content .center{
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    height:80%;
    width:600px;
}

</style>
