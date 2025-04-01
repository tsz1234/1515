<template>
    <div>
        <Card style="width:98%; margin:0 auto">
            <template #title>
                <Icon type="ios-film-outline"></Icon>
                小区词云图
            </template>
            <!-- 新增父级容器并添加居中样式 -->
            <div class="image-container">
                <img
                    src="../../src/assets/imgs/cba.jpg"
                    alt="词云图"
                    class="centered-image"
                >
            </div>
        </Card>
    </div>
</template>

<script>
export default {}
</script>

<style scoped>
/* Flexbox方案 */
.image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 300px;
    width: 50%;
}




.centered-image {
    max-width: 100%;
    height: auto;
    object-fit: contain;
}
</style>
