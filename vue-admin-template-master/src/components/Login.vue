<template>
    <div class="login-vue" :style="bg">
        <div class="container">
            <p class="title">WELCOME</p>
            <div class="input-c">
                <Input prefix="ios-contact" v-model="account" placeholder="用户名" clearable @on-blur="verifyAccount" />
                <p class="error">{{accountError}}</p>
            </div>
            <div class="input-c">
                <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable @on-blur="verifyPwd"
                       @keyup.enter.native="submit" />
                <p class="error">{{pwdError}}</p>
            </div>
            <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">登陆</Button>
            <p class="account"><span @click="register">注册账号</span> | <span @click="forgetPwd">忘记密码</span></p>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request';

export default {
    name: 'login',
    data() {
        return {
            account: '',
            pwd: '',
            accountError: '',
            pwdError: '',
            isShowLoading: false,
            bg: {},
        };
    },
    created() {
        this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg0' + new Date().getDay() + '.jpg') + ')';
    },
    watch: {
        $route: {
            handler(route) {
                this.redirect = route.query && route.query.redirect;
            },
            immediate: true,
        },
    },
    methods: {
        verifyAccount() {
            if (!this.account) {
                this.accountError = '请输入用户名';
            } else {
                this.accountError = '';
            }
        },
        verifyPwd() {
            if (!this.pwd) {
                this.pwdError = '请输入密码';
            } else {
                this.pwdError = '';
            }
        },
        register() {
            // 跳转到注册页面
            console.log('Register method is called');
            this.$router.push({ name: 'register' });
        },
        forgetPwd() {
            // 跳转到忘记密码页面
            this.$router.push('/forget-password');
        },
        async submit() {
            this.verifyAccount();
            this.verifyPwd();
            if (this.accountError || this.pwdError) {
                return;
            }
            this.isShowLoading = true;
            try {
                const res = await request.post('http://localhost:8000/myApp/login/', {
                    username: this.account,
                    password: this.pwd,
                });
                if (res.code === 0) {
                    // 登陆成功 设置用户信息
                    localStorage.setItem('userImg', res.data.userImg);
                    localStorage.setItem('userName', res.data.userName);
                    // 登陆成功 假设这里是后台返回的 token
                    localStorage.setItem('token', res.data.token);
                    this.$router.push({ path: this.redirect || '/' });
                } else {
                    this.accountError = res.msg;
                }
            } catch (error) {
                console.error(error);
                this.accountError = '登录失败，请稍后重试';
            } finally {
                this.isShowLoading = false;
            }
        },
    },
};
</script>

<style>
.login-vue {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
}

.login-vue .container {
    background: rgba(255, 255, 255, .5);
    width: 300px;
    text-align: center;
    border-radius: 10px;
    padding: 30px;
}

.login-vue .ivu-input {
    background-color: transparent;
    color: #fff;
    outline: #fff;
    border-color: #fff;
}

.login-vue ::-webkit-input-placeholder {
    /* WebKit, Blink, Edge */
    color: rgba(255, 255, 255, .8);
}

.login-vue :-moz-placeholder {
    /* Mozilla Firefox 4 to 18 */
    color: rgba(255, 255, 255, .8);
}

.login-vue ::-moz-placeholder {
    /* Mozilla Firefox 19+ */
    color: rgba(255, 255, 255, .8);
}

.login-vue :-ms-input-placeholder {
    /* Internet Explorer 10-11 */
    color: rgba(255, 255, 255, .8);
}

.login-vue .title {
    font-size: 16px;
    margin-bottom: 20px;
}

.login-vue .input-c {
    margin: auto;
    width: 200px;
}

.login-vue .error {
    color: red;
    text-align: left;
    margin: 5px auto;
    font-size: 12px;
    padding-left: 30px;
    height: 20px;
}

.login-vue .submit {
    width: 200px;
}

.login-vue .account {
    margin-top: 30px;
}

.login-vue .account span {
    cursor: pointer;
}

.login-vue .ivu-icon {
    color: #eee;
}

.login-vue .ivu-icon-ios-close-circle {
    color: #777;
}
</style>