import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import '../static/css/theme-green/index.css';       // 浅绿色主题
import './assets/css/icon.css';
import './components/common/directives';
import "babel-polyfill";
// import { Message } from 'element-ui';
// Vue.prototype.$message = Message;

Vue.config.productionTip = false
Vue.use(ElementUI, {
    size: 'small'
});
Vue.prototype.$axios = axios;
// 路由响应拦截
// http response 拦截器
axios.interceptors.response.use(
    response => {
        if (response.data.code === 200 || response.data.code === "200") {
            return response
        } else if (response.data.code === 204 || response.data.code === 205) { //登录超时和异地登录都跳登录页面
            sessionStorage.setItem('authorization', '-1');
            sessionStorage.setItem('user_id', '-1');
            Vue.prototype.$message.error(response.data.msg);
            router.replace({
                path: 'login',
                query: {
                    redirect: router.currentRoute.fullPath
                }
            })
            return false
        } else if (response.data.code === 203) { //没有权限操作
            Vue.prototype.$message.error(response.data.msg);
            router.replace({
                path: '403',
                query: {
                    redirect: router.currentRoute.fullPath
                }
            })
            return false
        } else if (response.data.code > 205 && response.data.code < 299) {
            return response
        }else {
            alert(response.data.msg);
        }
    },
    error => {
        return Promise.reject(error.response)   // 返回接口返回的错误信息
    }
);
//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    let authorization = sessionStorage.getItem('authorization'); //鉴权加密串
    let user_id = sessionStorage.getItem('user_id'); //user_id
    let user_name = sessionStorage.getItem('user_name'); //user_name
    axios.defaults.headers.common['authorization'] = authorization;
    axios.defaults.headers.common['user_id'] = user_id;
    axios.defaults.headers.common['user_name'] = user_name;
    console.log(user_name)
    axios.defaults.headers.common['url'] = to.path;
    let loginStatus = 0;// 0:未登录,1:登录

    if (authorization !== -1 && user_id !== -1 && authorization !== "-1" && user_id !== "-1" && authorization !== null && user_id !== null && authorization !== "" && user_id !== "" && authorization !== undefined && user_id !== undefined && authorization !== "undefined" && user_id !== "undefined") {
        loginStatus = 1
    }

    if (to.path === '/403' || to.path === '/404') {
        next()
    }

    if (loginStatus === 0 && to.path !== "/login") { // 用户未登录时
        next('/login')
    } else if (loginStatus === 1) {
        if (to.path === '/login' || to.path === '/') {
            next('/dashboard');
        } else {
            if (to.path === '/dashboard') {
                next()
            } else {
                let bol = true;
                const permission = sessionStorage.getItem('permission');
                const permissionARR = permission.split(",");
                for (let i = 0; i < permissionARR.length; i++) {
                    if (permissionARR[i] === to.path) {
                        bol = false;
                        next()
                    }
                }
                if (bol) {
                    next('/dashboard')
                }

            }
        }
    } else {
        next()
    }
})


new Vue({
    router,
    render: h => h(App)
}).$mount('#app')