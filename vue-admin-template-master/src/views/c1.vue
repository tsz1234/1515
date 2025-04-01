<template>
    <div>
        <Card style="width:98%; margin:0 auto">
            <template #title>
                <Icon type="ios-film-outline"></Icon>
                区域词云图
            </template>
            <div class="image-container">
                <img
                    src="../../src/assets/imgs/gas.jpg"
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

/* Grid布局替代方案 */
/* .image-container {
    display: grid;
    place-items: center;
    min-height: 600px;
} */

.centered-image {
    max-width: 100%;
    height: auto;
    object-fit: contain;
}
</style>
