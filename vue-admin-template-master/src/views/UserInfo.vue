<template>
    <div>
        <h1>基本资料</h1>
        <Form>
            <FormItem label="用户名">
                <Input v-model="userName" disabled />
            </FormItem>
            <FormItem label="头像">
                <img :src="userImg" alt="头像" style="width: 100px; height: 100px;" />
                <Button @click="uploadAvatar">更换头像</Button>
            </FormItem>
            <FormItem label="其他资料">
                <Input v-model="otherInfo" />
            </FormItem>
            <FormItem>
                <Button type="primary" @click="saveInfo">保存</Button>
            </FormItem>
        </Form>
    </div>
</template>

<script>
import request from '@/utils/request';

export default {
    name: 'UserInfo',
    data() {
        return {
            userName: localStorage.getItem('userName'),
            userImg: localStorage.getItem('userImg'),
            otherInfo: ''
        };
    },
    methods: {
        async saveInfo() {
            try {
                const response = await request.post('/api/updateUserInfo', {
                    userName: this.userName,
                    otherInfo: this.otherInfo
                });
                if (response.code === 0) {
                    this.$message.success('资料保存成功');
                } else {
                    this.$message.error(response.msg);
                }
            } catch (error) {
                console.error(error);
                this.$message.error('保存失败，请稍后再试');
            }
        },
        async uploadAvatar() {
            // 这里可以实现上传头像的逻辑
            // 例如使用 FileInput 组件选择文件，然后发送请求上传
            // 上传成功后更新 userImg 和 localStorage 中的头像信息
            const fileInput = document.createElement('input');
            fileInput.type = 'file';
            fileInput.accept = 'image/*';
            fileInput.addEventListener('change', async () => {
                const file = fileInput.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append('avatar', file);
                    try {
                        const response = await request.post('/api/uploadAvatar', formData);
                        if (response.code === 0) {
                            this.userImg = response.data.avatarUrl;
                            localStorage.setItem('userImg', response.data.avatarUrl);
                            this.$message.success('头像更换成功');
                        } else {
                            this.$message.error(response.msg);
                        }
                    } catch (error) {
                        console.error(error);
                        this.$message.error('上传失败，请稍后再试');
                    }
                }
            });
            fileInput.click();
        }
    }
};
</script>