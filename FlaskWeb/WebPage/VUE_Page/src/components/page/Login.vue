<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">后台管理系统</div>
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="ruleForm.username" placeholder="username">
                        <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" placeholder="password" v-model="ruleForm.password"
                              @keyup.enter.native="submitForm('ruleForm')">
                        <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm()">登录</el-button>
                </div>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        data: function () {
            return {
                ruleForm: {
                    username: 'admin',
                    password: '123123'
                },
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ]
                }
            }
        },
        methods: {
            submitForm() {
                if (this.ruleForm.username === null || this.ruleForm.username === '' || this.ruleForm.username === undefined || this.ruleForm.username === 'undefined') {
                    this.$message.error('登录名不能为空');
                    return false;
                }

                if (this.ruleForm.password === null || this.ruleForm.password === '' || this.ruleForm.password === undefined || this.ruleForm.password === 'undefined') {
                    this.$message.error('密码不能为空');
                    return false;
                }

                let json = {
                    username: this.ruleForm.username,
                    password: this.ruleForm.password
                };
                this.$axios.post("/api/sys_user/login", json).then((res) => {
                    if (res.data.code === 200) {
                        sessionStorage.setItem('authorization',res.headers['authorization']);
                        sessionStorage.setItem('user_name',res.headers['user_name']);
                        sessionStorage.setItem('user_id', res.headers['user_id']);
                        this.$message.success('登录成功');
                        this.$router.push('/dashboard');
                    } else {
                        this.$message.success(res.data.msg);
                    }
                }).catch(function (error) {
                    // alert("err==" + error);
                });
            }
        }
    }
</script>

<style scoped>
    .login-wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }

    .ms-title {
        width: 100%;
        line-height: 50px;
        text-align: center;
        font-size: 20px;
        color: #fff;
        border-bottom: 1px solid #ddd;
    }

    .ms-login {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 350px;
        margin: -190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.3);
        overflow: hidden;
    }

    .ms-content {
        padding: 30px 30px;
    }

    .login-btn {
        text-align: center;
    }

    .login-btn button {
        width: 100%;
        height: 36px;
        margin-bottom: 10px;
    }

    .login-tips {
        font-size: 12px;
        line-height: 30px;
        color: #fff;
    }
</style>