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
    justify-content: center;  /* 水平居中 */
    align-items: center;      /* 垂直居中 */
    min-height: 300px;        /* 设置最小高度防止折叠 */
    width: 50%;             /* 继承父容器宽度 */
}

/* Grid布局替代方案 */
/* .image-container {
    display: grid;
    place-items: center;
    min-height: 600px;
} */

.centered-image {
    max-width: 100%;         /* 防止图片溢出容器 */
    height: auto;            /* 保持图片比例 */
    object-fit: contain;     /* 完整显示图片内容 */
}
</style>
