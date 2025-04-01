<template>
    <div>
        <Card style="width:98%; margin:0 auto; overflow: visible; position: relative; z-index: 1;">
            <template #title>
                <Icon type="ios-film-outline"></Icon>
                条件选择
            </template>
            <Form>
                <Row>
                    <Col span="3">
                        <FormItem style="z-index: 100">
                            面积（㎡）
                            <InputNumber
                                v-model="inputArea"
                                placeholder="请输入面积"
                                :min="0"
                                style="width: 100%"/>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem style="z-index: 100">
                            区域
                            <Select v-model="selectedRegion" placeholder="请选择区域" style="z-index: 100">
                                <Option v-for="area in housesregion"
                                        :key="area"
                                        :value="area">{{area}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem style="z-index: 100">
                            装修
                            <Select v-model="selectedDecoration" placeholder="请选择装修" style="z-index: 100">
                                <Option v-for="decoration in housesdecoration"
                                        :key="decoration"
                                        :value="decoration">{{decoration}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem style="z-index: 100">
                            楼层
                            <Select v-model="selectedFloor" placeholder="请选择楼层" style="z-index: 100">
                                <Option v-for="floor in housesfloor"
                                        :key="floor"
                                        :value="floor">{{floor}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem style="z-index: 100">
                            年份
                            <Select v-model="selectedYear" placeholder="请选择年份" style="z-index: 100">
                                <Option v-for="year in housesyear"
                                        :key="year"
                                        :value="year">{{year}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem>
                            <Button type="primary" @click="handlePredict">预测</Button>
                        </FormItem>
                    </Col>
                </Row>
            </Form>
        </Card>
        <Card style="width:98%; margin:0 auto; overflow: visible; position: relative; z-index: 0;"> <!-- 降低预测结果卡片的 z-index -->
            <template #title>
                <Icon type="ios-calculator-outline"></Icon>
                预测结果
            </template>
            <p v-if="predictedPrice">预测价格: {{ predictedPrice }}元/平方米</p>
            <p v-else>请输入完整信息并点击预测按钮以获取预测价格。</p>
        </Card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            inputArea: null,
            selectedRegion: null,
            selectedDecoration: null,
            selectedFloor: null,
            selectedYear: null,
            housesregion: [],
            housesdecoration: [],
            housesfloor: [],
            housesyear: [],
            predictedPrice: null
        };
    },
    async mounted() {
        try {
            const response = await axios.get('http://localhost:8000/myApp/get_options/');
            this.housesregion = response.data.housesregion;
            this.housesdecoration = response.data.housesdecoration;
            this.housesfloor = response.data.housesfloor;
            this.housesyear = response.data.housesyear;
        } catch (error) {
            console.error('获取选项数据失败:', error);
            this.$Message.error('获取选项数据失败，请稍后重试');
        }

        // 监听下拉框显示事件
        document.addEventListener('click', (event) => {
            const dropdown = document.querySelector('.ivu-select-dropdown');
            if (dropdown) {
                // 获取下拉框的位置和尺寸
                const rect = dropdown.getBoundingClientRect();
                const windowHeight = window.innerHeight;

                // 如果下拉框超出窗口底部，调整其位置
                if (rect.bottom > windowHeight) {
                    dropdown.style.top = `${windowHeight - rect.height}px`;
                }
            }
        });
    },
    methods: {
        async handlePredict() {
            if (!this.selectedRegion || this.inputArea === null || !this.selectedDecoration || !this.selectedFloor || !this.selectedYear) {
                this.$Message.error('请完整填写所有字段');
                return;
            }

            // 验证区域和装修是否在训练数据中
            if (!this.housesregion.includes(this.selectedRegion) || !this.housesdecoration.includes(this.selectedDecoration) || !this.housesfloor.includes(this.selectedFloor) || !this.housesyear.includes(this.selectedYear)) {
                this.$Message.error('输入的区域、装修、楼层或年份不在有效范围内，请重新选择');
                return;
            }

            try {
                const response = await axios.post('http://localhost:8000/myApp/predict_price/', {
                    area: this.selectedRegion,
                    inputArea: this.inputArea,
                    decoration: this.selectedDecoration,
                    floor: this.selectedFloor,
                    year: this.selectedYear
                });
                this.predictedPrice = response.data.price;
            } catch (error) {
                const msg = error.response?.data?.error || `网络错误: ${error.message}`;
                this.$Message.error(`预测失败: ${msg}`);
            }
        }
    }
};
</script>

<style scoped>
/* 确保下拉框不被遮挡 */
.ivu-select-dropdown {
    z-index: 99999 !important;
    position: fixed !important;
    top: auto !important;
    left: auto !important;
    right: auto !important;
    bottom: auto !important;
    transform: none !important;
    overflow: visible !important;
}


.ivu-card {
    position: relative;
    z-index: 1;
    overflow: visible !important;
}


body {
    overflow-x: visible !important;
    overflow-y: visible !important;
}

.ivu-select-dropdown-list {
    max-height: 300px !important;
    overflow-y: auto !important;
}
</style>