<template>
    <div class="register-vue" :style="bg">
        <div class="container">
            <p class="title">REGISTER</p>
            <div class="input-c">
                <Input prefix="ios-contact" v-model="account" placeholder="用户名" clearable @on-blur="verifyAccount" />
                <p class="error">{{accountError}}</p>
            </div>
            <div class="input-c">
                <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable @on-blur="verifyPwd" />
                <p class="error">{{pwdError}}</p>
            </div>
            <div class="input-c">
                <Input type="password" v-model="confirmPwd" prefix="md-lock" placeholder="确认密码" clearable
                       @on-blur="verifyConfirmPwd" />
                <p class="error">{{confirmPwdError}}</p>
            </div>
            <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">注册</Button>
            <p class="account"><span @click="goLogin">返回登录</span></p>
        </div>
    </div>
</template>

<script>
import request from '@/utils/request';
import { Message } from 'view-design';

export default {
    name: 'register',
    data() {
        return {
            account: '',
            pwd: '',
            confirmPwd: '',
            accountError: '',
            pwdError: '',
            confirmPwdError: '',
            isShowLoading: false,
            bg: {},
        };
    },
    created() {
        this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg0' + new Date().getDay() + '.jpg') + ')';
    },
    methods: {
        register() {
            try {
                this.$router.push('/register');
            } catch (error) {
                console.error('导航到注册页面时出错:', error);
            }
        },
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
            } else if (this.pwd.length < 6) {
                this.pwdError = '密码长度不能少于6位';
            } else {
                this.pwdError = '';
            }
        },
        verifyConfirmPwd() {
            if (this.pwd !== this.confirmPwd) {
                this.confirmPwdError = '两次输入的密码不一致';
            } else {
                this.confirmPwdError = '';
            }
        },
        goLogin() {
            this.$router.push('/login');
        },
        async submit() {
            this.verifyAccount();
            this.verifyPwd();
            this.verifyConfirmPwd();
            if (this.accountError || this.pwdError || this.confirmPwdError) {
                return;
            }
            this.isShowLoading = true;
            try {
                console.log('Sending registration data:', {
                    username: this.account,
                    password: this.pwd,
                });
                const res = await request.post('http://localhost:8000/myApp/register/', {
                    username: this.account,
                    password: this.pwd,
                });
                console.log('Registration response:', res);
                if (res.code === 0) {
                    Message.success('注册成功，请登录');
                    this.$router.push('/login');
                } else {
                    this.accountError = res.msg;
                }
            } catch (error) {
                console.error(error);
                this.accountError = '注册失败，请稍后重试';
            } finally {
                this.isShowLoading = false;
            }
        },
    },
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

.register-vue .ivu-input {
    background-color: transparent;
    color: #fff;
    outline: #fff;
    border-color: #fff;
}

.register-vue ::-webkit-input-placeholder {
    /* WebKit, Blink, Edge */
    color: rgba(255, 255, 255, .8);
}

.register-vue :-moz-placeholder {
    /* Mozilla Firefox 4 to 18 */
    color: rgba(255, 255, 255, .8);
}

.register-vue ::-moz-placeholder {
    /* Mozilla Firefox 19+ */
    color: rgba(255, 255, 255, .8);
}

.register-vue :-ms-input-placeholder {
    /* Internet Explorer 10-11 */
    color: rgba(255, 255, 255, .8);
}

.register-vue .title {
    font-size: 16px;
    margin-bottom: 20px;
}

.register-vue .input-c {
    margin: auto;
    width: 200px;
}

.register-vue .error {
    color: red;
    text-align: left;
    margin: 5px auto;
    font-size: 12px;
    padding-left: 30px;
    height: 20px;
}

.register-vue .submit {
    width: 200px;
}

.register-vue .account {
    margin-top: 30px;
}

.register-vue .account span {
    cursor: pointer;
}

.register-vue .ivu-icon {
    color: #eee;
}

.register-vue .ivu-icon-ios-close-circle {
    color: #777;
}
</style>