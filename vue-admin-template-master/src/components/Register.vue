<template>
    <div class="register-vue">
        <div class="container">
            <p class="title">注册账号</p>
            <div class="input-c">
                <Input prefix="ios-contact" v-model="account" placeholder="用户名" clearable />
            </div>
            <div class="input-c">
                <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable />
            </div>
            <Button class="submit" type="primary" @click="submit">注册</Button>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request';

export default {
    name: 'register',
    data() {
        return {
            account: '',
            pwd: ''
        };
    },
    methods: {
        async submit() {
            try {
                const response = await request.post('/api/register', {
                    username: this.account,
                    password: this.pwd
                });
                if (response.code === 0) {
                    this.$message.success('注册成功，请登录');
                    this.$router.push('/login');
                } else {
                    this.$message.error(response.msg);
                }
            } catch (error) {
                console.error(error);
                this.$message.error('注册失败，请稍后再试');
            }
        }
    }
};
</script>

<style scoped>
.register-vue {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
}

.register-vue .container {
    background: rgba(255, 255, 255, .5);
    width: 300px;
    text-align: center;
    border-radius: 10px;
    padding: 30px;
}

.register-vue .input-c {
    margin: auto;
    width: 200px;
    margin-bottom: 20px;
}

.register-vue .submit {
    width: 200px;
}
</style>