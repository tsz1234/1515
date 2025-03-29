<template>
    <div>
        <Card style="width:98%; margin:0 auto">
            <template #title>
                <Icon type="ios-film-outline"></Icon>
                条件选择
            </template>
            <Form>
                <Row>
                    <Col span="3">
                        <FormItem>
                            面积（㎡）
                            <InputNumber
                                v-model="inputArea"
                                placeholder="请输入面积"
                                :min="0"
                                style="width: 100%"/>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem>
                            区域
                            <Select v-model="selectedRegion" placeholder="请选择区域">
                                <Option v-for="area in housesregion"
                                        :key="area"
                                        :value="area">{{area}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <FormItem>
                            装修
                            <Select v-model="selectedDecoration" placeholder="请选择装修">
                                <Option v-for="decoration in housesdecoration"
                                        :key="decoration"
                                        :value="decoration">{{decoration}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="3">
                        <Button type="primary" @click="handlePredict">预测单价</Button>
                    </Col>
                </Row>
            </Form>
            <div v-if="predictedPrice !== null">
                <h3>预测单价: {{ predictedPrice }} 元/平</h3>
            </div>
        </Card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            inputArea: null,
            selectedRegion: null,
            selectedDecoration: null,
            housesregion: [], // 从后端获取的区域列表
            housesdecoration: [], // 从后端获取的装修列表
            predictedPrice: null,
        }
    },
    created() {
        this.fetchOptions()
    },
    methods: {
        fetchOptions() {
            this.$http.get('http://localhost:8000/myApp/get_options/')
            .then(response => {
                // 使用 response.data 访问（适配axios）
                this.housesregion = response.data.housesregion || []
                this.housesdecoration = response.data.housesdecoration || []
            })
            .catch(error => {
                console.error('详细错误:', error.response)
            })
        },
        handlePredict() {
  if (!this.selectedRegion || this.inputArea === null || !this.selectedDecoration) {
    this.$Message.error('请完整填写所有字段');
    return;
  }

            this.$http.post('http://localhost:8000/myApp/predict_price/',
    {
      region: this.selectedRegion,
      area: parseFloat(this.inputArea), // 明确转换为浮点数
      decoration: this.selectedDecoration
    },
    {
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    }
  ).then(response => {
    if (response.data.error) {
      this.$Message.error(response.data.error);
    } else {
      this.predictedPrice = response.data.predicted_price.toFixed(2);
    }
  }).catch(error => {
    const msg = error.response?.data?.error || `网络错误: ${error.message}`;
    this.$Message.error(`预测失败: ${msg}`);
  });
}
    },
}
</script>
