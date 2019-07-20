<template>
    <div class="header">
        <!-- 折叠按钮 -->
        <div class="collapse-btn" @click="collapseChage">
            <i class="el-icon-menu"></i>
        </div>
        <div class="logo">后台管理系统</div>
        <div class="header-right">
            <div class="header-user-con">
                <!-- 全屏显示 -->
                <div class="btn-fullscreen" @click="handleFullScreen">
                    <el-tooltip effect="dark" :content="fullscreen?`取消全屏`:`全屏`" placement="bottom">
                        <i class="el-icon-rank"></i>
                    </el-tooltip>
                </div>
                <!-- 用户头像 -->
                <div class="user-avator"><img src="../../assets/img/img.jpg"></div>
                <!-- 用户名下拉菜单 -->
                <el-dropdown class="user-name" trigger="click" @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{username}} <i class="el-icon-caret-bottom"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
<!--                        <el-dropdown-item divided command="personal_data">个人资料</el-dropdown-item>-->
                        <el-dropdown-item divided command="update_pwd">修改密码</el-dropdown-item>
                        <el-dropdown-item divided command="loginout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
        </div>

        <!--个人资料页面-->
<!--        <el-dialog title="个人资料" :visible.sync="personal_data_page" width="30%">-->
<!--            <el-card shadow="hover" class="mgb20" style="height:252px;">-->
<!--                <div class="user-info">-->
<!--                    <img src="../../assets/img/img.jpg" class="user-avator" alt="">-->
<!--                    <div class="user-info-cont">-->
<!--                        <div class="user-info-name">{{name}}</div>-->
<!--                        <div>{{role}}</div>-->
<!--                    </div>-->
<!--                </div>-->
<!--                <div class="user-info-list">上次登录时间：<span>2018-01-01</span></div>-->
<!--                <div class="user-info-list">上次登录地点：<span>东莞</span></div>-->
<!--            </el-card>-->


<!--            <span slot="footer" class="dialog-footer">-->
<!--                <el-button @click="personal_data_page = false">取 消</el-button>-->
<!--                <el-button type="primary" @click="acceptAdd">确 定</el-button>-->
<!--            </span>-->
<!--        </el-dialog>-->

        <!-- 修改密码 -->
        <el-dialog title="修改密码" :visible.sync="update_pwd_page" width="30%">
            <el-form ref="form" :model="update_pwd_data" label-width="120px">
                <el-form-item label="原始密码">
                    <el-input type="password" v-model="update_pwd_data.pwd"></el-input>
                </el-form-item>
                <el-form-item label="新密码">
                    <el-input type="password" v-model="update_pwd_data.new_pwd"></el-input>
                </el-form-item>
                <el-form-item label="确认密码">
                    <el-input type="password" v-model="update_pwd_data.check_pwd"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="update_pwd_page = false">取 消</el-button>
                <el-button type="primary" @click="update_pwd_submit">确 定</el-button>
            </span>
        </el-dialog>

    </div>
</template>
<script>
    import bus from '../common/bus';

    export default {
        data() {
            return {
                addLoading: false,

                collapse: false,
                fullscreen: false,
                update_pwd_page: false,
                personal_data_page: false,
                update_pwd_data: {
                    pwd: '',
                    new_pwd: '',
                    check_pwd: ''
                }
            }
        },
        computed: {
            username() {
                let username = sessionStorage.getItem('user_name');
                return username //? username : this.name;
            }
        },
        methods: {
            // 用户名下拉菜单选择事件
            handleCommand(command) {
                if (command == 'loginout') {
                    this.$axios.post("/api/sys_user/logOut").then((res) => {
                        if (res.data.code === 200) {
                            sessionStorage.setItem('authorization', res.headers['authorization']);
                            sessionStorage.setItem('user_name', res.headers['user_name']);
                            sessionStorage.setItem('user_id', res.headers['user_id']);
                            this.$message.success('安全退出');
                            this.$router.push('/login');
                        } else {
                            this.$message.success(res.data.msg);
                        }
                    }).catch(function (error) {
                        alert("err==" + error);
                    });
                    sessionStorage.removeItem('authorization')
                    sessionStorage.removeItem('user_name')
                    sessionStorage.removeItem('user_id')
                    // ajax执行后台退出,前端执行清空请求头设置.
                }
                if (command === 'update_pwd') {
                    this.update_pwd_data.pwd = '',
                    this.update_pwd_data.new_pwd = '',
                    this.update_pwd_data.check_pwd = '',
                    this.update_pwd_page = true
                }

                if (command === 'personal_data') {
                    this.personal_data_page = true
                }

            },
            // 侧边栏折叠
            collapseChage() {
                this.collapse = !this.collapse;
                bus.$emit('collapse', this.collapse);
            },
            // 全屏事件
            handleFullScreen() {
                let element = document.documentElement;
                if (this.fullscreen) {
                    if (document.exitFullscreen) {
                        document.exitFullscreen();
                    } else if (document.webkitCancelFullScreen) {
                        document.webkitCancelFullScreen();
                    } else if (document.mozCancelFullScreen) {
                        document.mozCancelFullScreen();
                    } else if (document.msExitFullscreen) {
                        document.msExitFullscreen();
                    }
                } else {
                    if (element.requestFullscreen) {
                        element.requestFullscreen();
                    } else if (element.webkitRequestFullScreen) {
                        element.webkitRequestFullScreen();
                    } else if (element.mozRequestFullScreen) {
                        element.mozRequestFullScreen();
                    } else if (element.msRequestFullscreen) {
                        // IE11
                        element.msRequestFullscreen();
                    }
                }
                this.fullscreen = !this.fullscreen;
            },

            //修改密码提交
            update_pwd_submit(){

            },

        },
        mounted() {
            if (document.body.clientWidth < 1500) {
                this.collapseChage();
            }
        }
    }
</script>
<style scoped>
    .header {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        height: 70px;
        font-size: 22px;
        color: #fff;
    }

    .collapse-btn {
        float: left;
        padding: 0 21px;
        cursor: pointer;
        line-height: 70px;
    }

    .header .logo {
        float: left;
        width: 250px;
        line-height: 70px;
    }

    .header-right {
        float: right;
        padding-right: 50px;
    }

    .header-user-con {
        display: flex;
        height: 70px;
        align-items: center;
    }

    .btn-fullscreen {
        transform: rotate(45deg);
        margin-right: 5px;
        font-size: 24px;
    }

    .btn-bell, .btn-fullscreen {
        position: relative;
        width: 30px;
        height: 30px;
        text-align: center;
        border-radius: 15px;
        cursor: pointer;
    }

    .btn-bell-badge {
        position: absolute;
        right: 0;
        top: -2px;
        width: 8px;
        height: 8px;
        border-radius: 4px;
        background: #f56c6c;
        color: #fff;
    }

    .btn-bell .el-icon-bell {
        color: #fff;
    }

    .user-name {
        margin-left: 10px;
    }

    .user-avator {
        margin-left: 20px;
    }

    .user-avator-img {
        margin-left: 20%;
        margin-top: 20%;
    }

    .user-avator img {
        display: block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }

    .el-dropdown-link {
        color: #fff;
        cursor: pointer;
    }

    .el-dropdown-menu__item {
        text-align: center;
    }

    .user-info-cont {
        padding-left: 50px;
        flex: 1;
        font-size: 14px;
        color: #999;
    }

    .user-info-cont div:first-child {
        font-size: 30px;
        color: #222;
    }

    .user-info-list {
        font-size: 14px;
        color: #999;
        line-height: 25px;
    }

    .user-info-list span {
        margin-left: 70px;
    }

    .content-title {
        font-weight: 400;
        line-height: 50px;
        margin: 10px 0;
        font-size: 22px;
        color: #1f2f3d;
    }

    .pre-img {
        width: 100px;
        height: 100px;
        background: #f8f8f8;
        border: 1px solid #eee;
        border-radius: 5px;
    }

    .crop-demo {
        display: flex;
        align-items: flex-end;
    }

    .crop-demo-btn {
        position: relative;
        width: 100px;
        height: 40px;
        line-height: 40px;
        padding: 0 20px;
        margin-left: 30px;
        background-color: #409eff;
        color: #fff;
        font-size: 14px;
        border-radius: 4px;
        box-sizing: border-box;
    }

    .crop-input {
        position: absolute;
        width: 100px;
        height: 40px;
        left: 0;
        top: 0;
        opacity: 0;
        cursor: pointer;
    }
</style>
