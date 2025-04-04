<template>
    <div>
        <h1>修改密码</h1>
        <Form>
            <FormItem label="旧密码">
                <Input type="password" v-model="oldPassword" />
            </FormItem>
            <FormItem label="新密码">
                <Input type="password" v-model="newPassword" />
            </FormItem>
            <FormItem label="确认新密码">
                <Input type="password" v-model="confirmPassword" />
            </FormItem>
            <FormItem>
                <Button type="primary" @click="changePassword">保存</Button>
            </FormItem>
        </Form>
    </div>
</template>

<script>
import request from '@/utils/request';

export default {
    name: 'Password',
    data() {
        return {
            oldPassword: '',
            newPassword: '',
            confirmPassword: ''
        };
    },
    methods: {
        async changePassword() {
            // 检查两次输入的新密码是否一致
            if (this.newPassword !== this.confirmPassword) {
                this.$message.error('两次输入的新密码不一致');
                return;
            }

            // 检查旧密码和新密码是否为空
            if (!this.oldPassword || !this.newPassword) {
                this.$message.error('旧密码和新密码不能为空');
                return;
            }

            try {
                // 发送修改密码的请求
                const response = await request.post('http://localhost:8000/myApp/changePassword/', {
                    oldPassword: this.oldPassword,
                    newPassword: this.newPassword
                });

                // 检查 response.data 是否存在
                if (response && response.data) {
                    if (response.data.code === 0) {
                        this.$message.success('密码修改成功');
                    } else {
                        this.$message.error(response.data.msg || '未知错误，请稍后再试');
                    }
                } else {
                    this.$message.error('响应数据为空，请稍后再试');
                }
            } catch (error) {
                let errorMessage;
                if (error && error.response && error.response.data) {
                    // 服务器返回了响应，但状态码可能表示错误
                    errorMessage = error.response.data.msg || `请求失败，状态码: ${error.response.status}`;
                } else if (error && error.message) {
                    // 没有服务器响应，可能是网络问题
                    errorMessage = `网络错误: ${error.message}`;
                } else {
                    // 其他未知错误
                    errorMessage = '发生未知错误，请稍后再试';
                }
                // 显示错误信息
                this.$message.error(`修改失败: ${errorMessage}`);
            }
        }
    }
};
</script>