import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            meta: {title: '自述文件'},
            children: [
                {
                    path: '/dashboard',
                    component: resolve => require(['../components/page/Dashboard.vue'], resolve),
                    meta: {title: '系统首页'}
                },
                {
                    path: '/404',
                    component: resolve => require(['../components/page/404.vue'], resolve),
                    meta: {title: '404'}
                },
                {
                    path: '/403',
                    component: resolve => require(['../components/page/403.vue'], resolve),
                    meta: {title: '403'}
                }
                ,
                {
                    path: '/userTable',
                    component: resolve => require(['../components/page/UserTable.vue'], resolve),
                    meta: {title: '用户管理'}
                }
                ,
                {
                    path: '/menuTable',
                    component: resolve => require(['../components/page/MenuTable.vue'], resolve),
                    meta: {title: '菜单管理'}
                }
                ,
                {
                    path: '/roleTable',
                    component: resolve => require(['../components/page/RoleTable.vue'], resolve),
                    meta: {title: '角色管理'}
                }
                ,
                {
                    path: '/logTable',
                    component: resolve => require(['../components/page/LogTable.vue'], resolve),
                    meta: {title: '日志管理'}
                }
                ,
                {
                    path: '/channel',
                    component: resolve => require(['../components/page/ChannelTable.vue'], resolve),
                    meta: {title: '渠道管理'}
                }
                ,
                {
                    path: '/dicts',
                    component: resolve => require(['../components/page/DictTable.vue'], resolve),
                    meta: {title: '字典管理'}
                }

            ]
        },
        {
            path: '/login',
            component: resolve => require(['../components/page/Login.vue'], resolve)
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
