<template>
    <div>
        <Card style="width:98%; margin:0 auto">
        <template #title>
            <Icon type="ios-film-outline"></Icon>
            条件选择
        </template>
            <Form>
                <Row>
                    <Col span="1" style="text-align:center">-</Col>
                    <Col span="3">
                        <FormItem>
                            区域
                            <Select name="area" v-model="realData.lockarea">
                                <Option value="不限">不限</Option>
                                <Option v-for="area in realData.housesarea" v-bind:key="area" :value="area">{{area}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="1" style="text-align:center">-</Col>
                    <Col span="3">
                        <FormItem>
                            装修
                            <Select name="maker" v-model="realData.lockmaker">
                                <Option value="不限">不限</Option>
                                <Option v-for="maker in realData.housesmaker" v-bind:key="maker" :value="maker">{{maker}}</Option>
                            </Select>
                        </FormItem>
                    </Col>
                    <Col span="1" style="text-align:center">-</Col>
                    <Col span="2">
                        <FormItem>
                            <br>
                                <Button type="primary" style="display:block" v-on:click="query">提交</Button>
                            </br>
                        </FormItem>
                    </Col>
                </Row>
                </Form>
        </Card>
        <Card style="width:98%; margin:5px auto">
            <template #title>
            <Icon type="ios-home" ></Icon>
            数据
        </template>
            <List border style="height:300px;overflow:auto ">
<ListItem>
    <Row style="width:100%;text-align:center">
        <Col span="2">二手房导入序号</Col>
        <Col span="5">标题</Col>
        <Col span="2">总价(万元)</Col>
        <Col span="3">区域</Col>
        <Col span="3">小区</Col>
        <Col span="2">面积</Col>
        <Col span="2">楼层</Col>
        <Col span="2">年份</Col>
        <Col span="2">装修</Col>
    </Row>
</ListItem>
                <ListItem v-for="houses in realData.housesData" v-bind:key="houses.id">
    <Row style="width:100%;text-align:center">
        <Col span="2">{{houses.id}}</Col>
        <Col span="5">{{houses.title}}</Col>
        <Col span="2">{{houses.totalprice}}</Col>
        <Col span="3">{{houses.area}}</Col>
        <Col span="3">{{houses.community}}</Col>
        <Col span="2">{{houses.Acreage}}</Col>
        <Col span="2">{{houses.high}}</Col>
        <Col span="2">{{houses.age}}</Col>
        <Col span="2">{{houses.maker}}</Col>
        </Row>
                </ListItem>
</List>
        </Card>
    </div>
</template>

<script>
export default {
    data() {
        return{
            realData:{
                housesmaker:'',
                housesarea:"",
                lockarea:'',
                lockmaker:'',
                housesData:''
            }
        };
    },
    methods:{
        async query(){
            var area=this.realData.lockarea
            var maker=this.realData.lockmaker
            console.log(maker,area);
            var res=await this.$http.get('http://localhost:8000/myApp/summary/',{params:{area:area,maker:maker}});
            this.$set(this.realData,"housesData",res.data.housesData);
            console.log(this.realData.housesData);
        }
    },
    async mounted(){
        const res = await this.$http.get('http://localhost:8000/myApp/summary/')
        this.$set(this.realData, 'housesmaker',res.data.housesmaker)
        this.$set(this.realData, 'housesarea',res.data.housesarea)
    },
}
</script>

<style scoped>

</style>
